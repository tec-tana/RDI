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
import queue
import datetime as dt
# import local modules
import FileProcess


# Set test path here
TEST_PATH = r'C:\Users\Tanat\Desktop\test'

# This is a arbitrary input. Not quite sure why this number works.
FILE_LIST_DIRECTORY = 0x0001  # equals to 1 in base-10
# setting flag for thread worker
is_running = True
# set queue for watcher
queue_log = queue.Queue(maxsize=20)
# set queue for processing
# processing thread could take a long time, so we need larger buffer
queue_process = queue.Queue(maxsize=200)


class DirectoryWatch:
    """
    This class access a folder to look for changes and report back to main thread.

    Attributes:
        watch_path (str): The folder path to watch.
    """
    def __init__(self, watch_path=TEST_PATH):
        self.watch_path = watch_path
        # Create an object to return a handle that can be used to access the folder.
        self.hDir = win32file.CreateFile(self.watch_path,
                                         FILE_LIST_DIRECTORY,
                                         win32con.FILE_SHARE_READ |
                                         win32con.FILE_SHARE_WRITE |
                                         win32con.FILE_SHARE_DELETE,
                                         None,
                                         win32con.OPEN_EXISTING,
                                         win32con.FILE_FLAG_BACKUP_SEMANTICS,
                                         None
                                         )
        # Set up the thread for watcher
        thread_watcher = threading.Thread(target=self.watcher_thread)
        thread_watcher.daemon = True  # daemon thread dies when main thread exits, to combat with blocking thread
        thread_watcher.start()
        # Set up the thread for passing full_filename as argument
        thread_fileprocess = threading.Thread(target=file_process)
        thread_fileprocess.start()

    def watcher_thread(self):
        """
        A function to retrieve information describing the changes occurring within a directory.

        ReadDirectoryChangesW takes a previously-created handle to a directory, a buffer size for results,
        a flag to indicate whether to watch subtrees and a filter of what changes to notify. For larger batch
        processing, the buffer size may need to be increased to handle the change information.
        """
        global queue_log
        global is_running
        # Dictionary for different action types
        ACTIONS = {
            1: "Created",
            2: "Deleted",
            3: "Updated",
            4: "Renamed from something",
            5: "Renamed to something"
        }
        while is_running:  # This doesn't really work because ReadDirectoryChangesW is blocking
            # retrieve information describing the changes occurring within a directory
            results = win32file.ReadDirectoryChangesW(self.hDir,
                                                      1024,
                                                      True,
                                                      win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                                                      win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                                                      win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                                                      win32con.FILE_NOTIFY_CHANGE_SIZE |
                                                      win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                                                      win32con.FILE_NOTIFY_CHANGE_SECURITY,
                                                      None,
                                                      None
                                                      )
            # reading the changes and initiate actions
            for action, file in results:
                # get path of file with changes
                full_filename = os.path.join(self.watch_path, file)
                # append the list of CREATED files to another module for server upload
                queue_log.put((full_filename, ACTIONS.get(action, "Unknown")))
                # pass the list of CREATED files to another module for server upload
                if action == 1:  # if file is created
                    queue_process.put(full_filename)  # send filename to processing queue

        else:
            print("END thread 1")
            return


class GuiPart(tk.Frame):
    """
    This is a GUI to show changes found by watcher_thread.

    Attributes:
        master (tk): A tk object as the mainframe for GuiPart frame to reside in.
    """
    def __init__(self, master):
        self.master = master
        # Set up the GUI
        tk.Frame.__init__(self, master)
        self.pack()
        # create update-able container for status
        self.textVar = tk.StringVar()
        # display title
        tk.Label(self, text="Directory Status (recent 10)", font='Arial 12 bold').pack()
        # display status
        tk.Label(self, textvariable=self.textVar, justify='left', anchor='n').pack()
        # button to end program
        tk.Button(self, text='Close', command=self.end_command).pack()
        # execute end_command upon window delete
        self.master.protocol("WM_DELETE_WINDOW", self.end_command)

    def process_templog(self):
        """
        This function process the incoming log when queue is available.

        The one input of the function is a global variable, thus
        not required in the parameter.

        :return: None
        """
        # set default parameter to temp_log
        # This is the correct way to do default assignment on mutable object
        # because function declaration is processed only once, thus the updated
        # temp_log will not be recognized.
        global queue_log
        while queue_log.qsize():
            try:
                log = queue_log.get()
                # unpack tuple within the list
                full_filename, action = log
                # continue the process with updating display
                self.update_label(full_filename, action)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass
        # loop itself after 100ms interval
        self.update = root.after(100, mainframe.process_templog)

    def update_label(self, full_filename: str, action: str):
        """
        This function updates the status label on GUI.

        :param full_filename: raw string literal
        :param action: string literal
        """
        # set the number of lines that will be displayed
        DISPLAY_LIMIT = 10
        # get current displaying status
        text_list = self.textVar.get().split('\n')
        # create new line of status = date + filename + action
        new_line = dt.datetime.now().strftime("%Y-%m-%d %H:%M") + "\t    ..." + \
                   full_filename[len(full_filename) - 15:] + "       \t" + \
                   action
        # Replacing the oldest status over DISPLAY_LIMIT
        if len(text_list) >= DISPLAY_LIMIT:
            text_list = text_list[1:]  # Remove the oldest status
            text_list.append(new_line)
            updated_text = '\n'.join(text_list)
        else:  # for when there are less than DISPLAY_LIMIT
            text_list.append(new_line)
            updated_text = '\n'.join(text_list)
        # update text variable for label widget
        self.textVar.set(updated_text)

    def end_command(self):
        """
        This is an exit command for both GUI and thread_watcher
        """
        import sys
        global is_running
        # raises exit flag for thread
        is_running = False
        # cancel tk after
        self.master.after_cancel(self.update)
        # closes tk window
        self.master.destroy()
        # exit program
        exit()


def file_process():
    """
    This function process files that are newly created.
    """
    global is_running
    # while the program is running
    while is_running:
        # while there is a queue in queue_process
        while queue_process.qsize():
            try:
                # retrieve full_filename (raw string literal) from queue_process
                full_filename = queue_process.get()
                # process the file with external module
                FileProcess.file_process(full_filename)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass
    else:
        print('END thread 2')
        return


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x200")  # set default window geometry
    root.resizable(0, 0)  # prevent resizing in the x or y directions
    mainframe = GuiPart(root)  # initiate GUI
    watcher = DirectoryWatch(TEST_PATH)  # initialize DirectoryWatch
    root.after(100, mainframe.process_templog)  # update GUI at 100ms intervals
    root.mainloop()

