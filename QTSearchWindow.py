# QTSearchWIndow.py 
# ECE4574 FA22 Appointment Scheduler Nov. 28, 2022
# Sam Stewart, William Moore
# This handles the customer's window view and functionality
from msilib.schema import AppSearch
import sys
import appSearch
from pymongo import MongoClient
from bson.objectid import ObjectId

import PyQt6
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QLineEdit, QComboBox)
from PyQt6.QtCore import pyqtSlot
   


class SearchWidget(QWidget):    #Search Window

    #Take the list of buisnesses that are needed and convert them to a string
    def concatBiz(self): 
        buisnesses = ""
        for string in  self.biz:
            buisnesses = buisnesses + string + " "

        return buisnesses

    #Adds a business to the display of selected businesses
    def BizAdd(self):

        currentBiz = self.BusinessBox.currentText()

        if currentBiz not in  self.biz:
             self.biz.append(currentBiz)
        else:
             self.biz.remove(currentBiz)

        bizneeded = self.concatBiz()
        message = "Buisnesses Selected: "
        fullMessage = message + bizneeded
        self.messageBox.setText(fullMessage)     

    #Cancels an appointment
    def cancelation(self):
        try:
            self.col.update_one({'_id': ObjectId(self.cancelStartEntry.text())},{'$set': {'apointee': "NONE"}}, upsert=False)
        except:
            self.cancelStartEntry.clear()
            return
        self.cancelStartEntry.clear()
       
    #Runs search algorithm for appointments and formats response
    def findResult(self):
        result = appSearch.search( self.biz, self)
        self.toBook = result.copy()

        resultStr = ""
        
        for appmnt in result:

            resultStr += appmnt[0]
            resultStr += ": " 
            resultStr += str(appmnt[1])
            resultStr += " - "
            resultStr += str(appmnt[2])
            resultStr += "\n"
           
        if resultStr == "":
            resultStr = "No Compatable Appointments Found"

        self.resultBox.setText(resultStr)

    #Refreshes details and page upon being sent to this page, used to keep different user's data from staying for current user's login
    def loginRefresh(self):
        query = self.col.find({})
        for appointment in query:
            if appointment["business"] not in self.businessList:
                self.businessList.append(appointment["business"])
        
        self.searchStartEntry.setText("0")
        self.searchEndEntry.setText("24")
        self.cancelStartEntry.setText("")
        self.resultBox.setText("")
        self.toBook = []
        self.BusinessBox.clear()
        for name in self.businessList:
            self.BusinessBox.addItem(name)
        self.biz = []
        self.messageBox.setText("Buisnesses Selected: ")

    #Initializes the client's window
    def __init__(self, client):
        
        QWidget.__init__(self)
        self.mongo_client = MongoClient('mongodb://localhost:27017')#assuming local database
        self.col  = self.mongo_client["appointment_user_data"]["appointment_list"]#database user_data and collection appointment_list
        self.client = client
        self.toBook = []
        self.biz = []
        self.messageBox = QLabel()
        self.resultBox = QLabel()

        # Instructions
        self.businessList = []

        #DropBox
        self.BusinessBox = QComboBox()

        addButton = QPushButton(self)
        addButton.setText("Add/Remove")
        addButton.clicked.connect(self.BizAdd)

        helloMsg = QLabel("<h1>Select what you need.</h1>", self)
        
        #Keep updated what the user has selected
        message = "Buisnesses Selected: "
        bizneeded = self.concatBiz()
        fullMessage = message + bizneeded
        self.messageBox.setText(fullMessage)

        self.searchStart = QLabel("Start Time:")
        self.searchStartEntry = QLineEdit()
        self.searchEnd = QLabel("End Time:")
        self.searchEndEntry = QLineEdit()

        timesLayout = QHBoxLayout()
        timesLayout.addWidget(self.searchStart)
        timesLayout.addWidget(self.searchStartEntry)
        timesLayout.addWidget(self.searchEnd)
        timesLayout.addWidget(self.searchEndEntry)

        #Button starts the search
        searchButton = QPushButton(self)
        searchButton.setText("Search")
        searchButton.clicked.connect(self.findResult)

        bookButton = QPushButton("Book")
        bookButton.clicked.connect(self.bookAppointment)
        bookLayout = QHBoxLayout()
        bookLayout.addWidget(self.resultBox)
        bookLayout.addWidget(bookButton)

        viewButton = QPushButton("View Booked")
        cancelButton = QPushButton("Cancel Appointment")
        self.cancelStart = QLabel("Appointment ID to Cancel")
        self.cancelStartEntry = QLineEdit()

        cancelButton.clicked.connect(self.cancelation)
        
        self.cancelLayout = QHBoxLayout()
        self.cancelLayout.addWidget(self.cancelStart)
        self.cancelLayout.addWidget(self.cancelStartEntry)
        self.cancelLayout.addWidget(cancelButton)

        viewButton.clicked.connect(self.viewAppointments)

        # Logout Button
        self.logoutButton = QPushButton("Logout")
        self.logoutButton.clicked.connect(self.client.to_login)
     
        #adding everything to the layout
        self.layout = QVBoxLayout()
        sublayout = QHBoxLayout()

        self.layout.addWidget(helloMsg)
        self.layout.addLayout(sublayout)

        self.layout.addWidget(self.messageBox)

        self.layout.addWidget(self.BusinessBox)
        self.layout.addWidget(addButton)
        self.layout.addLayout(timesLayout)
        self.layout.addWidget(searchButton)
        self.layout.addLayout(bookLayout)
        self.layout.addWidget(viewButton)
        self.layout.addLayout(self.cancelLayout)
        self.layout.addWidget(self.logoutButton)
        self.setLayout(self.layout)  
        self.show()

    #Marks each selected appointment as taken
    @pyqtSlot()
    def bookAppointment(self):
        
        for apointment in self.toBook:
            self.col.update_one({'_id': ObjectId(apointment[3])},{'$set': {'apointee': self.client.username_text}}, upsert=False)
        
    #When returning to this window cleans up appointmnet viewing window for next time
    def endViewAll(self):
        self.client.Stack.setCurrentIndex(2)
        self.client.Stack.removeWidget(self.appointment_window)#removes widget to view appointments
        self.appointment_window.deleteLater()
        self.appointment_window = None

    #Opens viewing window to see customer's appointments
    @pyqtSlot()
    def viewAppointments(self):
        query = self.col.find({"apointee": self.client.username_text})
        self.appointment_window = ViewAppointmentsPrivate(self, query)
        pos = self.client.Stack.addWidget (self.appointment_window)
        self.client.Stack.setCurrentIndex(pos)#switches page to view appointments
        


if __name__ == "__main__":
    app = QApplication([])
    widget = SearchWidget()
    widget.setWindowTitle("PyQt App")
    widget.setGeometry(200,200,400,100)

    sys.exit(app.exec())


#View Window Class, For Viewing Appointments
class ViewAppointmentsPrivate(QWidget):

    def __init__(self, parent, query):
        super(ViewAppointmentsPrivate, self).__init__()
        self.layout = QVBoxLayout()
        for appointment in query:
            info = QLabel("Start Time: " + str(appointment["start_time"]) + "   End Time: " + str(appointment["end_time"]) + "   Business: " + str(appointment["business"]) + "   ID: " + str(appointment["_id"]))
            info.setTextInteractionFlags(PyQt6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
            self.layout.addWidget(info)        
        
        ######### Logout Button
        returnButton = QPushButton("Return")
        returnButton.clicked.connect(parent.endViewAll)
        self.layout.addWidget(returnButton)

        self.setLayout(self.layout)
        self.show