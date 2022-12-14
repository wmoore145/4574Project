#!/usr/bin/env python3
# client.py
# ECE4574 FA22 Appointment Scheduler Nov. 28, 2022
# Sam Stewart
# This is the main startup file for the project
import login
import QTSearchWindow
import businessWindow

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QStackedWidget, QFormLayout, QHBoxLayout, QCheckBox
from PyQt6.QtCore import pyqtSlot



class App(QWidget):
    #Inits all the windows
    def __init__(self):
        super(App, self).__init__()

        self.username_text = ""

        self.loginwindow = QWidget()
        self.initLoginPage()
        self.registrationwindow = QWidget()
        self.initRegistrationPage()
    
        
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget (self.loginwindow)#index 0
        self.Stack.addWidget (self.registrationwindow)#index 1
        self.searchwindow = QTSearchWindow.SearchWidget(self)
        self.Stack.addWidget (self.searchwindow)#index 2
        self.businesswindow = businessWindow.BusinessWindow(self)
        self.Stack.addWidget (self.businesswindow)#index 3


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

    #REGISTRATION WINDOW
    def initRegistrationPage(self): 
        layout = QFormLayout()
    
        # Create username textbox
        self.rusername = QLineEdit()
        layout.addRow("Username", self.rusername)

        # Create password textbox
        self.rpassword = QLineEdit()
        layout.addRow("Password", self.rpassword)

        # Create address textbox
        #self.raddress = QLineEdit()
        #layout.addRow("Address", self.raddress)

        self.business_option = QCheckBox("Business?")
        layout.addRow("",self.business_option)

        # button for attempting to register
        register_button = QPushButton('Register')
        register_button.clicked.connect(self.register_click)

        # button for return to login
        to_login_button = QPushButton('Return to Login')
        to_login_button.clicked.connect(self.to_login)

        # button setup
        layout.addRow("", register_button)
        layout.addRow("", to_login_button)

        self.registrationwindow.setLayout(layout)
    
    #LOGIN WINDOW
    def initLoginPage(self): 
        layout = QFormLayout()
    
        # Create textbox
        self.username = QLineEdit()
        layout.addRow("Username", self.username)

        # Create textbox
        self.password = QLineEdit()
        layout.addRow("Password", self.password)

        # button to login
        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login_click)

        # button to navigate to registration page
        registeration_button = QPushButton('Register')
        registeration_button.clicked.connect(self.registration_click)

        # button setup
        buttons = QHBoxLayout()
        buttons.addWidget(login_button)
        buttons.addWidget(registeration_button)
        layout.addRow("", buttons)

        self.loginwindow.setLayout(layout)

    #When login button clicked
    @pyqtSlot()
    def login_click(self):
        username = self.username.text()
        password = self.password.text()
        if login.login(username, password):
            self.username_text = username
            if login.isBusiness(username):
                self.businesswindow.loginRefresh()
                self.Stack.setCurrentIndex(3)#switches page to business window
            else:
                self.searchwindow.loginRefresh()
                self.Stack.setCurrentIndex(2)#switches page to search
        else:
            QMessageBox.question(self, 'Failed Login', "Incorrect Username or Password Provided")

    #When to registration page clicked on login
    @pyqtSlot()
    def registration_click(self):
        self.rusername.clear()
        self.rpassword.clear()
        self.Stack.setCurrentIndex(1)#switches page to register

    #When on registration page and clicks register
    @pyqtSlot()
    def register_click(self):
        username = self.rusername.text()
        password = self.rpassword.text()
        #address = self.raddress.text()
        business = self.business_option.isChecked()
        if username == "" or username == "NONE":
            QMessageBox.question(self, 'Failed Registration', "Invalid Username")
            return
        account_type = 'private'
        if business:
            account_type = 'business'
        if login.register(username, password, account_type):#, address):
            self.username_text = username
            if business:
                self.businesswindow.loginRefresh()
                self.Stack.setCurrentIndex(3)#switches page to business window
            else:
                self.searchwindow.loginRefresh()
                self.Stack.setCurrentIndex(2)#switches page to search
        else:
            QMessageBox.question(self, 'Failed Registration', "Username Already Taken")

    #When clicks return to login
    @pyqtSlot()
    def to_login(self):
        self.password.clear()
        self.Stack.setCurrentIndex(0)#switches page to login

#Starts up app and goes
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())