"""
Watcher User Interface
"""
# import standard lib
import tkinter as tk
import queue
import datetime as dt
# import local modules
import cfg

# setting flag for thread worker
is_running = True


class TicketScreen(tk.Frame):
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
        self.textVar.set('\n'*9)
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
        while cfg.queue_log.qsize():
            try:
                log = cfg.queue_log.get()
                # unpack tuple within the list
                full_filename, action = log
                # continue the process with updating display
                self.update_label(full_filename, action)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass
        # loop itself after 100ms interval
        self.update = self.master.after(100, self.process_templog)  # << Here, process_templog used to point directly to an object called "mainframe"

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
        global is_running
        # raises exit flag for thread
        is_running = False
        # cancel tk after
        self.master.after_cancel(self.update)
        # closes tk window
        self.master.destroy()
        # exit program
        exit()
