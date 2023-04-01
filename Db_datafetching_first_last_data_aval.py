import pyrebase
from datetime import datetime,timedelta, date

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


collectedData = db.child("collectedData").child("4nIlD4s8Jdc2Uoa1q0DeONmmisH2").get().val()

startDate = None
endDate = None
nullDate = "null"
listOfDates = []
for item in collectedData:
    for date in collectedData[item]:
        listOfDates.append(date)

startDate = listOfDates[1]
endDate = listOfDates[-1]

print('start date: ', startDate)
print('end date: ', endDate)
startDateSplit = startDate.split("-")
print(int(startDateSplit[0]))




