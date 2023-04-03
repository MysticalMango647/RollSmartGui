# For Firebase
import pyrebase
import pyqtgraph as pg
import numpy as np

# For Gui
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication


# FireBase KeyConfig
config = {
    'apiKey': "AIzaSyB8YyKlyoarYSiAfS6ZpbmfFHmW5xLIhYg",
    'authDomain': "sysc4907rollsmart.firebaseapp.com",
    'databaseURL': "https://sysc4907rollsmart-default-rtdb.firebaseio.com",
    'projectId': "sysc4907rollsmart",
    'storageBucket': "sysc4907rollsmart.appspot.com",
    'messagingSenderId': "937699780579",
    'appId': "1:937699780579:web:c626a608dc7a2f0b51a2d6",
    'measurementId': "G-HHFNCNF4NP"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

class OutputGraph(QDialog):
    def __init__(self):
        super(OutputGraph, self).__init__()
        loadUi("OutputGraph.ui", self)
        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        pg.plot(x, y, pen=None, symbol='o')


class GraphSelectionScreen(QDialog):
    def __init__(self):
        super(GraphSelectionScreen, self).__init__()
        loadUi("Graph.ui", self)
        self.SucessSubmitted.setText("Not Submitted")
        #self.SubmitButton.clicked.connect(self.submitPressed)



# main
app = QApplication(sys.argv)
GraphSelectionPage = GraphSelectionScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(GraphSelectionPage)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
#widget.setWindowIcon(QIcon('projectIcon.jpg'))
widget.setWindowTitle("Roll Smart")
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

