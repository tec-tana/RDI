""""
Signal Process

Reporting status and handling files when files have
been added, removed or updated within a directory.

Adapted from: http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
"""

# import standard lib
import os
import win32file
import win32con  # global constant definitions for interfacing with win32file
import threading
import queue
import datetime as dt
# import local modules
from config import cfg
from DirectoryWorker import FileProcess


# This is a arbitrary input. Not quite sure why this number works.
FILE_LIST_DIRECTORY = 0x0001  # equals to 1 in base-10
# setting flag for thread worker
is_running = True


class SignalWatch:
    """
    This class access a folder to look for changes and report back to main thread.

    Attributes:
        watch_path (str): The folder path to watch.
    """
    def __init__(self, watch_path):
        self.watch_path = watch_path
        self.watch_list = dict()  # create a dictionary to test if ALD program stops updating == finished run
        # Create an object to return a handle that can be used to access the folder.
        self.hDir = win32file.CreateFile(self.watch_path,
                                         FILE_LIST_DIRECTORY,
                                         win32con.FILE_SHARE_READ |
                                         win32con.FILE_SHARE_WRITE |
                                         win32con.FILE_SHARE_DELETE,
                                         None,
                                         win32con.OPEN_EXISTING,
                                         win32con.FILE_FLAG_BACKUP_SEMANTICS,
                                         None)
        # Set up the thread for watcher
        thread_watcher = threading.Thread(target=self.watcher_thread)
        thread_watcher.daemon = True  # daemon thread dies when main thread exits, to combat with blocking thread
        thread_watcher.start()
        # Set up the thread for passing full_filename as argument
        thread_fileprocess = threading.Thread(target=self.file_process)
        thread_fileprocess.daemon = True
        thread_fileprocess.start()
        # Set up the thread for passing full_filename as argument
        thread_watchlist = threading.Thread(target=self.watchlist)
        thread_watchlist.daemon = True
        thread_watchlist.start()

    def watcher_thread(self):
        """
        A function to retrieve information describing the changes occurring within a directory.

        ReadDirectoryChangesW takes a previously-created handle to a directory, a buffer size for results,
        a flag to indicate whether to watch subtrees and a filter of what changes to notify. For larger batch
        processing, the buffer size may need to be increased to handle the change information.
        """
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
                cfg.queue_log.put((full_filename, ACTIONS.get(action, "Unknown")))
                # decide what to do with the file
                self.watch_stop(action, full_filename)
        else:
            print("END thread 1")
            return

    def watch_stop(self, action, full_filename):
        """
        This function decides what to do with the file.

        Cuurently, it is assumed that the file is first created by ALD software
        then routinely updated during the run. In which case, we will watch for
        any changes with in 30 seconds. If there is no action, we can likely
        assume that the run has completed.

        On the other hand, if the file is created only after the run has completed,
        this will simplify the process as we will only need to look for CREATE
        signal.
        :return:
        """
        # CASE 1: File created when run starts, with routine updates
        # pass the CREATED / UPDATED files to another module for server upload
        try:

            if action == 2 and full_filename in self.watch_list:  # if file is deleted
                """ Not sure if this could happen, but container here just in case """
                del self.watch_list[full_filename]
            if action == 3:  # if file is updated
                self.watch_list[full_filename] = action, dt.datetime.now()  # update check time
        except KeyError:  # if there is no key, add key to watch_list
            self.watch_list[full_filename] = action, dt.datetime.now()  # add to watch list

        # CASE 2: File created after finished run
        """
        if action == 1:  # if file is created
            cfg.queue_process.put(full_filename, action)  # send filename to processing queue
        """

    def watchlist(self):
        WAIT_TIME = 10  # decide how long the program is going to wait for
        global is_running
        # while the program is running
        while is_running:
            # Checking through the watch list
            try:
                # unpack timestamp from last read status
                for full_filename, package in self.watch_list.items():
                    last_action, timestamp = package
                    # print(last_action, timestamp)
                    # If the file is not updating after 30 seconds, finished run.
                    # Forcing that the file must have gone through an update before, not just created.
                    # This is to ensure that the file has been used by the ALD software.
                    if (dt.datetime.now() - timestamp).total_seconds() > WAIT_TIME and last_action == 3:
                        cfg.queue_process.put(full_filename)  # send filename to processing queue
                        cfg.queue_log.put((full_filename, "Completed"))  # signal to GUI, file completed
                        del self.watch_list[full_filename]
            except RuntimeError:  # exception handling if dictionary changes value during iteration
                pass

    def file_process(self):
        """
        This function process files that are newly created.
        """
        global is_running
        # initiate file processor object
        processor = FileProcess.FileProcess()
        # while the program is running
        while is_running:
            # while there is a queue in queue_process
            while cfg.queue_process.qsize():
                try:
                    # retrieve full_filename (raw string literal) from queue_process
                    full_filename = cfg.queue_process.get()
                    # process the file with external module
                    processor.add(full_filename)
                except queue.Empty:
                    # just on general principles, although we don't
                    # expect this branch to be taken in this case
                    pass
        else:
            print('END thread 2', end='\n')
            return
