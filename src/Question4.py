import json
import pandas as pd
import datetime
import dateutil.relativedelta as relativedelta

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
DistrictList = []
StateList = []
for row in range(len(TargetList)):
    distr,state = TargetList.iloc[row,0],TargetList.iloc[row,1]
    r = StateIds[StateIds['State'] == state]
    if len(r) == 0:
        continue
    state_id = r.iloc[0,1]
    
    perstate = district[(district["District"]==distr) & (district["State"] == state)]
    weekcount = 0
    monthcount = 0
    
    perstate = district[(district["District"]==distr) & (district["State"] == state)]
    weekcount = 0
    monthcount = 0
    daycount = 0
    startdate = datetime.datetime(2020,3,15)
    currentdate = startdate
    enddate = datetime.datetime(2021,8,14)
    d = datetime.timedelta(days=1)
    d3 = datetime.timedelta(days=3)
    rd = relativedelta.relativedelta(months = 1)
    monthend = startdate + rd - d
    
    while currentdate<enddate:
        daycount += 1
        currentdate += d
        
        if(daycount == 7):
            weekcount += 1
            daycount = 0
            cur_week_cases = 0
            
            temp = perstate.loc[perstate['Date'] == currentdate]
            if len(temp)!=0:
                cur_week_cases = temp.iloc[0,3]-temp.iloc[0,4]-temp.iloc[0,5]
            
            out1.append((state_id+"_"+distr,weekcount,cur_week_cases))
            currentdate -= d3
            
        if currentdate == monthend or currentdate == enddate:
            monthcount += 1
            cur_month_cases = 0
            
            temp = perstate.loc[perstate['Date'] == currentdate]
            
            if len(temp)!=0:
                cur_month_cases = temp.iloc[0,3]-temp.iloc[0,4]-temp.iloc[0,5]
            
            out2.append((state_id+"_"+distr,monthcount,cur_month_cases))
            
            monthend += rd
    y1 = state_id+"_"+distr
    out1.append((y1,weekcount+1,cur_week_cases))
    DistrictList.append(y1)
    if (r.iloc[0,0],r.iloc[0,1]) not in StateList:
        StateList.append((r.iloc[0,0],r.iloc[0,1]))

perstate = district[(district["District"]=="Anantapur") & (district["State"] == "Andhra Pradesh")]
perstate

Districtpeaks = []
for dist in DistrictList:
    temp = []
    for row in out1:
        if row[0] != dist and len(temp)!=0:
            break;
        else:
            if row[0] == dist:
                temp.append(row)
    max = 0
    peak1 = -1
    peak2 = -1
    for i in range(0,70):
        if temp[i][2]>max:
            max = temp[i][2]
            peak1 = temp[i][1]
    max = 0       
    for i in range(70,129):
        if temp[i][2]>max:
            max = temp[i][2]
            peak2 = temp[i][1]
            
            
        
    Districtpeaks.append((dist,peak1,peak2))

    Districtmonpeaks = []
for dist in DistrictList:
    temp = []
    for row in out2:
        if row[0] != dist and len(temp)!=0:
            break;
        else:
            if row[0] == dist:
                temp.append(row)
                

    
    max = 0
    peak1 = -1
    peak2 = -1
    for i in range(0,9):
        if temp[i][2]>max:
            max = temp[i][2]
            peak1 = temp[i][1]
    max = 0       
    for i in range(9,17):
        if temp[i][2]>max:
            max = temp[i][2]
            peak2 = temp[i][1]
        
    Districtmonpeaks.append((dist,peak1,peak2))

    State_cases_Lists = {}
State_week_peak = []
State_mon_peak = []
for eachstate in StateList:
    test = eachstate[1]
    State_cases_Lists[test] = []

for row in out1:
        temp = row[0].split("_")
        State_cases_Lists[temp[0]].append(row)

for key in StateList:
    perweekcases = [0 for x in range(1,130)]
    temp = State_cases_Lists[key[1]]
    for row in temp:
        perweekcases[row[1]-1] += row[2]
        
    #to find the peaks
    max = 0
    peak1 = -1
    peak2 = -1
    for i in range(0,70):
        if perweekcases[i]>max:
            max = perweekcases[i]
            peak1 = i+1
    max = 0       
    for i in range(70,129):
        if perweekcases[i]>max:
            max = perweekcases[i]
            peak2 = i+1
    
    State_week_peak.append((key[0],peak1,peak2))
    
State_cases_Lists = {}  
for eachstate in StateList:
    test = eachstate[1]
    State_cases_Lists[test] = []
    
    
for row in out2:
        temp = row[0].split("_")
        State_cases_Lists[temp[0]].append(row)

for key in StateList:
    permoncases = [0 for x in range(17)]
    temp = State_cases_Lists[key[1]]
    for row in temp:
        permoncases[row[1]-1] += row[2]
        
    #to find the peaks
    max = 0
    peak1 = -1
    peak2 = -1
    for i in range(0,9):
        if permoncases[i]>max:
            max = permoncases[i]
            peak1 = i+1
    max = 0       
    for i in range(9,17):
        if permoncases[i]>max:
            max = permoncases[i]
            peak2 = i+1
    
    State_mon_peak.append((key[0],peak1,peak2))
    
    
    overallweekpeak = []
overallmonpeak = []
overallweek = [0 for x in range(129)]
overallmonth = [0 for x in range(17)]
for row in out1:
    overallweek[row[1]-1] += row[2]
    
for row in out2:
    overallmonth[row[1]-1] += row[2]
max = 0
peak1 = -1
peak2 = -1
for i in range(70):
    if overallweek[i]>max:
        max = overallweek[i]
        peak1 = i+1
max = 0       
for i in range(70,129):
    if overallweek[i]>max:
        max = overallweek[i]
        peak2 = i+1

overallweekpeak.append(("India",peak1,peak2))

max = 0
peak1 = -1
peak2 = -1
for i in range(9):
    if overallmonth[i]>max:
        max = overallmonth[i]
        peak1 = i+1
max = 0       
for i in range(9,17):
    if overallmonth[i]>max:
        max = overallmonth[i]
        peak2 = i+1

overallmonpeak.append(("India",peak1,peak2))

temp_dict1 = {"Districtid":[row[0] for row in Districtpeaks],"wave1-weekid":[row[1] for row in Districtpeaks],"wave2-weekid":[row[2] for row in Districtpeaks],
            "wave1-monthid":[row[1] for row in Districtmonpeaks],"wave2-monthid":[row[2] for row in Districtmonpeaks]}
temp_dict2 = {"State-name":[row[0] for row in State_mon_peak],"wave1-weekid":[row[1] for row in State_week_peak],"wave2-weekid":[row[2] for row in State_week_peak],
            "wave1-monthid":[row[1] for row in State_mon_peak],"wave2-monthid":[row[2] for row in State_mon_peak]}
temp_dict3 = {"Country":[row[0] for row in overallweekpeak],"wave1-weekid":[row[1] for row in overallweekpeak],"wave2-weekid":[row[2] for row in overallweekpeak],
            "wave1-monthid":[row[1] for row in overallmonpeak],"wave2-monthid":[row[2] for row in overallmonpeak]}
df = pd.DataFrame(temp_dict1)
df.to_csv('district-peaks.csv', index=False)
df = pd.DataFrame(temp_dict2)
df.to_csv('state-peaks.csv', index=False)
df = pd.DataFrame(temp_dict3)
df.to_csv('overall-peaks.csv', index=False)