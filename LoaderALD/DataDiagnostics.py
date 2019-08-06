"""
Perform diagnosis & due-diligence on data before upload
"""
import glob
import pandas as pd
import timeit
import re
from collections import defaultdict
import os
import numpy as np
import random
import math
import statistics


class EmptyFileFiler:
    """
    Create a list of files that are empty and do not hold value.

    In addition to determining whether the file is empty,
    this section indicates the number of columns in the data
    (first line) and index the integer number on the row.
    This is important as the only number in Heater Data that
    was recorded as integer is the number of cycles remaining.
    We can use that to re-issue the header.
    """
    def __init__(self, folder_name: str):
        self.folder_name = folder_name
        pass

    @staticmethod
    def filter_valid(element):
        invalid_entry = ['nan', None, 'NA']

        if (str(element) in invalid_entry):
            return False  # Discount the invalid
        else:
            return True  # Count the valid

    @staticmethod
    def list_find_integer(given_list):
        # The only number in Heater Data that was recorded as integer
        # is number of cycles remaining, and always available.
        ndx = 0
        last_ndx = 0
        for word in given_list:
            if str(word).isdigit():
                break  # last_ndx = ndx
            ndx += 1
        return ndx  # Return the first integer

    def count_empty_dataframe(self):
        # Note the files that doesn't have log data (only headers are available)
        # get data file names
        base_path = r'C:\Users\Tanat\PycharmProjects\NHI-ALD\Logfile'
        path = r''.join([base_path, '\\', self.folder_name])
        print("path: " + path)
        filenames = glob.glob(path + "/*.txt")

        counter = 0
        anticounter = 0
        column_count = list()
        int_count = list()
        iterable = list()
        coll_count = ''
        int_counter = ''

        output_filename1 = "".join(["empty_files_", self.folder_name.replace(" ", ""), ".txt"])
        output_filename2 = "".join(["valid_files_", self.folder_name.replace(" ", ""), ".txt"])

        with open(output_filename1, "w+") as file1:
            with open(output_filename2, "w+") as file2:
                for filename in filenames:
                    try:  # In case that file is EMPTY

                        '''if not '2019_06_25-13-46_Optimized 200C.txt' in filename:
                            raise ValueError()  # target specific file
                        else:
                            print(filename)'''

                        data = pd.read_csv(filename, sep="\t", engine='python', nrows=1)
                        if data.empty:
                            counter += 1
                            file1.write(filename[:] + "\n")
                        else:  # In case that file is NOT EMPTY
                            anticounter += 1
                            iterable = data.values.tolist()
                            cleanedList = list(filter(self.filter_valid, iterable[0]))
                            # Another quick way to create a filter is to use an in-line conditional expression below:
                            # cleanedList = [x for x in iterable[0] if str(x) != 'nan']
                            k = len(cleanedList)  # get the number of elements in the cleanedlist
                            int_index = self.list_find_integer(cleanedList)
                            file2.write(filename[59:] + "\t" + str(k) + "\t" + str(
                                int_index) + "\n")  # Record the valid filenames + number of column

                            if int_index not in int_count:
                                int_count.append(int_index)  # return the number of pandas column
                            int_count.sort()
                            int_counter = " ".join(map(str, int_count))

                            if k not in column_count:
                                column_count.append(k)  # return the number of pandas column
                            column_count.sort()
                            coll_count = " ".join(map(str, column_count))
                        print('Empty: ' + str(counter) + ' | Valid: ' + str(
                            anticounter) + ' | Column = ' + coll_count + ' | Integer @ ' + int_counter, end="\r",
                              flush=True)

                    except pd.io.common.EmptyDataError:
                        counter = counter + 1
                        # print('EmptyDataError: '+filename[46:], end="\n")
                        print('Empty: ' + str(counter) + ' | Valid: ' + str(
                            anticounter) + ' | Column = ' + coll_count + ' | Integer @ ' + int_counter, end="\r",
                              flush=True)
                        file1.write(filename[:] + "\n")

                    '''except ValueError:
                        pass'''

        print('Empty: ' + str(counter) + ' | Valid: ' + str(
            anticounter) + ' | Column = ' + coll_count + ' | Integer @ ' + int_counter, end="\n", flush=True)
        print('------------ Completed ------------')
        return


class PreProcess:
    """
    Data pre-processing

    Replace new header for Heater Data files
    """
    def __init__(self):
        pass

    @staticmethod
    def change_header():
        # Heater data has problems with mis-matched header

        heater_temp = ['', 'Heater Time', 'Program Time', 'MFC 1', 'MFC Time', 'Cycles Remaining', 'Recipe', 'Loop',
                       '\n']
        with open("valid_files_HeaterData.txt", "r") as f:
            content = f.readlines()
            new_content = []
            loop = 0
            net_loop = len(content)
            for line in content:
                elem = line[:-1].split('\t')
                add_heater = int(elem[2]) - 4
                heater_header = heater_temp.copy()
                for i in range(1, add_heater + 1):  # for range = [a,b) i.e. exclude last number
                    new_heater = 'Heater ' + str(i)  # Assign an arbitary heater number
                    heater_header.insert(i + 1, new_heater)  # insert 1 heater before given index
                header_replacement = '\t'.join(map(str, heater_header))

                new_path = 'Results/Heater Data (Fixed)/'
                filename = ''.join([new_path, elem[0]])
                old_path = r'C:\Users\Tanat\PycharmProjects\NHI-ALD\Logfile\Heater Data'
                sourcefile = r''.join([old_path, '\\', elem[0]])

                with open(filename, "w") as file1:
                    with open(sourcefile, "r") as file2:
                        content = file2.readlines()
                        content[0] = header_replacement
                    file1.writelines(content)

                heater_header.clear()
                new_content.clear()
                loop += 1
                print('Iterating: ' + str(loop) + "/" + str(net_loop), end='\r')

