#For Gui
import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget, QRadioButton, QTableWidgetItem, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import *
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
        #print("in findNextScreenToLoad function")
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
            personIsPractitioner = False
            self.loadUserDashboard(userLocalId, personIsPractitioner)

        else:
            print("Role is neither Prac. nor User")
            self.InvalidSignInAttempt.setText("Internal Error: User has no assigned role")


    def loadUserList(self, userLocalId):
        goToUserList = UserList(userLocalId)
        widget.addWidget(goToUserList)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loadUserDashboard(self, userLocalId, personIsPractitioner):
        goToUserDashboard = UserDashboard(userLocalId, personIsPractitioner)
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
            #print("in main accessing person name is: ", accessingPersonIs)
            roleOfAccessingPersonIs = db.child("loginInfo").child(accessingPersonIs).child("role").get().val()
            #print("role of: ", accessingPersonIs, "is: ", roleOfAccessingPersonIs)
            self.findNextScreenToLoad(roleOfAccessingPersonIs,userLocalId)

        except:
            self.InvalidSignInAttempt.setText("Invalid Email or Password")


class UserList(QDialog):
    def __init__(self, userId):
        super(UserList, self).__init__()
        loadUi("UserList.ui", self)
        self.userId = userId
        global UserUIDtoView
        findWhoUserIs = self.getNamefromUID(userId)
        WelcomeString = str("Welcome, Dr. " + findWhoUserIs)
        self.WelcomeName.setText(WelcomeString)
        self.UserListTable.setColumnWidth(0,400)
        self.UserListTable.setColumnWidth(1,300)
        self.UserListTable.setColumnWidth(2,280)
        self.loadUserTableInfo()

    def loadUserTableInfo(self):
        allUserInfo = db.child("loginInfo").get().val()
        #print(db.child("loginInfo").get().val())
        elementRow = 0
        numberofUsers = len(list(db.child("loginInfo").order_by_child("role").equal_to("User").get().val().keys()))
        #print(numberofUsers)
        self.UserListTable.setRowCount(numberofUsers)
        #getPractitionersUserSelection =
        self.UserListTable.selectionModel().selectionChanged.connect(self.selectionMade)

        #self.signInButton.clicked.connect(self.verifyUserSelectionDoneProperly())

        for key, val in allUserInfo.items():
            #print(key)
            #print(val.get('DOB'))
            selectedUID=val.get('UID')
            #Only display Users, no practitioners in the list of users
            if (val.get('role') != "Practitioner"):
                self.UserListTable.setItem(elementRow, 0, QtWidgets.QTableWidgetItem(str(key)))
                self.UserListTable.setItem(elementRow, 1, QtWidgets.QTableWidgetItem(str(val.get('DOB'))))
                self.UserListTable.setItem(elementRow, 2, QtWidgets.QTableWidgetItem(str(val.get('UID'))))
                elementRow = elementRow + 1

                '''Was trying to add radio button here instead, but it wasn't working out'''
                #userSelectRadioButton = QtWidgets.QRadioButton(str(val.get('UID')))
                #userSelectRadioButton.setChecked(False)
                #self.UserListTable.setItem(elementRow, 2, QtWidgets.QTableWidgetItem(userSelectRadioButton))


                '''was Experimenting with check box for col 2, select user'''
                '''
                chkBoxItem = QTableWidgetItem(selectedUID)
                chkBoxItem.setText(str(selectedUID))
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                self.ui.UserListTable.setItem(elementRow, 2, chkBoxItem)
                
                #src: https://stackoverflow.com/questions/39511181/python-add-checkbox-to-every-row-in-qtablewidget
                '''
        return


    def selectionMade(self, selected, deselected):
        for ix in selected.indexes():
            print('Selected Cell Location Row: {0}, Column: {1}'.format(ix.row(), ix.column()))
            self.verifyUserSelectionDoneProperly(ix.row(),ix.column())
        #for ix in deselected.indexes():
        #    print('Deselected Cell Location Row: {0}, Column: {1}'.format(ix.row(), ix.column()))
        #function src: https://learndataanalysis.org/source-code-how-to-detect-selected-and-deselected-cells-on-a-qtablewidget-pyqt5-tutorial/


    def verifyUserSelectionDoneProperly(self, row, col):
        #print("verifying user chose proper column")
        if(col != 2):
            self.InvalidSelectionMade.setText("Please Select only one user from the third column only")
        else:
            self.InvalidSelectionMade.setText("")
            PractitionerSelectedUID = self.UserListTable.item(row, col).text()
            print("The selected UID is: ", self.UserListTable.item(row, col).text())
            personIsPractitioner = True
            self.loadUserDashboard(PractitionerSelectedUID, personIsPractitioner)


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

    def loadUserDashboard(self, userLocalId, isPractitioner):
        goToUserDashboard = UserDashboard(userLocalId, isPractitioner)
        widget.addWidget(goToUserDashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class UserDashboard(QDialog):
    def __init__(self, userId, isPractitioner):
        super(UserDashboard, self).__init__()
        loadUi("UserDashboard.ui", self)
        self.userId = userId
        '''isPractitioner is going to be a boolean value, that can later 
        be used to determine to to exit out userDashboard to userlist'''
        self.isPractitioner = isPractitioner
        print("Verifying person is practioner: ", isPractitioner)

        findWhoUserIs = self.getNamefromUID(userId)
        self.userName = findWhoUserIs

        self.WelcomeName.setText(findWhoUserIs)
        userDescription = self.getDescription(userId)
        self.Description.setText(userDescription)

        '''Code keeps breaking upon button press, have to debug'''
        self.detailedAnalytics.clicked.connect(self.goToUserDetailedAnalyticsSelectionPage)
        #waitingForButtonPress = self.goToUserDetailedAnalyticsSelectionPage(userId, userName, isPractitioner)
        #self.detailedAnalytics.clicked.connect(waitingForButtonPress)

        '''Testing Alt solutions'''

        #waitingForButtonPress = self.goToUserDetailedAnalyticsSelectionPage(userId, userName, isPractitioner)
        #self.detailedAnalytics.clicked.connect(waitingForButtonPress)

    def getNamefromUID(self, userId):
        person = db.child("loginInfo").order_by_child("UID").equal_to(userId).get().val().keys()
        userNameis = list(person)
        userNameis = userNameis[0]
        return(userNameis)

    def getDescription(self, userId):
        userInfo = db.child("loginInfo").get().val()
        #print(userInfo)
        for key, val in userInfo.items():
            if val.get('UID') == userId:
                return(val.get('Description'))

    def goToUserDetailedAnalyticsSelectionPage(self):
        #print("goToUserDetailedAnalyticsSelectionPage coming soon")
        goToUserDetailedAnalyticSelectionPage = UserDetailedAnalyticsSelectionPage(self.userId, self.userName, self.isPractitioner)
        #self.userId, "Mango Pods", self.isPractitioner
        widget.addWidget(goToUserDetailedAnalyticSelectionPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class UserDetailedAnalyticsSelectionPage(QDialog):
    def __init__(self, userId, userName, isPractitioner):
        super(UserDetailedAnalyticsSelectionPage, self).__init__()
        loadUi("UserDetailedAnalyticsSelectionPage.ui", self)

        self.userId = userId
        self.userName = userName
        self.isPractitioner = isPractitioner
        displayHeaderText = userName + "'s Detailed Analytics Selection"
        self.NameDetails.setText(displayHeaderText)


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
    print("Closing Out App")



'''
Refrences Used for this project.

Login in Screen and General PyQt5 Walkthrough were used from 
https://www.youtube.com/@codefirstwithhala
Most concepts are derived from Hala and expanded upon to fit our usecase.

'''