import json
import pandas as pd
from datetime import datetime
import datetime as d
import dateutil.relativedelta as relativedelta
import numpy as np

cowindata = pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory = False)
censusdata = pd.DataFrame(pd.read_excel('DDW_PCA0000_2011_Indiastatedist.xlsx'))
cowindata = cowindata[['State','District_Key','District','01-09-2021.5','01-09-2021.6']]
censusdata = censusdata[['Level','Name','TRU','TOT_P','TOT_M','TOT_F']]
cowindata['District'] = cowindata['District'].str.replace("District","").str.strip()
censusdata['Name'] = censusdata['Name'].str.strip()

cowindist =list(set(cowindata['District'].dropna()))
censusdist = list(set(censusdata['Name'].dropna()))
count = 0
l = []
for i in censusdist:
    if i in cowindist:
        count+=1
    else:
        l.append(i)

changes = {
    'Mahbubnagar':'Mahabubnagar',
    'Rangareddy':'Ranga Reddy',
    'Sri Potti Sriramulu Nellore':'S.P.S. Nellore',
    'Y.S.R.':'Y.S.R. Kadapa',
    'Dibang Valley':'Upper Dibang Valley',
    'Kaimur (Bhabua)':'Kaimur',
    'Pashchim Champaran':'West Champaran',
    'Purba Champaran':'East Champaran',
    'Janjgir - Champa':'Janjgir Champa',
    'Ahmadabad':'Ahmedabad',
    'Banas Kantha':'Banaskantha',
    'Dohad':'Dahod',
    'Kachchh':'Kutch',
    'Mahesana':'Mehsana',
    'Panch Mahals':'Panchmahal',
    'Sabar Kantha':'Sabarkantha',
    'The Dangs':'Dang',
    'Lahul & Spiti':'Lahaul & Spiti',
    'Gurgaon':'Gurugram',
    'Mewat':'Nuh',
    'Kodarma':'Koderma',
    'Pashchimi Singhbhum':'West Singhbhum',
    'Purbi Singhbhum':'East Singhbhum',
    'SaraikelaKharsawan':'',
    'Badgam':'Budgam',
    'Bandipore':'Bandipora',
    'Baramula':'Baramulla',
    'Shupiyan':'Shopiyan',
    'Bagalkot':'Bagalkote',
    'Bangalore':'Bengaluru',
    'Bangalore Rural':'Bengaluru Rural',
    'Belgaum':'Belagavi',
    'Bellary':'Ballari',
    'Bijapur':'Vijayapura',
    'Chamarajanagar':'Chamarajanagara',
    'Chikmagalur':'Chikkamagaluru',
    'Gulbarga':'Kalaburagi',
    'Mysore':'Mysuru',
    'Shimoga':'Shivamogga',
    'Tumkur':'Tumakuru',
    'Ahmadnagar':'Ahmednagar',
    'Bid':'Beed',
    'Buldana':'Buldhana',
    'Gondiya':'Gondia',
    'Khandwa (East Nimar)':'Khandwa',
    'Khargone (West Nimar)':'Khargone',
    'Narsimhapur':'Narsinghpur',
    'Anugul':'Angul',
    'Baleshwar':'Balasore',
    'Baudh':'Boudh',
    'Debagarh':'Deogarh',
    'Jagatsinghapur':'Jagatsinghpur',
    'Jajapur':'Jajpur',
    'Firozpur':'Ferozepur',
    'Muktsar':'Sri Muktsar Sahib',
    'Sahibzada Ajit Singh Nagar':'S.A.S. Nagar',
    'Chittaurgarh':'Chittorgarh',
    'Dhaulpur':'Dholpur',
    'Jalor':'Jalore',
    'Jhunjhunun':'Jhunjhunu',
    'Kanniyakumari':'Kanyakumari',
    'The Nilgiris':'Nilgiris',
    'Allahabad':'Prayagraj',
    'Bara Banki':'Barabanki',
    'Faizabad':'Ayodhya',
    'Jyotiba Phule Nagar':'Amroha',
    'Kanshiram Nagar':'Kasganj',
    'Kheri':'Lakhimpur Kheri',
    'Mahamaya Nagar':'Hathras',
    'Mahrajganj':'Maharajganj',
    'Sant Ravidas Nagar (Bhadohi)':'Bhadohi',
    'Garhwal':'Pauri Garhwal',
    'Hardwar':'Haridwar',
    'Darjiling':'Darjeeling',
    'Haora':'Howrah',
    'Hugli':'Hooghly',
    'Koch Bihar':'Cooch Behar',
    'Maldah':'Malda',
    'North Twenty Four Parganas':'North 24 Parganas',
    'Puruliya':'Purulia',
    'South Twenty Four Parganas':'South 24 Parganas',
    'North West':'North West Delhi',
    'North':'North Delhi',
    'North East':'North East Delhi',
    'East':'East Delhi',
    'Central':'Central Delhi',
    'West':'West Delhi',
    'South West':'South West Delhi',
    'South':'South Delhi'
    
}

