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

yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
listofSensorData = ['heartRate', 'jerk', 'seat', 'speed', 'spo2','weightDistribution']
dailySummary24hrResult = []

tempDate = '2023-03-21'
sensorListCounter = 0

dateFound = False

for items in listofSensorData:
    print(items, "<- name of the key")
    print(list(collectedData.keys())[sensorListCounter], "<- name of the key in db")
    #print(collectedData[items])
    for dates in collectedData[items]:
        #print(dates, "<- dates in db")
        '''uncomment one line below for real code'''
        #if (dates == yesterdayIs):
        '''Below if statement, is just for test demo code, DELETE if statement below and uncomment one above FOR REAL FUNCTIONALITY'''
        if (dates == tempDate):
            dateFound=True
            print(dates, "<- date caught")
            sensorValueCounter = 0
            sensorValueSum = 0

            for key, val in collectedData[items][dates].items():
                print(key, "<- time caught")
                print(val, "<- data is")
                if val == 'null':
                    continue
                else:
                    sensorValueCounter += 1
                #if condition for time
                if items == listofSensorData[1]:
                    sensorValueSum += val[0]
                else:
                    sensorValueSum += val

    if dateFound:
        print(sensorValueCounter, "<- sensorValueCounter is")
        print(sensorValueSum, "<- sensorValueSum is")
        dailySummary24hrResult.append(sensorValueSum/sensorValueCounter)

    sensorListCounter += 1

if (len(dailySummary24hrResult)==0):
    print('no data, on the selected data')
    dailySummary24hrResult = [0,0,0,0,0,0]

print(dailySummary24hrResult)

print('sensors data avaliable')
print(yesterday, '<- yesterday would be')

'''
# setup base structure for collecteddata table
collectedData = "collectedData"

db.child(collectedData).child(userLocalId).child("heartRate").child(creationDate).child(creationTime).set(
    "null")

'''