class MissingSet:
    """
    Filter common / missing files from the set
    """
    def __init__(self):
        folder_names = ["Heater Data", "Pressure Data", "RF Data", "Reports"]
        rawnames = []
        union_set = set()
        folder_set = {}
        diff = []
        listw = {}
        list_diff = {}
        missing_filenames = {'Filenames': []}
        common_filenames = {'Filenames': []}
        filenames = list()
        file_num = len(folder_names)
        pass

    #@classmethod
    def extract_name(self):
        ''' Section A: Extract names of all files '''

        for name in folder_names: missing_filenames.setdefault(name, [])

        for folder_name in folder_names:  # iterate for each folder name
            base_path = r'C:\Users\Tanat\PycharmProjects\NHI-ALD\Logfile'
            path = r''.join([base_path, '\\', folder_name])
            filenames.append(glob.glob(path + "/*"))

        for k in range(0, file_num):  # iterate each folder
            for filename in filenames[k]:  # iterate each file in folder
                a = re.split('\\\\', filename)
                rawnames.append(a[-1][:-4])  # Extract only the file name, extension removed
            folder_set[k] = set(rawnames)  # Transfer list of file names to a separate set
            rawnames.clear()

    #@classmethod
    def create_missing_list(self):
        ''' Section B: Create a list of missing files '''

        for i in range(0, file_num):  # iterate each folder
            union_set = union_set | set(folder_set[i])  # Create a union set

        for i in range(0, file_num):  # iterate each folder
            base = set(folder_set[i])  # copy each folder to a set variable, base
            list_diff = union_set.difference(base)  # find the relative complement of base set in union set
            # This denotes all the files that base set is missing
            # for elem in list(list_diff):
            #     missing_filenames.setdefault(elem, []).append(folder_names[i])
            # Appended here is the folder that does not have the filename

            for elem in list(list_diff):
                if elem not in missing_filenames.get('Filenames', ''):
                    missing_filenames['Filenames'].append(elem)
                    for name in folder_names:
                        missing_filenames[name].append("")
                    missing_filenames[folder_names[i]][-1] = "Missing"
                else:
                    ndx = missing_filenames['Filenames'].index(elem)
                    missing_filenames[folder_names[i]][ndx] = "Missing"

    #@classmethod
    def create_common_list(self):
        ''' Section C: Create a list of common files '''

        intersection_list = set(folder_set[0])
        for i in range(0, file_num):  # iterate each folder
            intersection_list = intersection_list.intersection(set(folder_set[i]))  # Create an intersection set

    def convert_to_dataframe(self):
        ''' Section D: Convert to dataframe '''

        df_missing = pd.DataFrame(missing_filenames)
        df_common = pd.DataFrame(intersection_list)

        # Saving Pandas DataFrames
        df_missing.to_csv("Results\missing files.csv", index=True, encoding='utf8')
        df_common.to_csv("Results\common files.csv", index=True, encoding='utf8')

        # (df_missing.style
        #    .applymap(color_cells, subset=["Heater Data", "Pressure Data", "RF Data", "Reports"])
        #    .set_table_styles(styles))

        # (df_common.style
        #    .set_table_styles(styles))

class FileMerger:
    """
    Merge common & valid files
    """
    def __init__(self):
        pass

    # Display and remove rows in heater data pandas
    def clean_heater_file(filename):
        base_path = r'C:\Users\Tanat\PycharmProjects\NHI-ALD\venv\Scripts\Results\Heater Data (Fixed)'
        path = r''.join([base_path, '\\', filename, '.txt'])
        with open(path, "r") as file:
            data1 = pd.read_csv(file, sep="\t", engine='python')
            data1 = data1.iloc[:, 1:-1]  # Remove the first column
            data1.rename(columns={'Heater Time': 'Time'}, inplace=True)
            data1.rename(columns={'Cycles Remaining': 'cycle1'}, inplace=True)
            data1.sort_values(by='Time')
        return data1

    # Display pressure data in pandas
    def clean_pressure_file(filename):
        base_path = r'C:\Users\Tanat\PycharmProjects\NHI-ALD\Logfile\Pressure Data'
        path = r''.join([base_path, '\\', filename, '.txt'])
        with open(path, "r") as file:
            data2 = pd.read_csv(file, sep="\t", engine='python')
            data2 = data2.iloc[:, 1:]  # Remove the first column
            data2.rename(columns={'Pressure ': 'Pressure'}, inplace=True)
            data2.rename(columns={'Pressure Time': 'Time'}, inplace=True)
            data2.rename(columns={'Cycles Remaining': 'cycle2'}, inplace=True)
            data2.sort_values(by='Time')
        return data2

    # Display RF data in pandas
    def clean_rf_file(filename):
        base_path = r'C:\Users\Tanat\PycharmProjects\NHI-ALD\Logfile\RF Data'
        path = r''.join([base_path, '\\', filename, '.txt'])
        with open(path, "r") as file:
            data3 = pd.read_csv(file, sep="\t", engine='python')
            data3 = data3.iloc[:, 1:]  # Remove the first column
        return data3
        # data3.hist(column='Cycles Remaining')

    def merge_heater_pressure_files(data1, data2):
        data1 = data1.replace({pd.np.nan: ''})
        data2 = data2.replace({pd.np.nan: ''})
        data = pd.merge_asof(data1, data2, on='Time')
        data = data[1:].replace({pd.np.nan: ''})  # removes the first line & replace Nan
        return data

        # list(data.columns.values)