censusdist = list(set(censusdata['Name'].dropna()))
cowindist =list(set(cowindata['District'].dropna()))
left = []
out = []
for dist in censusdist:
    
    if dist not in cowindist:
        left.append(dist)
        continue
    
    temp1 = censusdata[(censusdata['Name'] == dist) & (censusdata['TRU'] == 'Total')]
    temp2 = cowindata[cowindata['District'] == dist]
    
    out.append((temp2.iloc[0,0],temp2.iloc[0,1],int(temp2.iloc[0,3]),int(temp2.iloc[0,4]),int(temp1.iloc[0,4]),int(temp1.iloc[0,5])))
    
    
for dist in left:
    if dist in changes.keys():
        dist1 = changes[dist]
        temp1 = censusdata[(censusdata['Name'] == dist) & (censusdata['TRU'] == 'Total')]
        temp2 = cowindata[cowindata['District'] == dist1]
        if dist1 not in cowindist:
            continue

        out.append((temp2.iloc[0,0],temp2.iloc[0,1],int(temp2.iloc[0,3]),int(temp2.iloc[0,4]),int(temp1.iloc[0,4]),int(temp1.iloc[0,5])))

districtwise = []
test = []
for row in out:
    
    vr = row[3]/row[2]
    pr = row[5]/row[4]
    rr = vr/pr
    
    districtwise.append((row[1],vr,pr,rr))

Statelist = list(set([row[0] for row in out]))
Statewise = []
for state in Statelist:
    vm = 0
    vf = 0
    tm = 0
    tf = 0
    for row in out:
        if row[0] == state:
            vm+=row[2]
            vf+=row[3]
            tm+=row[4]
            tf+=row[5]
    if vm != 0 and tm!=0:
        vr = vf/vm
        pr = tf/tm
        rr = vr/pr
    Statewise.append((state,vr,pr,rr))
    
overall = []
vm = 0
vf = 0
tm = 0
tf = 0
for row in out:
    vm+=row[2]
    vf+=row[3]
    tm+=row[4]
    tf+=row[5]
if vm != 0 and tm!=0:
        vr = vf/vm
        pr = tf/tm
        rr = vr/pr
overall.append(("India",vr,pr,rr))

districtwise = sorted(districtwise, key=lambda x: x[3])
Statewise = sorted(Statewise, key=lambda x: x[3])
overall = sorted(overall,key = lambda x:x[3])

temp_dict1 = {"Districtid":[row[0] for row in districtwise] , "vaccinationratio":[row[1] for row in districtwise],"populationratio":[row[2] for row in districtwise],
              "ratioofratios":[row[3] for row in districtwise]}
temp_dict2 = {"State":[row[0] for row in Statewise] , "vaccinationratio":[row[1] for row in Statewise],"populationratio":[row[2] for row in Statewise],
              "ratioofratios":[row[3] for row in Statewise]}
temp_dict3 = {"Country":[row[0] for row in overall] , "vaccinationratio":[row[1] for row in overall],"populationratio":[row[2] for row in overall],
              "ratioofratios":[row[3] for row in overall]}
df = pd.DataFrame(temp_dict1)
df.to_csv('District-vaccination-population-ratio.csv', index=False)
df = pd.DataFrame(temp_dict2)
df.to_csv('State-vaccination-population-ratio.csv', index=False)
df = pd.DataFrame(temp_dict3)
df.to_csv('Overall-vaccination-population-ratio.csv', index=False)

