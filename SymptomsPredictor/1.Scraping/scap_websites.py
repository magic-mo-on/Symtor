"""
This script is used to scrpae the diseases list form 6 different sites

 https://www.nhp.gov.in/disease-a-z/
 https://www.nhsinform.scot/illnesses-and-conditions/a-to-z
 https://www.cdc.gov/az/a.html
 https://timesofindia.indiatimes.com/life-style/health-fitness/health-a-z?tabid=alltab
 https://www.medicinenet.com/diseases_and_conditions/alpha_b.htm
 https://www.seattlechildrens.org/conditions/a-z/

"""

import requests
from bs4 import BeautifulSoup
import time
import re
import pickle
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# start_time = time.time()

nhp_list = list()
nhs_list = list()
cdc_list = list()
tof_list = list()
med_list = list()
sea_list = list()
# https://www.nhp.gov.in/disease-a-z/

print("\n processing https://www.nhp.gov.in/disease-a-z/")
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
diseases = []
for letter in letters:
    URL = 'https://www.nhp.gov.in/disease-a-z/'+letter
    time.sleep(1)
    page = requests.get(URL, verify=False)

    soup = BeautifulSoup(page.content, 'html5lib')
    all_diseases = soup.find('div', class_='all-disease')

    for element in all_diseases.find_all('li'):
        nhp_list.append(element.get_text().lower().strip())
        print(element.get_text().lower().strip())

print("scaraping completed from https://www.nhp.gov.in/disease-a-z/\n")

# https://www.nhsinform.scot/illnesses-and-conditions/a-to-z

url = 'https://www.nhsinform.scot/illnesses-and-conditions/a-to-z'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'lxml')
for heading in soup.find_all("h2"):
    nhs_list.append(heading.get_text().lower().strip())
    print(heading.get_text().lower().strip())

print("\nscaraping completed from https://www.nhsinform.scot/illnesses-and-conditions/a-to-z\n")

# https://www.cdc.gov/az/a.html

for letter in letters:
    url = 'https://www.cdc.gov/az/{}.html'.format(letter)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'lxml')
    pri = 0
    for heading in soup.find_all("a"):
        txt = heading.text.strip()
        if txt == "What is the A-Z Index?":
            break
        if txt == "#":
            pri = 1
            continue
        if pri == 1:
            cdc_list.append(txt.strip().lower())
            print(txt.strip().lower())

print("\nscaraping completed from https://www.cdc.gov/az/\n")


# https://timesofindia.indiatimes.com/life-style/health-fitness/health-a-z?tabid=alltab

url = 'https://timesofindia.indiatimes.com/life-style/health-fitness/health-a-z?tabid=alltab'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'lxml')
for heading in soup.find_all("span", {'class': 'capTxt'}):
    tof_list.append(heading.text.strip().lower())
    print(heading.text.strip().lower())

print("\nscaraping completed from https://timesofindia.indiatimes.com/life-style/health-fitness/health-a-z?tabid=alltab\n")

# https://www.medicinenet.com/diseases_and_conditions/alpha_b.htm
# letters=['c']
for letter in letters:
    url = 'https://www.medicinenet.com/diseases_and_conditions/alpha_'+letter+'.htm'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'lxml')
    count = 0
    pri = 0
    for a in soup.find_all("a"):
        txt = a.text
        if re.match("^[A-z][a-z]-[A-z][a-z]$", txt):
            continue
        if(len(txt) > 0 and txt[-1] == "?"):
            continue
        if(a.text == "Z"):
            pri = 1
            continue
        if(a.text == "A"):
            count += 1
        if count == 2:
            break
        if pri == 1:
            #print(a.text.strip().lower())
            med_list.append(a.text.strip().lower())
            print(a.text.strip().lower())

print("\nscaraping completed from https://www.medicinenet.com/diseases_and_conditions/alpha_c.htm\n")

# https://www.seattlechildrens.org/conditions/a-z/

url = 'https://www.seattlechildrens.org/conditions/a-z/'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'lxml')
special_divs = soup.find_all('a')
pri = 0
for m in special_divs:
    txt = m.text
    if txt == "Z":
        pri = 1
    if (txt == "back to top"):
        continue
    if pri == 1:
        sea_list.append(txt.strip().lower())
        print(txt.strip().lower())
    if txt == "Wound Infection":
        break

print("\nscaraping completed from https://www.seattlechildrens.org/conditions/a-z/\n")

# # ### https://www.sfcdcp.org/infectious-diseases-a-to-z/
# ### response 403
# import requests
# from bs4 import BeautifulSoup
# from urllib.request import Request, urlopen
# hdr = {'User-Agent': 'Mozilla/5.0'}
# url = 'https://www.sfcdcp.org/infectious-diseases-a-to-z/'
# reqs = Request(url,headers=hdr)
# page=urlopen(reqs)
# soup = BeautifulSoup(page, 'lxml')
# sizes = soup.find_all('li')
# pri=0
# print(reqs)
# for tag in soup.find_all('a',{"class":"external-link"}):
#     print (tag.text)


# main code
all_diseases = nhp_list+nhs_list+cdc_list+tof_list+med_list+sea_list
set_diseases = list(set(all_diseases))


print("all diseases:::", len(all_diseases))
print("unique diseases:::", len(set_diseases))
print("www.nhp.gov.in :::", len(nhp_list))
print("www.nhsinform.scot :::", len(nhs_list))
print("www.cdc.gov ::: ", len(cdc_list))
print("timesofindia.indiatimes.com :::", len(tof_list))
print("www.medicinenet.com :::", len(med_list))
print("www.seattlechildrens.org :::", len(sea_list))


with open('../finalData/websites/nhp_list.pkl', 'wb') as f:
    pickle.dump(nhp_list, f)

with open('../finalData/websites/nhsinform_list.pkl', 'wb') as f:
    pickle.dump(nhs_list, f)

with open('../finalData/websites/cdc_list.pkl', 'wb') as f:
    pickle.dump(cdc_list, f)

with open('../finalData/websites/timesofindia_list.pkl', 'wb') as f:
    pickle.dump(tof_list, f)

with open('../finalData/websites/medicinenet_list.pkl', 'wb') as f:
    pickle.dump(med_list, f)

with open('../finalData/websites/seattlechildrens_list.pkl', 'wb') as f:
    pickle.dump(sea_list, f)

# with open('../data/all_diseases.pkl', 'wb') as f:
#     pickle.dump(all_diseases, f)

with open('../finalData/pickle/all_diseases.pkl', 'wb') as f:
    pickle.dump(set_diseases, f)

# print("--- %s seconds ---" % (time.time() - start_time))
