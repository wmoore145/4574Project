from msilib.schema import AppSearch
import random
import sys
import appSearch

from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QWidget, QComboBox)

   


class SearchWidget(QWidget):    #Search Window

    def concatBiz(bizness): #Take the list of buisnesses that are needed and convert them to a string
        buisnesses = ""
        for string in biz:
            buisnesses = buisnesses + string

        return buisnesses

    def BizA(self): #Slot from button A, changes the biz list and updates the label

        if "A" not in biz:
            biz.append("A")
        else:
            biz.remove("A")

        bizneeded = self.concatBiz()
        message = "Buisnesses Selected: "
        fullMessage = message + bizneeded
        messageBox.setText(fullMessage)
        
    def BizB(self):

        if "B" not in biz:
            biz.append("B")
        else:
            biz.remove("B")

        bizneeded = self.concatBiz()
        message = "Buisnesses Selected: "
        fullMessage = message + bizneeded
        messageBox.setText(fullMessage)
        
    def BizC(self):

        if "C" not in biz:
            biz.append("C")
        else:
            biz.remove("C")

        bizneeded = self.concatBiz()
        message = "Buisnesses Selected: "
        fullMessage = message + bizneeded
        messageBox.setText(fullMessage)     

    def BizAdd(self):

        currentBiz = self.BusinessBox.currentText()

        if currentBiz not in biz:
            biz.append(currentBiz)
        else:
            biz.remove(currentBiz)

        bizneeded = self.concatBiz()
        message = "Buisnesses Selected: "
        fullMessage = message + bizneeded
        messageBox.setText(fullMessage)     

    def findResult(self):

        #go get the result from what you need
        result = appSearch.search(biz)
        resultBox.setText(result)


    def __init__(self, biz, messageBox, resultBox):
        
        QWidget.__init__(self)

        # Instructions
        businessList = ['A', 'B', 'C']
        #DropBox
        self.BusinessBox = QComboBox()
        for name in businessList:
            self.BusinessBox.addItem(name)

        addButton = QPushButton(self)
        addButton.setText("Add")
        addButton.clicked.connect(self.BizAdd)

        helloMsg = QLabel("<h1>Select what you need.</h1>", self)
        
        #Keep updated what the user has selected
        message = "Buisnesses Selected: "
        bizneeded = self.concatBiz()
        fullMessage = message + bizneeded
        messageBox.setText(fullMessage)

        #Button starts the search
        searchButton = QPushButton(self)
        searchButton.setText("Search")
        searchButton.clicked.connect(self.findResult)

     
        #adding everything to the layout
        layout = QVBoxLayout()
        sublayout = QHBoxLayout()

        layout.addWidget(helloMsg)
        layout.addLayout(sublayout)

        layout.addWidget(messageBox)

        layout.addWidget(self.BusinessBox)
        layout.addWidget(addButton)
        layout.addWidget(searchButton)
        layout.addWidget(resultBox)
        self.setLayout(layout)  
        self.show()


        


if __name__ == "__main__":
    app = QApplication([])
    biz = []
    messageBox = QLabel()
    resultBox = QLabel()
    widget = SearchWidget(biz, messageBox, resultBox)
    widget.setWindowTitle("PyQt App")
    widget.setGeometry(200,200,400,100)

    sys.exit(app.exec())