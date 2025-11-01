from ScrapperLib import scrapper,closeDriver
import pickle 
import json
import time

start = time.time()
# read diseases from all_diseases pickle
with open('../finalData/pickle/all_diseases.pkl', 'rb') as f:
    allDiseases=pickle.load(f)
allDiseases.sort()

# result_dict=dict()
with open('../finalData/UncleandiseaseData.json', 'rb') as f:
    result_dict=json.load(f)
count_disease=dict()
completedList=list()
errorList=list()
browser="Chrome"

for disease in allDiseases:
    count_disease[disease]=0

count=1
# disease=0
with open('../finalData/pickle/breakpoint.pkl', 'rb') as f:
    disease=pickle.load(f)
allDiseaseseLength=len(allDiseases)

print("\ntotal mined diseases until now:",len(result_dict))
print("\ncontinuing from",disease,allDiseases[disease])
print("\n")

def writeData():
    # with open("demoData2.json", "w") as outfile: 
    #     json.dump(result_dict, outfile)
    with open('../finalData/UncleandiseaseData.json', "w") as outfile: 
        json.dump(result_dict, outfile)
    with open('../finalData/pickle/completedList.pkl', 'wb') as f:
        pickle.dump(completedList, f)
    with open('../finalData/pickle/errorList.pkl', 'wb') as f:
        pickle.dump(errorList, f)
    with open('../finalData/pickle/breakpoint.pkl', 'wb') as f:
        pickle.dump(disease, f)

while(disease<allDiseaseseLength):
    #print(allDiseases[disease])
    if count_disease[allDiseases[disease]]<=1:
        result=scrapper(browser,allDiseases[disease])
        if result!=None:
            completedList.append(allDiseases[disease])
            # disease=result[1]
            # result=result[0]
            # result[allDiseases[disease]]['broswer']=browser
            result_dict.update(result)
            print("\n----------->",list(result.keys())[0],"  ---->",len(result_dict))
            disease+=1
            count+=1
        else:
            # disease+=1
            # continue
            count_disease[allDiseases[disease]]+=1
            if browser=="Chrome":
                browser="Firefox"
            else:
                browser="Chrome"
    else:
        errorList.append(allDiseases[disease])
        print(allDiseases[disease],disease)
        if browser=="Chrome":
            browser="Firefox"
        else:
            browser="Chrome"
        disease+=1
        count+=1

    if count==20:
        writeData()
        print("\n---------written data----------\n")
        count=0
        # break
writeData()
closeDriver()

end = time.time()
print("time elapsed:",end - start)