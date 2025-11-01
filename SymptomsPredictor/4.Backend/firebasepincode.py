import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import pgeocode
import json 

#intializing firebase
cred = credentials.Certificate("data/symtorconversations-firebase-adminsdk-c7ofx-e46f03e3bb.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#getting andhra and telangana
df=pd.read_csv("data/all_india_PO_list_without_APS_offices_ver2_lat_long.csv")
df=df.fillna(method='ffill')
df=df[(df["statename"]=="TELANGANA" ) | (df["statename"]=="ANDHRA PRADESH" )]

maindict=dict()
count=0
#getting pincode data
for index, row in df.iterrows():
    #print(row['pincode'], row['Taluk'],row['statename'])
    maindict[row['pincode']]=dict()
    #adding city
    maindict[row['pincode']]['city']=row['Taluk']
    #additng state
    maindict[row['pincode']]['state']=row['statename'].lower()
    #adding hospitals
    maindict[row['pincode']]['hospitals']=dict()
    maindict[row['pincode']]['hospitals']['totalHospitals']=1
    maindict[row['pincode']]['hospitals']['sample hospital']={
        "oxygenbeds":10,
        "normalbeds":10
    }

batch = db.batch()
count=0
for pincode,data in maindict.items():
    count+=1
    den_ref = db.collection(u'corona').document(str(pincode))
    batch.set(den_ref, data)
    if count==350:
       print("commited 350 records")
       batch.commit()
       batch = db.batch()
       count=0 

with open("pincode.json", "w") as outfile: 
    json.dump(maindict, outfile)

nomi = pgeocode.Nominatim('IN')