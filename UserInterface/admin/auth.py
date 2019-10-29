from PyQt5 import QtWidgets
from datafed.CommandLib import loginByPassword, loginByToken
from config import cfg

class authDialog(QtWidgets.QApplication):
    def __init__(self):
        import sys
        super(authDialog, self).__init__(sys.argv)
        login = Login()
        login.show()
        self.exec_()  # execute the dialogue

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        authreg = QtWidgets.QWidget()
        formlayout = QtWidgets.QFormLayout(self)

        title_ID = QtWidgets.QLabel('User ID')
        title_pass = QtWidgets.QLabel('Password')
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)

        formlayout.addRow(title_ID, self.textName)
        formlayout.addRow(title_pass, self.textPass)
        authreg.setLayout(formlayout)

        layout.addWidget(authreg)
        layout.addWidget(self.buttonLogin)
        self.setLayout(layout)

    def handleLogin(self):
        try:
            if cfg.dev_user:  # for dev purposes
                self.textName.setText(cfg.dev_user[0])
                self.textPass.setText(cfg.dev_user[1])
            loginByPassword(str(self.textName.text()), str(self.textPass.text()))
            QtWidgets.QMessageBox.information(self, 'Welcome', 'Log-in Success!')
            cfg.user.addUser(self.textName.text())
            cfg.isConnected = True
            self.close()  # closing dialogue after successful log-in
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
