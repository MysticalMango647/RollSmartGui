import pyrebase
from datetime import datetime

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


allUserInfo = db.child("collectedData").get().val()
print(allUserInfo)
for key, val in allUserInfo.items():

    #print(val.get('heartRate'))
    collectedData = "collectedData"

    print(key)
    creationDate = datetime.today().strftime('%Y-%m-%d')
    creationTime = datetime.today().strftime('%H:%M:%S')
    db.child(collectedData).child(key).child("spo2").child(creationDate).child(creationTime).set("null")

'''
# setup base structure for collecteddata table
collectedData = "collectedData"

db.child(collectedData).child(userLocalId).child("heartRate").child(creationDate).child(creationTime).set(
    "null")

'''