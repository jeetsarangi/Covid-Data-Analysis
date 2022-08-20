import json
import pandas as pd
from datetime import datetime
import datetime as d
import dateutil.relativedelta as relativedelta

cowindata = pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory = False)
cowindata = cowindata[['State','District_Key','District','01-09-2021.8','01-09-2021.9']]

TargetDistrict = list(set(cowindata['District_Key'].dropna()))

out = []
for dist in TargetDistrict:
    temp = cowindata[cowindata['District_Key'] == dist]
    out.append((temp.iloc[0,0],temp.iloc[0,1],temp.iloc[0,2],int(temp.iloc[0,3]),int(temp.iloc[0,4])))

Districtwise = []
for row in out:
    if row[3] == 0:
        ratio = float('inf')
    else:
        ratio = row[4]/row[3]
    Districtwise.append((row[1],ratio))

Statelist = list(set([row[0] for row in out]))
Statewise = []
for state in Statelist:
    tot_cs = 0
    tot_cv = 0
    for row in out:
        if row[0] == state:
            tot_cs += row[4]
            tot_cv += row[3]
    if tot_cv == 0:
        ratio = float('inf')
    else:
        ratio = tot_cs/tot_cv
    Statewise.append((state,ratio))

overall = []
totCS = 0
totCV = 0
for row in out:
    totCS += row[4]
    totCV += row[3]
overall.append(("India",totCS/totCV))

Districtwise = sorted(Districtwise, key=lambda x: x[1])
Statewise = sorted(Statewise, key=lambda x: x[1])

temp_dict1 = {"Districtid":[row[0] for row in Districtwise] , "vaccineratio":[row[1] for row in Districtwise]}
temp_dict2 = {"Stateid":[row[0] for row in Statewise] , "vaccineratio":[row[1] for row in Statewise]}
temp_dict3 = {"Country":[row[0] for row in overall] , "vaccineratio":[row[1] for row in overall]}
df = pd.DataFrame(temp_dict1)
df.to_csv('District-vaccine-type-ratio.csv', index=False)
df = pd.DataFrame(temp_dict2)
df.to_csv('State-vaccine-type-ratio.csv', index=False)
df = pd.DataFrame(temp_dict3)
df.to_csv('Overall-vaccine-type-ratio.csv', index=False)
