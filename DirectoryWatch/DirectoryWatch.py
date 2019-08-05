""""
Directory Watcher

Reporting status and handling files when files have
been added, removed or updated within a directory.

Adapted from: http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
"""

import os
import win32file
import win32con  # global constant definitions for interfacing with win32file
import tkinter as tk
import threading
import datetime as dt


# Set test path here
TEST_PATH = r'C:\Users\Tanat\Desktop\test'

# This is a arbitrary input. Not quite sure why this number works.
FILE_LIST_DIRECTORY = 0x0001  # equals to 1 in base-10
# setting flag for thread worker
is_running = True


class DirectoryWatch:
    """
    This class access a folder to look for changes and report back to main thread.

    Attributes:
        WATCH_PATH (str): The folder path to watch.
    """
    def __init__(self, watch_path=TEST_PATH):
        self.watch_path = watch_path
        # Create an object to return a handle that can be used to access the folder.
        self.hDir = win32file.CreateFile(fileName=self.watch_path,
                                         desiredAccess=FILE_LIST_DIRECTORY,
                                         shareMode=win32con.FILE_SHARE_READ |
                                                   win32con.FILE_SHARE_WRITE |
                                                   win32con.FILE_SHARE_DELETE,
                                         attributes=None,
                                         CreationDisposition=win32con.OPEN_EXISTING,
                                         flagsAndAttributes=win32con.FILE_FLAG_BACKUP_SEMANTICS,
                                         hTemplateFile=None
                                         )
        # Set up the thread
        thread = threading.Thread(target=self.watcher_thread)
        thread.start()

    def watcher_thread(self):
        """
        A function to retrieve information describing the changes occurring within a directory.

        ReadDirectoryChangesW takes a previously-created handle to a directory, a buffer size for results,
        a flag to indicate whether to watch subtrees and a filter of what changes to notify. For larger batch
        processing, the buffer size may need to be increased to handle the change information.
        """
        # Dictionary for different action types
        ACTIONS = {
            1: "Created",
            2: "Deleted",
            3: "Updated",
            4: "Renamed from something",
            5: "Renamed to something"
        }
        # create container to temporarily record changes
        temp_log = list()
        while is_running:
            # retrieve information describing the changes occurring within a directory
            results = win32file.ReadDirectoryChangesW(handle=self.hDir,
                                                      size=1024,
                                                      bWatchSubtree=True,
                                                      dwNotifyFilter=win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                                                                     win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                                                                     win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                                                                     win32con.FILE_NOTIFY_CHANGE_SIZE |
                                                                     win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                                                                     win32con.FILE_NOTIFY_CHANGE_SECURITY,
                                                      overlapped=None
                                                      #, None <= here is a legacy code that I cannot find the
                                                      # formal parameter name for, so I'm storing here in case
                                                      # it is important.
                                                      )
            # reading the changes and initiate actions
            for action, file in results:
                # get path of file with changes
                full_filename = os.path.join(self.watch_path, file)
                # append the list of CREATED files to another module for server upload
                temp_log.append((full_filename, ACTIONS.get(action, "Unknown")))
                # yield the list of CREATED files to another module for server upload
                yield full_filename, ACTIONS.get(action, "Unknown")
            # send the list of changes to GUI container
            yield temp_log
            # clear temporary log
            temp_log.clear()


class GuiPart(tk.Frame):
    """
    This is a GUI to show changes found by watcher_thread
    """
    def __init__(self, master=None):
        # Set up the GUI
        tk.Frame.__init__(self, master)
        self.pack()
        self.textVar = tk.StringVar()
        tk.Label(self, text="Directory Status (recent 10)", font='Arial 12 bold').pack()
        tk.Label(self, textvariable=self.textVar, justify='left', anchor='n').pack()
        # tk.Button(master, text='Done', command=self.end_command).pack()

    def update_label(self):
        for action, file in results:
            full_filename = os.path.join(self.watch_path, file)
            textList = wndw.textVar.get().split('\n')
            new_line = dt.datetime.now().strftime("%Y-%m-%d %H:%M") + "\t..." + \
                       str(full_filename[len(full_filename) - 15:]) + "  \t" + \
                       str(ACTIONS.get(action, "Unknown"))
            if action == 1:
                yield full_filename
            if len(textList) >= 10:
                textList = textList[1:]
                textList.append(new_line)
                updated_text = '\n'.join(textList)
            else:
                textList.append(new_line)
                updated_text = '\n'.join(textList)
            wndw.textVar.set(updated_text)
        pass

    @staticmethod
    def end_command():
        is_running = False
        exit()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x200")  # set default window geometry
    root.resizable(0, 0)  # prevent resizing in the x or y directions
    mainframe = GuiPart(root)  # initiate GUI
    root.after(250, mainframe.update_label)  # update GUI at 250ms intervals
    root.mainloop()

