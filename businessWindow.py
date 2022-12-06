# businessWindow.py
# ECE4574 FA22 Appointment Scheduler Nov. 28, 2022
# Sam Stewart, William Moore
# This handles the business' window view and all functionality
import PyQt6
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel


class BusinessWindow(QWidget):

    #Switches to view window
    def viewAll(self):
        #needs to view all of the appointments the buisness has
        query = self.col.find({"business": self.client.username_text})
        self.appointment_window = ViewAppointmentsBusiness(self, query)
        pos = self.client.Stack.addWidget (self.appointment_window)
        self.client.Stack.setCurrentIndex(pos)#switches page to view appointments

    #Creates an appointment
    def creation(self):
        self.col.insert_one({"business": self.client.username_text, "start_time": self.createStartEntry.text(), "end_time": self.createEndEntry.text(), "apointee": "NONE"})
        self.createStartEntry.clear()
        self.createEndEntry.clear()

    #Deletes an appointment
    def cancelation(self):
        #takes this start time and cancels the appointment with that start
        try:
            query = self.col.find_one({'_id': ObjectId(self.cancelStartEntry.text())})
        except:
            self.cancelStartEntry.clear()
            return
        if query is None:
            self.cancelStartEntry.clear()
            return
        self.col.delete_one({'_id': ObjectId(self.cancelStartEntry.text())})
        self.cancelStartEntry.clear()

    #When returning to this window cleans up appointmnet viewing window for next time
    def endViewAll(self):
        self.client.Stack.setCurrentIndex(3)
        self.client.Stack.removeWidget(self.appointment_window)#removes widget to view appointments
        self.appointment_window.deleteLater()
        self.appointment_window = None

    ##Refreshes details and page upon being sent to this page, used to keep different user's data from staying for current user's login
    def loginRefresh(self):
        self.cancelStartEntry.clear()

    #Initializes the business window
    def __init__(self, client):
        super(BusinessWindow, self).__init__()
        self.mongo_client = MongoClient('mongodb://localhost:27017')#assuming local database
        self.col  = self.mongo_client["appointment_user_data"]["appointment_list"]#database user_data and collection appointment_list
        self.client = client
        
        self.setWindowTitle('Buisness Window')
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 300
        self.setGeometry(self.left, self.top, self.width, self.height)

        #### Setting welcome message
        
        fullName = "<h1>Welcome</h1>"
        self.name =  QLabel(fullName)

        ######## Setting the creation layout
        
        self.createStart = QLabel("Start Time:")
        self.createStartEntry = QLineEdit()
        self.createEnd = QLabel("End Time:")
        self.createEndEntry = QLineEdit()
        self.createButton = QPushButton("Create")

        self.createLayout = QHBoxLayout()
        self.createLayout.addWidget(self.createStart)
        self.createLayout.addWidget(self.createStartEntry)
        self.createLayout.addWidget(self.createEnd)
        self.createLayout.addWidget(self.createEndEntry)
        self.createLayout.addWidget(self.createButton)

        ####### Setting Cancel layout
        self.cancel = QPushButton("Cancel")
        self.cancelStart = QLabel("Appointment ID to Cancel")
        self.cancelStartEntry = QLineEdit()
        
        self.cancelLayout = QHBoxLayout()
        self.cancelLayout.addWidget(self.cancelStart)
        self.cancelLayout.addWidget(self.cancelStartEntry)
        self.cancelLayout.addWidget(self.cancel)

        ######### Set connections
        self.viewButton = QPushButton("View Your Business' Appointments")
        self.viewButton.clicked.connect(self.viewAll)
        self.createButton.clicked.connect(self.creation)
        self.cancel.clicked.connect(self.cancelation)

        ######### Logout Button
        self.logoutButton = QPushButton("Logout")
        self.logoutButton.clicked.connect(self.client.to_login)
        
       ########## Set layout for whole window
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.viewButton)
        createDirection = QLabel("Fill in entries below and hit 'create' to create new appointment")
        self.layout.addWidget(createDirection)
        self.layout.addLayout(self.createLayout)
        cancelDirection = QLabel("Fill in ID of appointment to be canceled")
        self.layout.addWidget(cancelDirection)
        self.layout.addLayout(self.cancelLayout)
        self.layout.addWidget(self.logoutButton)

        self.setLayout(self.layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    widget = BusinessWindow()

    sys.exit(app.exec())

#View Window Class, For Viewing Appointments
class ViewAppointmentsBusiness(QWidget):

    def __init__(self, parent, query):
        super(ViewAppointmentsBusiness, self).__init__()
        self.layout = QVBoxLayout()
        for appointment in query:
            info = QLabel("Start Time: " + str(appointment["start_time"]) + "   End Time: " + str(appointment["end_time"]) + "   Apointee: " + str(appointment["apointee"]) + "   ID: " + str(appointment["_id"]))
            info.setTextInteractionFlags(PyQt6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
            self.layout.addWidget(info)        
        
        ######### Logout Button
        returnButton = QPushButton("Return")
        returnButton.clicked.connect(parent.endViewAll)
        self.layout.addWidget(returnButton)

        self.setLayout(self.layout)
        self.show