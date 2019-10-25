import MainWindow
from Admin import auth as AdminAuth

if __name__ == '__main__':
    import datafed.CommandLib as datafed
    from PyQt5 import QtWidgets
    import sys

    auth, uid = datafed.init()  # initiate datafed connection
    print('Authentication status: ', auth, uid)
    AdminAuth.authDialog()  # open authentication dialogue


