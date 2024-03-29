# For Firebase
import pyrebase
from datetime import datetime

# For Gui
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QIcon

# For Email Notifications
from email.message import EmailMessage
import ssl
import smtplib


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


class AdminScreen(QDialog):
    def __init__(self):
        super(AdminScreen, self).__init__()
        loadUi("AdminScreen.ui", self)
        self.SucessSubmitted.setText("Status: Not Submitted")

        #Return Button is only disabled for AdminUserCreation.py file only.
        self.ReturnButton.hide()

        self.SubmitButton.clicked.connect(self.submitPressed)
        self.ResetButton.clicked.connect(self.resetAllFields)

        '''Testing code below'''
        #self.SubmitButton.clicked.connect(self.NoMoreEditing)

    def resetAllFields(self):

        #re-enabling fields
        self.FirstName.setReadOnly(False)
        self.FirstName.setDisabled(False)
        self.LastName.setReadOnly(False)
        self.LastName.setDisabled(False)
        self.Email.setReadOnly(False)
        self.Email.setDisabled(False)
        self.Password.setReadOnly(False)
        self.Password.setDisabled(False)
        #self.PasswordDouble.setReadOnly(False)
        #self.PasswordDouble.setEnabled(True)
        self.DOB.setEnabled(True)
        self.TypeSelection.setEnabled(True)
        self.Description.setDisabled(False)
        self.Description.setReadOnly(False)

        #clearing out fields
        self.FirstName.clear()
        self.LastName.clear()
        self.Description.clear()
        self.Password.clear()
        self.Email.clear()
        #self.PasswordDouble.clear()
        #self.PasswordChecker.setText("")
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
        #self.PasswordDouble.setReadOnly(True)
        #self.PasswordDouble.setDisabled(True)
        self.DOB.setDisabled(True)
        self.TypeSelection.setDisabled(True)
        self.Description.setDisabled(True)
        self.Description.setReadOnly(True)
        print("disable User input sucess")
        return

    def submitPressed(self):

        firstName = self.FirstName.text()
        lastName = self.LastName.text()
        email = self.Email.text()
        password = self.Password.text()
        #confirmPassword = self.PasswordDouble.text()
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
        #UNCOMMENT WHEN DONE TESTING
        #self.sendUserNotification(email, password)


        print("Notification Sent, Everything completed.")
        self.SucessSubmitted.setText("Submitted :)")
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
        db.child(collectedData).child(userLocalId).child("speed").child(creationDate).child(creationTime).set(
            "null")
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


# main
app = QApplication(sys.argv)
AdminPage = AdminScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(AdminPage)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.setWindowIcon(QIcon('projectIcon.jpg'))
widget.setWindowTitle("Roll Smart")
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
