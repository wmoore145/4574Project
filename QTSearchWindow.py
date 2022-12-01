from msilib.schema import AppSearch
import random
import sys
import appSearch
from pymongo import MongoClient

from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QWidget, QComboBox)

   


class SearchWidget(QWidget):    #Search Window

    def concatBiz(self): #Take the list of buisnesses that are needed and convert them to a string
        buisnesses = ""
        for string in  self.biz:
            buisnesses = buisnesses + string

        return buisnesses

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

    def findResult(self):
        #go get the result from what you need
        result = appSearch.search( self.biz, self.col)
        self.resultBox.setText(result)

    def loginRefresh(self):
        query = self.col.find({})
        for appointment in query:
            if appointment["business"] not in self.businessList:
                self.businessList.append(appointment["business"])
        
        self.BusinessBox.clear()
        for name in self.businessList:
            self.BusinessBox.addItem(name)
        self.biz = []
        self.messageBox.setText("Buisnesses Selected: ")




    def __init__(self, client):
        
        QWidget.__init__(self)
        self.mongo_client = MongoClient('mongodb://localhost:27017')#assuming local database
        self.col  = self.mongo_client["appointment_user_data"]["appointment_list"]#database user_data and collection appointment_list
        self.client = client
        self.biz = []
        self.messageBox = QLabel()
        self.resultBox = QLabel()

        # Instructions
        self.businessList = []
        #query = self.col.find({})
        #for appointment in query:
        #    if appointment["business"] not in self.businessList:
        #        self.businessList.append(appointment["business"])

        #DropBox
        self.BusinessBox = QComboBox()
        #for name in self.businessList:
        #    self.BusinessBox.addItem(name)

        addButton = QPushButton(self)
        addButton.setText("Add/Remove")
        addButton.clicked.connect(self.BizAdd)

        helloMsg = QLabel("<h1>Select what you need.</h1>", self)
        
        #Keep updated what the user has selected
        message = "Buisnesses Selected: "
        bizneeded = self.concatBiz()
        fullMessage = message + bizneeded
        self.messageBox.setText(fullMessage)

        #Button starts the search
        searchButton = QPushButton(self)
        searchButton.setText("Search")
        searchButton.clicked.connect(self.findResult)

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
        self.layout.addWidget(searchButton)
        self.layout.addWidget(self.resultBox)
        self.layout.addWidget(self.logoutButton)
        self.setLayout(self.layout)  
        self.show()


        


if __name__ == "__main__":
    app = QApplication([])
    widget = SearchWidget()
    widget.setWindowTitle("PyQt App")
    widget.setGeometry(200,200,400,100)

    sys.exit(app.exec())
