import json
import pandas as pd
from datetime import datetime
import datetime as d
import dateutil.relativedelta as relativedelta
import math

cowindata = pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory = False)
censusdata = pd.DataFrame(pd.read_excel('DDW_PCA0000_2011_Indiastatedist.xlsx'))
censusdata['Name'] = censusdata['Name'].str.replace("&","and").str.strip()
censusdata['Name'] = censusdata['Name'].str.strip()
censusdata['Name'] = censusdata['Name'].str.lower()
cowindata['State'] = cowindata['State'].str.lower()
censusdata = censusdata[['Name','TRU','TOT_P']]

Statelist = list(set(cowindata['State'].dropna()))
Names = list(set(censusdata['Name'].dropna()))
Statelist
count = 0
for i in Statelist:
    if i in Names:
        count+=1

censusdata = censusdata[(censusdata['TRU'] == "Total")]
censusdata[censusdata['Name'] == "nct of delhi"]

out = []
permanent = d.datetime(2021, 8, 14)
for state in Statelist:
    if state not in Names:
        continue
    temp1 = censusdata[(censusdata['Name']==state) & (censusdata['TRU']=="Total")]
    totalpop = temp1.iloc[0,2]
    perstate = cowindata[cowindata['State']==state]
    perstate = perstate[['07-08-2021.3','14-08-2021.3']]
    vaccinatedweek = 0
    vaccinated = 0
    for i in range(len(perstate)):
        vaccinatedweek += (int(perstate.iloc[i,1])-int(perstate.iloc[i,0]))
        vaccinated += int(perstate.iloc[i,1])
    left = totalpop - vaccinated
    rateofvaccination = vaccinatedweek/7
    time = math.ceil(left/rateofvaccination)
    days = d.timedelta(days = time)
    finaldate = permanent+days
    resultdate = str(finaldate.day)+"/"+str(finaldate.month)+"/"+str(finaldate.year)
    out.append((state.upper(),left,rateofvaccination,resultdate))
    
statecen = "nct of delhi"
temp1 = censusdata[(censusdata['Name']==statecen) & (censusdata['TRU']=="Total")]
totalpop = temp1.iloc[0,2]
perstate = cowindata[cowindata['State']=="delhi"]
perstate = perstate[['07-08-2021.3','14-08-2021.3']]
vaccinatedweek = 0
vaccinated = 0
for i in range(len(perstate)):
    vaccinatedweek += (int(perstate.iloc[i,1])-int(perstate.iloc[i,0]))
    vaccinated += int(perstate.iloc[i,1])
left = totalpop - vaccinated
rateofvaccination = vaccinatedweek/7
time = math.ceil(left/rateofvaccination)
days = d.timedelta(days = time)
finaldate = permanent+days
resultdate = str(finaldate.day)+"/"+str(finaldate.month)+"/"+str(finaldate.year)
out.append(("Delhi",left,rateofvaccination,resultdate))

out.sort()
temp_dict1 = {"Stateid":[row[0] for row in out] , "populationleft":[row[1] for row in out], "rateofvaccination":[row[2] for row in out],"date":[row[3] for row in out]}
df = pd.DataFrame(temp_dict1)
df.to_csv('complete-vaccination.csv', index=False)
