#For Gui
import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QDialog, QApplication, QWidget


#For Firebase
import pyrebase

#KeyConfig
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

#Establish User
global userLocalId


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("IntroScreen.ui",self)
        self.PasswordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        gettingUserId=self.verifySignIn
        self.signInButton.clicked.connect(gettingUserId)

    def verifySignIn(self):
        Email = self.EmailEntry.text()
        Password = self.PasswordEntry.text()
        #print(Email, Password)

        try:
            login = auth.sign_in_with_email_and_password(Email, Password)
            userInfo = auth.get_account_info(login['idToken'])
            userLocalId = userInfo['users'][0]['localId']
            print("The user local Id is: ", userLocalId)
            self.InvalidSignInAttempt.setText("")
            goToUserList = UserList(userLocalId, login, db)
            widget.addWidget(goToUserList)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except:
            self.InvalidSignInAttempt.setText("Invalid Email or Password")


class UserList(QDialog):
    def __init__(self, userId, login, db):
        super(UserList, self).__init__()
        loadUi("UserList.ui", self)
        print("in userlist class init function")
        self.userId = userId
        #self.login = login
        #self.db = db
        self.WelcomeName.setText("Welcome, UserXYZ")
        #allLoginInfo = db.child("loginInfo").get()
        #print(allLoginInfo.val())
        #self.getNamefromUID()
        allLoginInfo = db.child("loginInfo").get()
        allLoginInfoWithVal = allLoginInfo.val()
        print(allLoginInfo.val())

        for userInfo in allLoginInfoWithVal:
            print(userInfo.child().get().val())
            '''
            if userInfo['UID'] == userLocalId:
                print(userInfo)
                print("Hello corbin")
            else:
                pass
            '''


    def getNamefromUID(self):
        print("in getNamefromUID fucntion")
        loadUi("UserDashboard.ui", self)

        return

class UserDashboard(QDialog):
    def __init__(self):
        super(UserDashboard, self).__init__()

app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)

widget.setFixedHeight(800)
widget.setFixedWidth(1200)
#widget.setWindowIcon(QIcon('projectIcon.jpg'))
widget.setWindowTitle("Roll Smart")
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")