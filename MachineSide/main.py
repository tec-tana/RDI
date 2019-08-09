# import standard lib
import tkinter as tk
# import local modules
from DirectoryWorker.SignalProcess import SignalWatch
from DirectoryWorker.WatcherUI import TicketScreen

if __name__ == '__main__':
    # Set test path
    TEST_PATH1 = r'C:\Users\Tanat\Desktop\test1'
    TEST_PATH2 = r'C:\Users\Tanat\Desktop\test2'

    root = tk.Tk()
    root.title("Directory Watch")
    root.geometry("500x220")  # set default window geometry
    root.resizable(0, 0)  # prevent resizing in the x or y directions
    mainframe = TicketScreen(root)  # initiate GUI
    watcher1 = SignalWatch(TEST_PATH1)  # initialize DirectoryWorker 1
    watcher2 = SignalWatch(TEST_PATH2)  # initialize DirectoryWorker 2
    root.after(100, mainframe.process_templog)  # update GUI at 100ms intervals
    root.mainloop()