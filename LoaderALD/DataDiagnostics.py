"""
Perform diagnosis & due-diligence on data before upload
"""
import glob
import pandas as pd
import timeit
import re
import pprint
from collections import defaultdict
import os
import numpy as np
import random
import math
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import statistics


class EmptyFileFiler:

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

