import pandas as pd
import json

cowin_data = pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory = False)
covid_data = pd.read_csv("district_wise.csv")

def jointwo(Tab1,Tab2,on):
    res = pd.merge(Tab1,Tab2,how="inner",on = on)
    return res

Intersec = jointwo(cowin_data,covid_data,"District")
removeList = ['Chengalpattu', 'Gaurela Pendra arwahi', 'Nicobars', 'North and Middle Andaman', 'Saraikela-Kharsawan',
'South Andaman', 'Tenkasi', 'Tirupathur', 'Yanam']

for dist in removeList:
    Intersec = Intersec.drop(Intersec[Intersec["District"] == dist].index)

Intersec = Intersec[['State_Code_x','District']].drop_duplicates()
with open("neighbor-districts.json") as n:
    neighbor = json.load(n)

del neighbor['mumbai_city/Q2341660']

for eachkey in neighbor.keys():
    listm = neighbor[eachkey]
    if 'mumbai_city/Q2341660' in listm:
        listm.remove('mumbai_city/Q2341660')

del neighbor['bijapur_district/Q1727570']


for eachkey in neighbor.keys():
    listm = neighbor[eachkey]
    if 'bijapur_district/Q1727570' in listm:
        listm.remove('bijapur_district/Q1727570')

DistrictList = list(neighbor.keys())

def removedust(key):
    if "/" in key:
        key = key[:key.index("/")]
    key = key.replace("_"," ")
    key = key.replace("district","")
    key = key.replace("-"," ")
    key = key.replace("–"," ")
    key = key.strip()
    return key

listone = ['Chengalpattu', 'Gaurela Pendra arwahi', 'Nicobars', 'North and Middle Andaman', 'Seraikela Kharsawan',
'South Andaman', 'Tenkasi', 'Tirupathur', 'Yanam']+['Kheri', 'Konkan division', 'Niwari', 'Noklak', 'Parbhani', 'Pattanamtitta']
listone = [x.lower() for x in listone]
for eachkey in neighbor.keys():
    listm = neighbor[eachkey]
    n = []
    for el in listm:
        el1 = removedust(el)
        if el1 not in listone:
            n.append(el)
    neighbor[eachkey] = n

Cleanedkeys = {}
removeList = ['Kheri', 'Konkan division', 'Niwari', 'Noklak', 'Parbhani', 'Pattanamtitta']+['Chengalpattu', 'Gaurela Pendra arwahi', 'Nicobars', 'North and Middle Andaman', 'Saraikela-Kharsawan',
'South Andaman', 'Tenkasi', 'Tirupathur', 'Yanam']
removeList = [x.lower() for x in removeList]
notmatched = []
morethan1 = []
Frame = Intersec['District'].str.lower()
for name in DistrictList:
    name1 = removedust(name)
    if name1 in removeList:
        continue
    temp = Intersec[Frame[:]==name1]
    if len(temp) == 0:
        notmatched.append(name)
    elif len(temp) == 1:
        Cleanedkeys[name] = (temp.iloc[0,0]+"_"+temp.iloc[0,1])
    else:
        morethan1.append(name)

notmatched.sort()
conversion = pd.read_csv("mismatch.csv")
conversion['neighbor json'] = conversion['neighbor json'].str.strip()
conversion['coviddata'] = conversion['coviddata'].str.strip()

count = 0
for element in notmatched:
    element1 = removedust(element)
    temp = conversion[conversion['neighbor json']==element1]
    if len(temp) == 0:
        continue
    element1 = temp.iloc[0,1]
    row = Intersec[Frame[:]==element1]
    if len(row) == 1:
        Cleanedkeys[element] = row.iloc[0,0]+"_"+row.iloc[0,1]
        
    else:
        morethan1.append(element)
   
morethan1dic = { 'hamirpur/Q2086180':'HP_Hamirpur','hamirpur/Q2019757':'UP_Hamirpur','bilaspur/Q1478939':'HP_Bilaspur','bilaspur/Q100157':'CT_Bilaspur',
               'pratapgarh/Q1585433':'RJ_Pratapgarh','pratapgarh/Q1473962':'UP_Pratapgarh','balrampur/Q1948380':'UP_Balrampur','balrampur/Q16056268':'CT_Balrampur','aurangabad/Q43086':'BR_Aurangabad',
                'aurangabad/Q592942':'MH_Aurangabad'}
result = {}
count = 0
for key in neighbor:
    if key in Cleanedkeys.keys():
        result[Cleanedkeys[key]] = neighbor[key]
        count += 1
    elif key in morethan1dic.keys():
        count += 1
        result[morethan1dic[key]] = neighbor[key]

for key in result:
    newlist = []
    oldlist = result[key]
    for elmt in oldlist:
        if elmt in Cleanedkeys.keys():
            newlist.append(Cleanedkeys[elmt])
        elif elmt in morethan1dic.keys():
            newlist.append(morethan1dic[elmt])
    newlist.sort()
    result[key] = newlist

result1 = {}
for i in sorted(result):
    result1[i]=result[i]

with open('neighbor-districts-modified.json','w') as outputfile:
    json.dump(result1,outputfile)