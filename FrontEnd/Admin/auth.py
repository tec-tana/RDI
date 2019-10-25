from PyQt5 import QtWidgets
from datafed.CommandLib import loginByPassword, loginByToken

class authDialog(QtWidgets.QApplication):
    def __init__(self):
        import sys
        super(authDialog, self).__init__(sys.argv)
        login = Login()
        login.show()
        sys.exit(self.exec_())

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        title_ID = QtWidgets.QLabel('User ID')
        title_pass = QtWidgets.QLabel('Password')
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QFormLayout(self)
        layout.addRow(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        try:
            loginByPassword(self.textName.text(), self.textPass.text())
            QtWidgets.QMessageBox.information(self, 'Welcome', 'Log-in Success!')
            sys.exit(app.exec_())  # closing dialogue after successful log-in
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
