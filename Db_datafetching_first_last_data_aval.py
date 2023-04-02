import pyrebase
from datetime import datetime,timedelta, date

#import plotly.express as px
#import plotly.graph_objs as go


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
collectedDataList = list(collectedData)
startDate = None
endDate = None
nullDate = "null"
listOfDates = []

DateTimeValue = {}

selectedStartDate = '2023-03-07'
selectedEndDate = '2023-03-21'

selectedStartDateSplit = selectedStartDate.split('-')
selectedStartDateTimeVar = datetime(int(selectedStartDateSplit[0]),int(selectedStartDateSplit[1]),int(selectedStartDateSplit[2]))
selectedEndDateSplit = selectedStartDate.split('-')
selectedEndDateTimeVar = datetime(int(selectedEndDateSplit[0]),int(selectedEndDateSplit[1]),int(selectedEndDateSplit[2]))

format = '%Y-%m-%d'
start_dt = datetime.strptime(selectedStartDate, format)
end_dt = datetime.strptime(selectedEndDate, format)

for item in collectedData:
    if item == 'heartRate':
        for dateInDb in collectedData[item]:

            dateInDbSplit = dateInDb.split('-')
            compareDateInDbVar = datetime(int(dateInDbSplit[0]),int(dateInDbSplit[1]),int(dateInDbSplit[2]))

            if (compareDateInDbVar >= selectedStartDateTimeVar) and (compareDateInDbVar <= selectedEndDateTimeVar):
                listOfDates.append(dateInDb)
                print(date)
                for time, value in collectedData[item][dateInDb].items():
                    if value != nullDate:
                        print(item, ', ', dateInDb, ', ', time, ', ', value)
                        DateTimeTogether = dateInDb + ' ' + time
                        print(DateTimeTogether)
                        DateTimeValue[DateTimeTogether]=value

print(DateTimeValue)



'''
for i in collectedData:
    if i == 'heartRate':
        #print(collectedData[i])
        for j in collectedData[i]:
            print(collectedData[i][j])
            print()
            for time, value in collectedData[i][j].items():
                print(time, value)

'''



