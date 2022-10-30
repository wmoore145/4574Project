from msilib.schema import AppSearch
import random
import sys
import appSearch

from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QWidget)

   


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

    def findResult(self):

        #go get the result from what you need
        result = appSearch.search(biz)
        resultBox.setText(result)


    def __init__(self, biz, messageBox, resultBox):
        
        QWidget.__init__(self)
        # Instructions
        helloMsg = QLabel("<h1>Select what you need.</h1>", self)
        
        #Keep updated what the user has selected
        message = "Buisnesses Selected: "
        bizneeded = self.concatBiz()
        fullMessage = message + bizneeded
        messageBox.setText(fullMessage)

        #Buttons are simply for examples, we will need to do a drop down menu or something else for selection
        #Preparing the buttons
        button1 = QPushButton(self)
        button1.setText("Buisness A")
        button1.clicked.connect(self.BizA)

        button2 = QPushButton(self)
        button2.setText("Buisness B")
        button2.clicked.connect(self.BizB)

        button3 = QPushButton(self)
        button3.setText("Buisness C")
        button3.clicked.connect(self.BizC)


        #Button starts the search
        searchButton = QPushButton(self)
        searchButton.setText("Search")
        searchButton.clicked.connect(self.findResult)

     
        #adding everything to the layout
        layout = QVBoxLayout()
        sublayout = QHBoxLayout()
        sublayout.addWidget(button1)
        sublayout.addWidget(button2)
        sublayout.addWidget(button3)
        layout.addWidget(helloMsg)
        layout.addLayout(sublayout)

        layout.addWidget(messageBox)
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
    widget.setGeometry(100,100,280,80)

    sys.exit(app.exec())