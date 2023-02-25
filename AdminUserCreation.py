# For Firebase
import pyrebase
from datetime import datetime

#import ipython
# For Gui
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication


# For Email Notifications
from email.message import EmailMessage
import ssl
import smtplib


# setup email SMTP connection
# session=smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
# session.login(USERNAME, PASSWORD)

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
        self.SucessSubmitted.setText("Not Submitted")
        self.SubmitButton.clicked.connect(self.submitPressed)

    # once Submitted is pressed, no more editing is allowed
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
        self.PasswordDouble.setReadOnly(True)
        self.PasswordDouble.setDisabled(True)
        # self.DOB.setReadOnly(True)
        # self.DOB.setDisabled(True)

        print("disable User input sucess")
        return

    def submitPressed(self):
        firstName = self.FirstName.text()
        lastName = self.LastName.text()
        email = self.Email.text()
        password = self.Password.text()
        passwordCheck = self.PasswordDouble.text()
        description = self.Description.text()
        roleType = self.TypeSelection.currentText()
        dob = self.DOB.selectedDate().toString()

        self.createFirebaseAuthAccount(email, password)

        # email, password, firstName, lastName, description, roleType, dob
        self.fillInLoginInfoToFirebase(email, password, firstName, lastName, description, roleType, dob)

        print(lastName + ", " + firstName)
        print("The Selected Role is: ", roleType)
        print("The Selected DOB is: ", dob)
        print("Submitted Pressed")
        self.sendUserNotification(email, password)
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
        #templateForName = "Name"
        CreateName = (firstName + " " + lastName)
        #db.child(loginInfo).child(templateForName).set(CreateName)
        db.child(loginInfo).child(CreateName).child("UID").set(userLocalId)
        db.child(loginInfo).child(CreateName).child("role").set(roleType)
        db.child(loginInfo).child(CreateName).child("DOB").set(dob)
        db.child(loginInfo).child(CreateName).child("Description").set(description)

        #setup base structure for collecteddata table
        collectedData = "collectedData"
        creationDate = datetime.today().strftime('%Y-%m-%d')
        creationTime = datetime.today().strftime('%H:%M:%S')
        db.child(collectedData).child(userLocalId).child("heartRate").child(creationDate).child(creationTime).set("null")
        db.child(collectedData).child(userLocalId).child("jerk").child(creationDate).child(creationTime).set("null")
        db.child(collectedData).child(userLocalId).child("seat").child(creationDate).child(creationTime).set("null")
        db.child(collectedData).child(userLocalId).child("speed").child(creationDate).child(creationTime).set("null")
        db.child(collectedData).child(userLocalId).child("weightDistribution").child(creationDate).child(creationTime).set("null")

        print("sucessful built of login info and collected data tan;e, sending of to email notification function")

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

        Your Username is: this current email.
        Your Password is: """ + password + """

        If you have any issues, please contact your doctors office.

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
        return


# main
app = QApplication(sys.argv)
AdminPage = AdminScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(AdminPage)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
#widget.setWindowIcon(QIcon('projectIcon.jpg'))
widget.setWindowTitle("Roll Smart")
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
