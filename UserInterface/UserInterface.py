import sys
import datafed.CommandLib as datafed
from admin import auth as AdminAuth
from layout import main
from config import cfg

if __name__ == '__main__':
    auth, uid = datafed.init()  # initiate datafed connection
    print('Authentication status: ', auth, uid)

    AdminAuth.authDialog()  # open authentication dialogue
    if cfg.isConnected is False: exit()  # exit if authentication was bypassed
    else:
        try:
            cfg.user.update_ownership()  # update project and collection owned by the user
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e))
            exit()
    print('User(s) logged-in: ', cfg.user._userinfo['name'])
    if cfg.user._userinfo['name']:  # if a user is signed up
        sys.exit(main.UI())

