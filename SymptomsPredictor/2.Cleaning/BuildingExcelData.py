#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from itertools import combinations


# In[10]:


with open('../finalData/pickle/diseases_symptoms_cleaned.pickle', 'rb') as handle:
    diseases_symptoms_cleaned = pickle.load(handle)
with open('../finalData/pickle/new_symptoms.pickle', 'rb') as handle:
    new_symptoms = pickle.load(handle)
with open('../finalData/pickle/symptom_match.pickle', 'rb') as handle:
    symptom_match = pickle.load(handle)


# In[11]:


total_symptoms = new_symptoms
total_symptoms = list(total_symptoms)
total_symptoms.sort()
total_symptoms=['label_dis']+total_symptoms


# In[12]:


len(total_symptoms)


# In[13]:


f = open("../Analyze/4.disease symptoms length.txt", "w")
for dis in sorted(diseases_symptoms_cleaned.keys()):
    f.write(dis+" --> "+str(len(diseases_symptoms_cleaned[dis]))+"\n")
f.close()


# # initializing data frame

# In[14]:


df_comb = pd.DataFrame(columns=total_symptoms)
df_norm = pd.DataFrame(columns=total_symptoms)


# In[7]:


def write(df_norm,df_comb):
    df_norm.to_pickle("picklefiles/df_norm.pkl")
    df_comb.to_pickle("picklefiles/df_comb.pkl")


# In[ ]:


count=0
for key, values in diseases_symptoms_cleaned.items():
    print(key)
    count+=1
    key = str.encode(key).decode('utf-8')
    tmp = []
    
    # For similar symptoms, replace with the value in dictionary
    for symptom in values:
        if symptom in symptom_match.keys():
            tmp.append(symptom_match[symptom])
            # print(symptom)
        else:
            tmp.append(symptom)
            
    values = list(set(tmp))
    diseases_symptoms_cleaned[key] = values
    
    # Populate row for normal
    row_norm = dict({x:0 for x in total_symptoms})
    for sym in values:
        row_norm[sym] = 1
    row_norm['label_dis']=key
    df_norm = df_norm.append(pd.Series(row_norm), ignore_index=True)
         
    # Populate rows for combination dataset
    for comb in range(1, len(values) + 1):
        for subset in combinations(values, comb):
            row_comb = dict({x:0 for x in total_symptoms})
            for sym in list(subset):
                row_comb[sym]=1
            row_comb['label_dis']=key
            df_comb = df_comb.append(pd.Series(row_comb), ignore_index=True)
    if count==10:
        write(df_norm,df_comb)
        count=0
write(df_norm,df_comb)


# In[15]:


print(df_comb.shape)
print(df_norm.shape)


# In[16]:


df_comb.to_csv("../dis_sym_dataset_comb.csv",index=None)
df_norm.to_csv("../dis_sym_dataset_norm.csv",index=None)


# In[ ]:




