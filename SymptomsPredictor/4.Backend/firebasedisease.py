import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle
import json

#intializing firebase
cred = credentials.Certificate("data/symtorconversations-firebase-adminsdk-c7ofx-e46f03e3bb.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
db = firestore.client()

users_ref = db.collection(u'diseases')
docs = users_ref.stream()

# count=0
# for doc in docs:
#     # print(f'{doc.id} => {doc.to_dict()}')
#     print(doc.id)
#     count+=1
# print(count)

with open('../data/diseases_symptoms_cleaned.pickle', 'rb') as handle:
    diseases_symptoms_cleaned = pickle.load(handle)

with open('../data/FinalDisease.json') as json_file:
    result_dict = json.load(json_file)

batch = db.batch()
count=0

for key,value in diseases_symptoms_cleaned.items():
    count+=1
    data=result_dict[key]
    data['rawSymptoms']=data['symtpoms']
    data['symptoms']=value
    del data['symtpoms']
    if "/" in key:
        key= key.replace("/", "\\")
    doc_ref = db.collection(u'diseases').document(key)
    doc_ref.set(data)
    if count==350:
        print("commited 350 records")
        batch.commit()
        batch = db.batch()
        count=0
