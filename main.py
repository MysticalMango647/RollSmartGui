#!/usr/bin/env python3


# For Gui
import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QComboBox,QTableWidget, QRadioButton, QTableWidgetItem, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon

# For Firebase
import pyrebase


#Libraries carried over from admin screen
# For Email Notifications
from email.message import EmailMessage
import ssl
import smtplib

#date time
from datetime import datetime, date, timedelta

import keyboard

# KeyConfig
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

# Establish User
global userLocalId


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("IntroScreen.ui", self)
        self.PasswordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        # gettingUserId=self.verifySignIn
        # print(gettingUserId)
        self.signInButton.clicked.connect(self.verifySignIn)
        self.createNewAccountButton.clicked.connect(self.loadNewAccountCreationPage)
        self.userId = None
        self.pracId = None
        self.EmailEntry.clear()
        self.PasswordEntry.clear()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.verifySignIn()

    def loadNewAccountCreationPage(self):
        practId = None
        goToNewAccountCreation = NewAccountCreation(practId)
        widget.addWidget(goToNewAccountCreation)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def findNextScreenToLoad(self, userRole, userLocalId):
        # print("in findNextScreenToLoad function")
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
        noPracId = None
        goToUserDashboard = UserDashboard(userLocalId, noPracId)
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
            print("the accessing person is", accessingPersonIs)
            # print("in main accessing person name is: ", accessingPersonIs)
            roleOfAccessingPersonIs = db.child("loginInfo").child(accessingPersonIs).child("role").get().val()
            # print("role of: ", accessingPersonIs, "is: ", roleOfAccessingPersonIs)
            self.findNextScreenToLoad(roleOfAccessingPersonIs, userLocalId)
        except:
            self.InvalidSignInAttempt.setText("Invalid Email or Password")


