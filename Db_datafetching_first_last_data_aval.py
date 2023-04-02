import pyrebase
from datetime import datetime,timedelta, date

import plotly.express as px
import plotly.graph_objs as go


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
DateAndTimeList = []
ValueList = []
selectedStartDate = '2023-02-27'
selectedEndDate = '2023-03-20'

selectedStartDateSplit = selectedStartDate.split('-')
selectedStartDateTimeVar = datetime(int(selectedStartDateSplit[0]),int(selectedStartDateSplit[1]),int(selectedStartDateSplit[2]))
selectedEndDateSplit = selectedStartDate.split('-')
selectedEndDateTimeVar = datetime(int(selectedEndDateSplit[0]),int(selectedEndDateSplit[1]),int(selectedEndDateSplit[2]))

format = '%Y-%m-%d'
startingPointDate = datetime.strptime(selectedStartDate, format)
endingPointDate = datetime.strptime(selectedEndDate, format)

for item in collectedData:
    if item == 'heartRate':
        for dateInDb in collectedData[item]:

            dateInDbSplit = dateInDb.split('-')
            compareDateInDbVar = datetime(int(dateInDbSplit[0]),int(dateInDbSplit[1]),int(dateInDbSplit[2]))

            if startingPointDate <= compareDateInDbVar <= endingPointDate:
                listOfDates.append(dateInDb)
                for time, value in collectedData[item][dateInDb].items():
                    if value == nullDate:
                        print('skipping date: ', dateInDb, ', Because Value is: ', value)
                    else:
                        print(item, ', ', dateInDb, ', ', time, ', ', value)
                        DateTimeTogether = dateInDb + ' ' + time
                        DateAndTimeList.append(DateTimeTogether)
                        ValueList.append(value)
                        #print(DateTimeTogether)
                        #DateTimeValue[DateTimeTogether] = value
            else:
                (dateInDb, 'skipping this dates, as user per user defined dates.')
print(DateAndTimeList, 'dt lsit')
print(ValueList, 'value list')

fig = px.line(x=DateAndTimeList, y=ValueList)
fig.show(renderer="browser")

'''
DateTimeValue['DateAndTime']= DateAndTimeList
DateTimeValue['Value']=ValueList

the_dict = {'dates': ['2020-01-01', '2020-01-02'], 'y_vals': [100,200]}
fig = px.bar(the_dict, x='dates', y='y_vals')
fig.show()'''

'''
df = px.data.stocks()
fig = px.line(DateTimeValue, x='DateAndTime', y="Value")
fig.show()'''
'''
print(DateTimeValue)
fig = px.bar(DateTimeValue, x='DateAndTime', y='Value')
fig.show()
'''

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



