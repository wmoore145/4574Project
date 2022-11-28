
import PyQt6
import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QStackedWidget, QListWidget, QFormLayout, QHBoxLayout, QVBoxLayout, QRadioButton, QLabel, QCheckBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot

class BusinessWindow(QWidget):

    def viewAll(self):
        #needs to view all of the appointments the buisness has
        print("View button pressed")

    def creation(self):
        #needs to take this start and end times and create an appointment slot
        print("StartTime", self.createStartEntry.text())
        print("End Time", self.createEndEntry.text())

    def cancelation(self):
        #takes this start time and cancels the appointment with that start
        print("Start to cancel", self.cancelStartEntry.text())

    def __init__(self):
        super(BusinessWindow, self).__init__()
        self.setWindowTitle('Buisness Window')
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 300
        self.setGeometry(self.left, self.top, self.width, self.height)

        #### Setting welcome message
        name = "Buisness Name"
        fullName = "<h1>Welcome " + name + "</h1>"
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
        self.cancelStart = QLabel("Start Time to Cancel")
        self.cancelStartEntry = QLineEdit()
        
        self.cancelLayout = QHBoxLayout()
        self.cancelLayout.addWidget(self.cancelStart)
        self.cancelLayout.addWidget(self.cancelStartEntry)
        self.cancelLayout.addWidget(self.cancel)

        ######### Set connections
        self.viewButton = QPushButton("View Appointments")
        self.viewButton.clicked.connect(self.viewAll)
        self.createButton.clicked.connect(self.creation)
        self.cancel.clicked.connect(self.cancelation)
        
       ########## Set layout for whole window
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.viewButton)
        createDirection = QLabel("Fill in entries below and hit 'create' to create new appointment")
        self.layout.addWidget(createDirection)
        self.layout.addLayout(self.createLayout)
        cancelDirection = QLabel("Fill in start time of appointment to be canceled")
        self.layout.addWidget(cancelDirection)
        self.layout.addLayout(self.cancelLayout)

        self.setLayout(self.layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    widget = BusinessWindow()

    sys.exit(app.exec())
