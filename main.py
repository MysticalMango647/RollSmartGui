#For Gui
import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QIcon


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
        #gettingUserId=self.verifySignIn
        #print(gettingUserId)
        self.signInButton.clicked.connect(self.verifySignIn)

    def findNextScreenToLoad(self, userRole, userLocalId):
        print("in findNextScreenToLoad function")
        '''
        goToUserList = UserList(userLocalId)
        widget.addWidget(goToUserList)
        goToUserDashboard = UserDashboard(userLocalId)
        widget.addWidget(goToUserDashboard)
        print("added userlist and dashboard to widgets")
        '''
        if (userRole == "Practitioner"):
            # Go to UserList page(for Practitioner)
            print("role in nextscreenfunc. is prac.")
            self.loadUserList(userLocalId)

        elif (userRole == "User"):
            # Go to UserDashboard page(for Users)
            print("role in nextscreenfunc. is user")
            self.loadUserDashboard(userLocalId)

        else:
            print("Role is neither Prac. nor User")
            self.InvalidSignInAttempt.setText("Internal Error: User has no assigned role")


    def loadUserList(self, userLocalId):
        goToUserList = UserList(userLocalId)
        widget.addWidget(goToUserList)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loadUserDashboard(self, userLocalId):
        goToUserDashboard = UserDashboard(userLocalId)
        widget.addWidget(goToUserDashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def verifySignIn(self):
        Email = self.EmailEntry.text()
        Password = self.PasswordEntry.text()
        print(Email, Password)

        try:
            login = auth.sign_in_with_email_and_password(Email, Password)
            userInfo = auth.get_account_info(login['idToken'])
            userLocalId = userInfo['users'][0]['localId']
            print("The user local Id is: ", userLocalId)
            self.InvalidSignInAttempt.setText("")

            person = db.child("loginInfo").order_by_child("UID").equal_to(userLocalId).get().val().keys()
            accessingPerson = list(person)
            accessingPersonIs = str(accessingPerson[0])
            print("in main accessing person name is: ", accessingPersonIs)
            roleOfAccessingPersonIs = db.child("loginInfo").child(accessingPersonIs).child("role").get().val()
            print("role of: ", accessingPersonIs, "is: ", roleOfAccessingPersonIs)
            self.findNextScreenToLoad(roleOfAccessingPersonIs,userLocalId)

        except:
            self.InvalidSignInAttempt.setText("Invalid Email or Password")


class UserList(QDialog):
    def __init__(self, userId):
        super(UserList, self).__init__()
        loadUi("UserList.ui", self)
        print("in userlist class init function")
        self.userId = userId
        findWhoUserIs = self.getNamefromUID(userId)
        WelcomeString = str("Welcome, Dr. " + findWhoUserIs)
        self.WelcomeName.setText(WelcomeString)

        self.UserListTable.setColumnWidth(0,400)
        self.UserListTable.setColumnWidth(1,400)
        self.UserListTable.setColumnWidth(2,190)
        self.fillUserTableInfo()

    def fillUserTableInfo(self):
        allUserInfo = db.child("loginInfo").get().val()
        print(db.child("loginInfo").get().val())
        elementRow = 0
        print("the length of alluserInfo is: ", len(allUserInfo))
        self.UserListTable.setRowCount(len(allUserInfo))
        for key, val in allUserInfo.items():
            print(key)
            print(val.get('DOB'))
            selectedUID=val.get('UID')
            self.UserListTable.setItem(elementRow, 0, QtWidgets.QTableWidgetItem(str(key)))
            self.UserListTable.setItem(elementRow, 1, QtWidgets.QTableWidgetItem(str(val.get('DOB'))))
            elementRow = elementRow + 1
        return

    def loadUserDashboard(self, userLocalId):
        goToUserDashboard = UserDashboard(userLocalId)
        widget.addWidget(goToUserDashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def getNamefromUID(self, userId):
        # self.login = login
        # self.db = db

        # allLoginInfo = db.child("loginInfo").get()
        # print(allLoginInfo.val())
        # self.getNamefromUID()
        '''
        allLoginInfo = db.child("loginInfo").get()
        allLoginInfoWithVal = allLoginInfo.val()
        print(allLoginInfo.val())

        for userInfo in allLoginInfoWithVal:
            print(userInfo.child().get().val())

            if userInfo['UID'] == userLocalId:
                print(userInfo)

            else:
                pass


        allLoginInfo = db.child("loginInfo").get()
        allLoginInfoWithVal = allLoginInfo.val()
        print(allLoginInfoWithVal)
        '''
        print("in getNamefromUID fucntion")
        person = db.child("loginInfo").order_by_child("UID").equal_to(userId).get().val().keys()
        accessingPerson = list(person)
        accessingPersonName = accessingPerson[0]
        print(accessingPerson)
        return(accessingPersonName)





class UserDashboard(QDialog):
    def __init__(self, userId):
        super(UserDashboard, self).__init__()
        loadUi("UserDashboard.ui", self)
        self.userId = userId
        print("in UserDashboard class")

app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.setWindowIcon(QIcon('projectIcon.jpg'))
widget.setWindowTitle("RollSmart")
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")



'''
Refrences Used for this project.

Login in Screen and General PyQt5 Walkthrough were used from 
https://www.youtube.com/@codefirstwithhala
Most concepts are derived from Hala and expanded upon.

'''