class UserList(QDialog):
    def __init__(self, pracID):
        super(UserList, self).__init__()
        loadUi("UserList.ui", self)
        #storing pracID so can be used to get name and backtrack to this page
        self.pracID = pracID
        self.UserUIDList = []
        self.localUserID = None

        global UserUIDtoView

        findWhoPracIs = self.getNamefromUID(pracID)
        WelcomeString = str("Welcome, Dr. " + findWhoPracIs)

        self.WelcomeName.setText(WelcomeString)
        self.UserListTable.setColumnWidth(0, 250)
        self.UserListTable.setColumnWidth(1, 80)
        self.UserListTable.setColumnWidth(2, 440)
        self.UserListTable.setColumnWidth(3, 200)

        #populate table with data
        self.loadUserTableInfo()

        #Line below makes it so the practitioner is not able to edit the boxes
        self.UserListTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        #newacc and signout button page redirect
        self.PracCreateNewUser.clicked.connect(self.loadNewAccountCreationPage)
        self.SignOut.clicked.connect(self.loadLoginPage)

        #submit button action clause
        self.Submit.clicked.connect(self.submitButtonPressed)
        self.UserListTable.selectionModel().selectionChanged.connect(self.selectionMade)


    def submitButtonPressed(self):
        validSelection = False
        RowBoxIndex = int(self.RowCounterBox.currentText()) - 1
        self.UserListTable.selectRow(RowBoxIndex)
        self.localUserID = self.UserUIDList[int(self.RowCounterBox.currentText()) - 1]
        if (int(self.RowCounterBox.currentText()))!= 0:
            print("in submitbuttonpressed function")
            self.loadUserDashboard()
        else:
            print("current rowcounterbox is 0, in the if statement. Proof ->", int(self.RowCounterBox.currentText()))
            self.InvalidSelectionMade.setText("Select a data on table or choose from row drop down")

    def selectionMade(self, selected, deselected):
        for ix in selected.indexes():
            print('Selected Cell Location Row: {0}, Column: {1}'.format(ix.row(), ix.column()))
            #combobox row counter updating
            self.RowCounterBox.setCurrentIndex(ix.row()+1)
            #setting local user id to view for when we need it for the next page
            self.localUserID = self.UserUIDList[int(self.RowCounterBox.currentText())-1]
            print(self.localUserID)
            self.verifyUserSelectionDoneProperly(ix.row(), ix.column())
        # function src: https://learndataanalysis.org/source-code-how-to-detect-selected-and-deselected-cells-on-a-qtablewidget-pyqt5-tutorial/

    def verifyUserSelectionDoneProperly(self, row, col):
        # print("verifying user chose proper column")
        approvedCol = [0,1,2,3]
        print(self.RowCounterBox.currentText(), "<- current rowcounterbox index")
        if (col not in approvedCol or int(self.RowCounterBox.currentText()) == 0):
            print("current rowcounterbox is 0, in the if statement")
            #self.InvalidSelectionMade.setText("Select a data on table or choose from row drop down")

        else:
            self.InvalidSelectionMade.setText("")
            PractitionerSelectedUID = self.UserListTable.item(row, col).text()
            print("The selected data is: ", self.UserListTable.item(row, col).text())
            personIsPractitioner = True
            #self.submitButtonPressed()
            self.Submit.clicked.connect(self.submitButtonPressed)
            #self.Submit.clicked.connect(self.loadUserDashboard)
            ###################################
    def loadLoginPage(self):
        goToWelcome = WelcomeScreen()
        widget.addWidget(goToWelcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loadNewAccountCreationPage(self):
        practId = self.pracID
        goToNewAccountCreation = NewAccountCreation(practId)
        widget.addWidget(goToNewAccountCreation)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def loadUserTableInfo(self):
        allUserInfo = db.child("loginInfo").get().val()
        # print(db.child("loginInfo").get().val())
        elementRow = 0
        numberofUsers = len(list(db.child("loginInfo").order_by_child("role").equal_to("User").get().val().keys()))
        # print(numberofUsers)

        self.UserListTable.setRowCount(numberofUsers)

        comboboxList=["0"]

        #NUmber on combo box in incremented by 1 to match what UserListTable displays
        for i in range(numberofUsers):
            comboboxList.append(str(i+1))
        print(comboboxList)
        self.RowCounterBox.addItems(comboboxList)
        # self.signInButton.clicked.connect(self.verifyUserSelectionDoneProperly())

        for key, val in allUserInfo.items():
            # print(key)
            # print(val.get('DOB'))
            selectedUID = val.get('UID')
            # Only display Users, no practitioners in the list of users
            if (val.get('role') != "Practitioner"):

                #Storing UID in a list for retrival to load next page accordingly
                UniqueID = val.get('UID')
                self.UserUIDList.append(UniqueID)

                #Col 1: Name
                self.UserListTable.setItem(elementRow, 0, QtWidgets.QTableWidgetItem(str(key)))
                #Col 2: Age
                dobYearString, mm, dd, yy = (val.get('DOB')).split(" ", 3)
                months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
                getMonthinNum = months.index(mm.lower())+1
                today = date.today()
                year_diff = today.year - int(yy)
                getMMandDDdifference = ((today.month, today.day) < (int(getMonthinNum), int(dd)))
                age = year_diff - getMMandDDdifference
                #logic from https://pyshark.com/build-age-calculator-in-python/
                self.UserListTable.setItem(elementRow, 1, QtWidgets.QTableWidgetItem(str(age)))

                # Col 3: Description
                self.UserListTable.setItem(elementRow, 2, QtWidgets.QTableWidgetItem(str(val.get('Description'))))

                # Col 4: DOB
                self.UserListTable.setItem(elementRow, 3, QtWidgets.QTableWidgetItem(str(val.get('DOB'))))

                elementRow = elementRow + 1


                '''Was trying to add radio button here instead, but it wasn't working out'''
                # userSelectRadioButton = QtWidgets.QRadioButton(str(val.get('UID')))
                # userSelectRadioButton.setChecked(False)
                # self.UserListTable.setItem(elementRow, 2, QtWidgets.QTableWidgetItem(userSelectRadioButton))

                '''was Experimenting with check box for col 2, select user'''
                '''
                chkBoxItem = QTableWidgetItem(selectedUID)
                chkBoxItem.setText(str(selectedUID))
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                self.ui.UserListTable.setItem(elementRow, 2, chkBoxItem)
                
                #src: https://stackoverflow.com/questions/39511181/python-add-checkbox-to-every-row-in-qtablewidget
                '''
        #print(self.UserUIDList, "<- UID of all users that are dispayed on the userlist table, The length is ->", len(self.UserUIDList))

        return

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
        return (accessingPersonName)

    def loadUserDashboard(self):
        goToUserDashboard = UserDashboard(self.localUserID, self.pracID)
        widget.addWidget(goToUserDashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class UserDashboard(QDialog):
    def __init__(self, userId, pracID):
        super(UserDashboard, self).__init__()
        loadUi("UserDashboard.ui", self)
        self.userId = userId
        self.pracID = pracID
        print("made it back to udash")
        print("The practId is: ", pracID)

        '''isPractitioner is going to be a boolean value, that can later 
        be used to determine to to exit out userDashboard to userlist'''


        findWhoUserIs = self.getNamefromUID()
        self.userName = findWhoUserIs

        self.WelcomeName.setText(findWhoUserIs)
        userDescription = self.getDescription()
        self.Description.setText(userDescription)

        '''Code keeps breaking upon button press, have to debug'''
        self.detailedAnalytics.clicked.connect(self.goToUserDetailedAnalyticsSelectionPage)
        # waitingForButtonPress = self.goToUserDetailedAnalyticsSelectionPage(userId, userName, isPractitioner)
        # self.detailedAnalytics.clicked.connect(waitingForButtonPress)

        '''Testing Alt solutions'''
        # waitingForButtonPress = self.goToUserDetailedAnalyticsSelectionPage(userId, userName, isPractitioner)
        # self.detailedAnalytics.clicked.connect(waitingForButtonPress)

        '''Loading data from userName'''
        #self.loadUserStats(self.userId)


        # block users from making practitioner accounts
        if self.pracID is None:
            self.ReturnButton.hide()
        self.ReturnButton.clicked.connect(self.loadUserList)
        self.SignOut.clicked.connect(self.loadLoginPage)

    def loadUserList(self):
        goToUserList = UserList(self.pracID)
        widget.addWidget(goToUserList)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def loadLoginPage(self):
        goToWelcome = WelcomeScreen()
        widget.addWidget(goToWelcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def getNamefromUID(self):
        person = db.child("loginInfo").order_by_child("UID").equal_to(self.userId).get().val().keys()
        userNameis = list(person)
        userNameis = userNameis[0]
        return (userNameis)

    def getDescription(self):
        userInfo = db.child("loginInfo").get().val()
        # print(userInfo)
        for key, val in userInfo.items():
            if val.get('UID') == self.userId:
                return (val.get('Description'))

    def loadUserStats(self):
        print(self.userId, " data being fetched and updated displayed")
        userStats = db.child("collectedData").child(self.userId).get().val()
        #print(userStats, " data that collected from the user.")


        for key, val in userStats.items():
            print(key.get(''), "key's of the choosen user are")
            #if val.get('') == date.today() - timedelta(days=1):
            #    return (val.get('Description'))


    def goToUserDetailedAnalyticsSelectionPage(self):
        # print("goToUserDetailedAnalyticsSelectionPage coming soon")qt
        goToUserDetailedAnalyticSelectionPage = UserDetailedAnalyticsSelectionPage(self.userId, self.userName,self.pracID)
        widget.addWidget(goToUserDetailedAnalyticSelectionPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class UserDetailedAnalyticsSelectionPage(QDialog):
    def __init__(self, userId, userName, pracId):
        super(UserDetailedAnalyticsSelectionPage, self).__init__()
        loadUi("UserDetailedAnalyticsSelectionPage.ui", self)
        print("PracId is: ", pracId, "UserId is: ", userId)
        self.userId = userId
        self.userName = userName
        self.pracId = pracId
        displayHeaderText = userName + "'s Detailed Analytics Selection"
        self.NameDetails.setText(displayHeaderText)
        loadvals = self.placeholder

        self.ReturnButton.clicked.connect(loadvals)
        self.SignOut.clicked.connect(self.loadLoginPage)

    def placeholder(self):
        print("in placehodler")
        self.loadUserDashboard(self.userId,self.pracId)
    def loadUserDashboard(self, UID, PID):
        print("in the load user dashboard function")
        toUserDashboard = UserDashboard(UID, PID)
        widget.addWidget(toUserDashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def loadLoginPage(self):
        goToWelcome = WelcomeScreen()
        widget.addWidget(goToWelcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class NewAccountCreation(QDialog):
    def __init__(self, practID):
        super(NewAccountCreation, self).__init__()
        loadUi("AdminScreen.ui", self)


        self.SucessSubmitted.setText("Status: Not Submitted")

        # Return Button is only disabled for AdminUserCreation.py file only.
        #self.ReturnButton.hide()

        self.SubmitButton.clicked.connect(self.submitPressed)
        self.ResetButton.clicked.connect(self.resetAllFields)

        '''Testing code below'''
        # self.SubmitButton.clicked.connect(self.NoMoreEditing)


        '''New Code on the main.py side for compatibility of roletype'''
        self.practID = practID
        print("The practId is: ", practID)
        # block users from making practitioner accounts
        if practID is None:
            self.TypeSelection.setDisabled(True)
        self.ReturnButton.clicked.connect(self.FigureOutReturnScreen)


    def FigureOutReturnScreen(self):
        if self.practID is None:
            self.loadLoginPage()
        if self.practID is not None:
            self.loadUserList()
    def loadUserList(self):
        goToUserList = UserList(self.practID)
        widget.addWidget(goToUserList)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def loadLoginPage(self):
        goToWelcome = WelcomeScreen()
        widget.addWidget(goToWelcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def resetAllFields(self):

        # re-enabling fields
        self.FirstName.setReadOnly(False)
        self.FirstName.setDisabled(False)
        self.LastName.setReadOnly(False)
        self.LastName.setDisabled(False)
        self.Email.setReadOnly(False)
        self.Email.setDisabled(False)
        self.Password.setReadOnly(False)
        self.Password.setDisabled(False)
        # self.PasswordDouble.setReadOnly(False)
        # self.PasswordDouble.setEnabled(True)
        self.DOB.setEnabled(True)
        self.TypeSelection.setEnabled(True)
        self.Description.setDisabled(False)
        self.Description.setReadOnly(False)

        # clearing out fields
        self.FirstName.clear()
        self.LastName.clear()
        self.Description.clear()
        self.Password.clear()
        self.Email.clear()
        # self.PasswordDouble.clear()
        # self.PasswordChecker.setText("")
        print("all fields have been cleared and enabled")
        return

    def NoMoreEditing(self):
        listToDisable = ['FirstName', 'LastName', 'Email', 'Password', 'PasswordDouble', 'Description']
        '''
        for items in listToDisable:

            self.getattr(self, items).setReadOnly(True)
            self.getattr(self, items).setDisabled(True)

        '''
        self.FirstName.setReadOnly(True)
        self.FirstName.setDisabled(True)
        self.LastName.setReadOnly(True)
        self.LastName.setDisabled(True)
        self.Email.setReadOnly(True)
        self.Email.setDisabled(True)
        self.Password.setReadOnly(True)
        self.Password.setDisabled(True)
        # self.PasswordDouble.setReadOnly(True)
        # self.PasswordDouble.setDisabled(True)
        self.DOB.setDisabled(True)
        self.TypeSelection.setDisabled(True)
        self.Description.setDisabled(True)
        self.Description.setReadOnly(True)
        print("disable User input sucess")
        return

    def submitPressed(self):
        self.SucessSubmitted.setText("Status: Loading")
        firstName = self.FirstName.text()
        lastName = self.LastName.text()
        email = self.Email.text()
        password = self.Password.text()
        # confirmPassword = self.PasswordDouble.text()
        description = self.Description.toPlainText()
        print(description)
        roleType = self.TypeSelection.currentText()
        dob = self.DOB.selectedDate().toString()

        self.createFirebaseAuthAccount(email, password)

        self.fillInLoginInfoToFirebase(email, password, firstName, lastName, description, roleType, dob)

        print(lastName + ", " + firstName)
        print("The Selected Role is: ", roleType)
        print("The Selected DOB is: ", dob)
        print("Submitted Pressed")

        #########################################
        # UNCOMMENT WHEN DONE TESTING
        self.sendUserNotification(email, password)
        #########################################

        print("Notification Sent, Everything completed.")
        self.SucessSubmitted.setText("Status: Submitted :)")
        self.NoMoreEditing()

        # Setup email and password for firebase Auth

    def createFirebaseAuthAccount(self, email, password):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            print("New Account Created Sucessfully")
            return True
        except:
            print("email exist already")
            return False

    def fillInLoginInfoToFirebase(self, email, password, firstName, lastName, description, roleType, dob):
        # signing into firebase

        login = auth.sign_in_with_email_and_password(email, password)
        print("sign on to firebase sucess")
        userInfo = auth.get_account_info(login['idToken'])
        userLocalId = userInfo['users'][0]['localId']
        print(userInfo)
        print("The user local Id is: ", userLocalId)

        # setup detail for loginInfo Table
        loginInfo = "loginInfo"
        # templateForName = "Name"
        CreateName = (firstName + " " + lastName)
        # db.child(loginInfo).child(templateForName).set(CreateName)
        db.child(loginInfo).child(CreateName).child("UID").set(userLocalId)
        db.child(loginInfo).child(CreateName).child("role").set(roleType)
        db.child(loginInfo).child(CreateName).child("DOB").set(dob)
        db.child(loginInfo).child(CreateName).child("Description").set(description)

        # setup base structure for collecteddata table
        collectedData = "collectedData"
        creationDate = datetime.today().strftime('%Y-%m-%d')
        creationTime = datetime.today().strftime('%H:%M:%S')
        db.child(collectedData).child(userLocalId).child("heartRate").child(creationDate).child(creationTime).set(
            "null")
        db.child(collectedData).child(userLocalId).child("jerk").child(creationDate).child(creationTime).set("null")
        db.child(collectedData).child(userLocalId).child("seat").child(creationDate).child(creationTime).set("null")
        db.child(collectedData).child(userLocalId).child("speed").child(creationDate).child(creationTime).set("null")
        db.child(collectedData).child(userLocalId).child("weightDistribution").child(creationDate).child(
            creationTime).set("null")
        db.child(collectedData).child(userLocalId).child("spo2").child(creationDate).child(creationTime).set("null")

        print("sucessfully built of login info and collected data time, sending of to email notification function")

        return

        # Email Notification to user when account is created.

    def sendUserNotification(self, email, password):
        # email notification details
        rollSmartEmail = 'sysc4907rollsmart@gmail.com'
        rollSmartPassword = 'Sysc4907'
        securePassword = 'fxnoeivordwkvtkf'
        receivingEmail = email

        emailSubject = 'Welcome to RollSmart!'
        emailBody = """
                Welcome to RollSmart!

                Your Username is: """ + receivingEmail + """
                Your Password is: """ + password + """

                If you have any issues, please contact your local doctors office.

                -RollSmart
                """
        # Set Elements of email
        emailObject = EmailMessage()
        emailObject['From'] = rollSmartEmail
        emailObject['To'] = receivingEmail
        emailObject['Subject'] = emailSubject
        emailObject.set_content(emailBody)

        # adding ssl security for email transmission
        securityContent = ssl.create_default_context()

        # Sending the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=securityContent) as smtp:
            smtp.login(rollSmartEmail, securePassword)
            smtp.sendmail(rollSmartEmail, receivingEmail, emailObject.as_string())
        print("Email Sent")

        # SMTP function dereived from: https://www.youtube.com/watch?v=g_j6ILT-X0k&ab_channel=ThePyCoach
        return

if __name__ == "__main__":
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
