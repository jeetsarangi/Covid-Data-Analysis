import json
import pandas as pd
import datetime
import dateutil.relativedelta as relativedelta
import numpy as np

cowindata = pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory = False)
district = pd.read_csv('districts.csv')
district['Date'] = pd.to_datetime(district['Date'])

StateIds = cowindata[['State','State_Code']].drop_duplicates()
StateIds = StateIds.dropna()

fil = ['Unknown','Italians','Other State','Other Region','State Pool']
indexes = district[district['District'].isin(fil)].index
district.drop(indexes,inplace = True)
TargetList = district[['District','State']].drop_duplicates()

out1 = []
out2 = []
out3 = []

for row in range(len(TargetList)):
    distr,state = TargetList.iloc[row,0],TargetList.iloc[row,1]
    r = StateIds[StateIds['State'] == state]
    if len(r) == 0:
        continue
    state_id = r.iloc[0,1]
    
    perstate = district[(district["District"]==distr) & (district["State"] == state)]
    weekcount = 0
    monthcount = 0
    daycount = 0
    startdate = datetime.datetime(2020,3,15)
    currentdate = startdate
    enddate = datetime.datetime(2021,8,14)
    d = datetime.timedelta(days=1)
    rd = relativedelta.relativedelta(months = 1)
    monthend = startdate + rd - d
    casescum = 0
    
    cur_week_cases = 0
    cur_month_cases = 0
    while currentdate<enddate:
        temp = perstate.loc[perstate['Date'] == currentdate]

        if len(temp) != 0:
            cur_week_cases += temp.iloc[0,3]-casescum
            cur_month_cases += temp.iloc[0,3]-casescum
            casescum += temp.iloc[0,3]-casescum
            
        daycount += 1
        currentdate += d

        if(daycount == 7) or currentdate == enddate:
            weekcount += 1
            daycount = 0
            out1.append((state_id+"_"+distr,weekcount,cur_week_cases))

            cur_week_cases = 0
            
        if currentdate == monthend or currentdate == enddate :
            monthcount += 1
            out2.append((state_id+"_"+distr,monthcount,cur_month_cases))
            cur_month_cases = 0
            monthend += rd

            
#     out1.append((District,weekcount+1,cur_week_cases))
#     out2.append((state_id+"_"+distr,monthcount+1,cur_month_cases))
    out3.append((state_id+"_"+distr,casescum))
    
district_cases_week = {"District":[row[0] for row in out1],"Week-id":[row[1] for row in out1],"Cases":[row[2] for row in out1]}
district_cases_month = {"District":[row[0] for row in out2],"Month-id":[row[1] for row in out2],"Cases":[row[2] for row in out2]}
district_cases_Overall = {"District":[row[0] for row in out3],"Cases":[row[1] for row in out3]}
df = pd.DataFrame(district_cases_week)
df.to_csv('cases-week.csv', index=False)
df = pd.DataFrame(district_cases_month)
df.to_csv('cases-month.csv', index=False)
df = pd.DataFrame(district_cases_Overall)
df.to_csv('cases-Overall.csv', index=False)