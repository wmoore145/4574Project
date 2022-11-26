import login
import QTSearchWindow
import PyQt6

import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QStackedWidget, QListWidget, QFormLayout, QHBoxLayout, QRadioButton, QLabel, QCheckBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot



class App(QWidget):
    def __init__(self):
        super(App, self).__init__()

        self.loginwindow = QWidget()
        self.initLoginPage()
        self.registrationwindow = QWidget()
        self.initRegistrationPage()
        self.searchwindow = QTSearchWindow.SearchWidget()
#TO ADD NEW WINDOWS ADD HERE WITH 'self.YOURWIDGETNAME' AND YOUR WIDGET'S CONSTRUCTOR, THEN 'self.Stack.addWidget (self.YOURWIDGETNAME)' TO END OF LIST BELOW, KEEP IN MIND ITS INDEX

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget (self.loginwindow)#index 0
        self.Stack.addWidget (self.registrationwindow)#index 1
        self.Stack.addWidget (self.searchwindow)#index 2

#FOR NAVIGATION ADD BUTTON THAT CALLS self.Stack.setCurrentIndex(YOUR_DESIRED_INDEX)


        hbox = QHBoxLayout(self)
        hbox.addWidget(self.Stack)
        self.setLayout(hbox)

        self.Stack.setCurrentIndex(0)
        

        self.setWindowTitle('4574 Scheduler')
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 300
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def initRegistrationPage(self): #REGISTRATION WINDOW
        layout = QFormLayout()
    
        # Create textbox
        self.rusername = QLineEdit()
        layout.addRow("Username", self.rusername)

        # Create textbox
        self.rpassword = QLineEdit()
        layout.addRow("Password", self.rpassword)

        self.business_option = QCheckBox("Business?")
        layout.addRow("",self.business_option)

        # make and connect button to function on_click
        register_button = QPushButton('Register')
        register_button.clicked.connect(self.register_click)

        # button setup
        layout.addRow("", register_button)

        self.registrationwindow.setLayout(layout)
    
    def initLoginPage(self): #LOGIN WINDOW
        layout = QFormLayout()
    
        # Create textbox
        self.username = QLineEdit()
        layout.addRow("Username", self.username)

        # Create textbox
        self.password = QLineEdit()
        layout.addRow("Password", self.password)

        # make and connect button to function on_click
        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login_click)

        # make and connect button to function on_click
        registeration_button = QPushButton('Register')
        registeration_button.clicked.connect(self.registration_click)

        # button setup
        buttons = QHBoxLayout()
        buttons.addWidget(login_button)
        buttons.addWidget(registeration_button)
        layout.addRow("", buttons)

        self.loginwindow.setLayout(layout)

    @pyqtSlot()
    def login_click(self):
        username = self.username.text()
        password = self.password.text()
        if login.login(username, password):
            self.Stack.setCurrentIndex(2)#switches page to search
        else:
            QMessageBox.question(self, 'Failed Login', "Incorrect username or password provided")

    @pyqtSlot()
    def registration_click(self):
        self.Stack.setCurrentIndex(1)#switches page to register

    @pyqtSlot()
    def register_click(self):
        username = self.rusername.text()
        password = self.rpassword.text()
        business = self.business_option
        account_type = 'private'
        if business:
            account_type = 'business'
        if login.register(username, password, account_type):
            self.Stack.setCurrentIndex(2)#switches page to search
        else:
            QMessageBox.question(self, 'Failed Registration', "Username already taken")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())