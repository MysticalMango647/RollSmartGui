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
#print(collectedData)
yesterday = (date.today() - timedelta(days=6))
yesterdayIs = yesterday.strftime('%Y-%m-%d')
listofSensorData = ['heartRate', 'jerk', 'seat', 'speed', 'spo2','weightDistribution']
dailySummary24hr = []
for items in listofSensorData:
    print(items, "<- name of the key")
    #print(collectedData[items])
    for dates in collectedData[items]:
        #print(dates, "<- dates in db")
        if (dates == yesterdayIs):
            print(dates, "<- date caught")
            sensorValueCounter = 0
            sensorValueSum = 0
            '''
            for key, val in collectedData[items][dates].items():
                print(key, "<- time caught")
                print(val, "<- data is")
                sensorValueCounter += 1
                sensorValueSum = sensorValueSum + int(val)'''
        else:
            print("no data collected from yesterdayIs")
    print(sensorValueCounter, "<- sensorValueCounter is")
    print(sensorValueSum, "<- sensorValueSum is")
    #dailySummary24hr.append(sensorValueSum/sensorValueCounter)

print(yesterday.strftime('%Y-%m-%d'))

print('sensors data avaliable')
for key, val in collectedData.items():
    print(key)

print(dailySummary24hr)
'''
# setup base structure for collecteddata table
collectedData = "collectedData"

db.child(collectedData).child(userLocalId).child("heartRate").child(creationDate).child(creationTime).set(
    "null")

'''