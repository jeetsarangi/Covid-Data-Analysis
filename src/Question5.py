import json
import pandas as pd
from datetime import datetime
import datetime as d
import dateutil.relativedelta as relativedelta

cowindata = pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory = False)

DistrictList = list(set(cowindata['District_Key'].dropna()))
StateList = list(set(cowindata['State'].dropna()))
DistrictList.sort()
StateList.sort()

startdate = d.datetime(2021,1,16)
enddate = d.datetime(2021,9,1)
delta = d.timedelta(days = 1)

def stringtodate(s):
    date = datetime.strptime(s[:-2], '%d-%m-%Y')
    return date

def datetostring(date):
    s = ''
    if date.day < 10:
        s+="0"
    s += str(date.day)+"-"
    
    if date.month < 10:
        s += "0"
    s += str(date.month)+"-"
    s += str(date.year)
    return s
    
out1 = []
out2 = []
out3 = []
for dist in DistrictList:
    
    temp = cowindata[cowindata['District_Key'] == dist]
    temp = temp.fillna(0) 
    
    
    currentdate = startdate  
    weekdaycount = 0
    weekcount = 0
    monthcount = 0
    rd = relativedelta.relativedelta(months = 1)
    monthend = currentdate+rd-delta
    fcumsumweek = 0
    scumsumweek = 0
    fcumsummonth = 0
    scumsummonth = 0
    while currentdate <= enddate:
        
        if weekdaycount == 7 or currentdate == enddate:
            col = datetostring(currentdate)
            Firstdose = int(temp[col+".3"].iloc[0])-fcumsumweek
            Seconddose = int(temp[col+".4"].iloc[0])-scumsumweek
            
#             totaldose = Firstdose+Seconddose-cumsumweek
            
            fcumsumweek += Firstdose
            scumsumweek += Seconddose
            
            weekcount += 1
            weekdaycount = 0
            
            out1.append((temp['State'].iloc[0],temp['District_Key'].iloc[0],weekcount,Firstdose,Seconddose))
            
        if currentdate == monthend or currentdate == enddate:
            col = datetostring(currentdate)
            Firstdose = int(temp[col+".3"].iloc[0])-fcumsummonth
            Seconddose = int(temp[col+".4"].iloc[0])-scumsummonth
            
            
            fcumsummonth += Firstdose
            scumsummonth += Seconddose
            
            monthcount += 1
            monthend = monthend+rd
            
            out2.append((temp['State'].iloc[0],temp['District_Key'].iloc[0],monthcount,Firstdose,Seconddose))
            
        currentdate+=delta
        weekdaycount += 1
        
    out3.append((temp['State'].iloc[0],temp['District_Key'].iloc[0],fcumsummonth,scumsummonth))

StateList = list(set([row[0] for row in out3]))
StateList.sort()
Stateweekout = []
Statemonout = []
Stateoverall = []
for state in StateList:
    temp1 = [0]*33
    temp2 = [0]*33
        
    for row in out1:
        if row[0] == state:
            temp1[row[2]-1] += row[3]
            temp2[row[2]-1] += row[4]
    
    for index in range(len(temp1)):
        Stateweekout.append((state,index+1,temp1[index],temp2[index]))
    
    
for state in StateList:
    temp1 = [0]*8
    temp2 = [0]*8
#     for i in range(33):
#         temp.append(0)
        
    for row in out2:
        if row[0] == state:
            temp1[row[2]-1] += row[3]
            temp2[row[2]-1] += row[4]
    
    for index in range(len(temp1)):
        Statemonout.append((state,index+1,temp1[index],temp2[index]))
    
        
for state in StateList:
    sum = [0,0]
    for row in out3:
        if row[0] == state:
            sum[0]+=row[2]
            sum[1]+=row[3]
    Stateoverall.append((state,sum[0],sum[1]))

temp_dict1 = {"Districtid":[row[1] for row in out1] , "Weekid":[row[2] for row in out1],"Dose1":[row[3] for row in out1],
              "Dose2":[row[4] for row in out1]}
temp_dict2 = {"Districtid":[row[1] for row in out2] , "Monthid":[row[2] for row in out2],"Dose1":[row[3] for row in out2],
              "Dose2":[row[4] for row in out2]}
temp_dict3 = {"Districtid":[row[1] for row in out3] , "Dose1":[row[2] for row in out3],
              "Dose2":[row[3] for row in out3]}
temp_dict4 = {"Stateid":[row[0] for row in Stateweekout] , "weekid":[row[1] for row in Stateweekout], "Dose1":[row[2] for row in Stateweekout],
              "Dose2":[row[3] for row in Stateweekout]}
temp_dict5 = {"Stateid":[row[0] for row in Statemonout] , "monthid":[row[1] for row in Statemonout], "Dose1":[row[2] for row in Statemonout],
              "Dose2":[row[3] for row in Statemonout]}
temp_dict6 = {"Stateid":[row[0] for row in Stateoverall] , "Dose1":[row[1] for row in Stateoverall],
              "Dose2":[row[2] for row in Stateoverall]}
df = pd.DataFrame(temp_dict1)
df.to_csv('District-vaccinated-count-week.csv', index=False)
df = pd.DataFrame(temp_dict2)
df.to_csv('District-vaccinated-count-month.csv', index=False)
df = pd.DataFrame(temp_dict3)
df.to_csv('District-vaccinated-count-overall.csv', index=False)
df = pd.DataFrame(temp_dict4)
df.to_csv('State-vaccinated-count-week.csv', index=False)
df = pd.DataFrame(temp_dict5)
df.to_csv('State-vaccinated-count-month.csv', index=False)
df = pd.DataFrame(temp_dict6)
df.to_csv('State-vaccinated-count-overall.csv', index=False)

