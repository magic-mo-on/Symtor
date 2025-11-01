import warnings
warnings.filterwarnings("ignore")
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#web dricer config
chromeOptions = webdriver.ChromeOptions() 
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument('disable-infobars')
chromeDriver=webdriver.Chrome(chrome_options=chromeOptions, executable_path=r'Drivers/chromedriver.exe')
firefoxOptions = webdriver.FirefoxOptions()

# firefoxOptions.add_argument("--headless")
firefoxDriver = webdriver.Firefox(options=firefoxOptions,executable_path=r'Drivers\geckodriver.exe')
def closeDriver():
    chromeDriver.close()
    firefoxDriver.close()

# firefoxDriver=chromeDriver
# def closeDriver():
#     chromeDriver.close()

def split_joins(resstr):
    resdict=dict()
    resstr=resstr.splitlines()
    for i in range(0,len(resstr),2):
        resdict[resstr[i]]=resstr[i+1]
    return resdict

def symptoms_join(resstr):
    resdict=dict()
    resstr=resstr.splitlines()
    for i in resstr:
        temp=i.split(":")
        resdict[temp[0].strip()]=temp[1].strip()
    return resdict

# xpath variables
othername_div="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div/div[1]"
extraname_div="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div/div[2]"
symtpoms_div="//*[@id=\"kp-wp-tab-HealthSymptoms\"]/div/div/div/div/div/div/div/div[2]"
diagnose_div="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[4]/div/div[2]/div/div/div/div[3]/div/div/div/div/div/div/div/div[1]/div[1]"
symptom_desc_div="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[4]/div/div[2]/div/div/div/div[3]/div/div/div/div/div/div/div/div[1]/div[2]"
overview_span="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/g-tabs/div/div/a[1]/div[1]/span"
overview_div="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[4]/div/div[1]/div/div/div/div[3]/div[1]/div/div"
occurance_span="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[4]/div/div[1]/div/div/div/div[3]/div[1]/div/div/div/div/div/div/div/div[3]/div[1]/span"
treatments_span="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/g-tabs/div/div/a[3]/div[1]/span"
common_treat_div="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[4]/div/div[3]/div/div/div/g-tabs/div/div"
specialist_span="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/g-tabs/div/div/a[4]/div[1]/span"
specialist_div="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[4]/div/div[4]/div/div/div/div[3]/div[1]/div/div/div/div/div"

#varibales
tab_switch_time=1
page_load_time=2

def scrapper(browser,disease):
    result_dict=dict()
    if browser=="Chrome":
        driver=chromeDriver
    else:
        driver=firefoxDriver
        # driver.maximize_window()
    #print("processing "+disease)
    try:
        #oepning url in google
        driver.get("https://www.google.com/search?q="+disease.lower()+" symptoms")
        #result_dict[disease]=dict()
        time.sleep(2)
    # SYMPTOMS
        otherName=driver.find_elements_by_xpath(othername_div)
        extraName=driver.find_elements_by_xpath(extraname_div)
        diagnoseType=driver.find_element_by_xpath(diagnose_div)
        symptomDesc=driver.find_element_by_xpath(symptom_desc_div)
        symtpoms=driver.find_element_by_xpath(symtpoms_div)
        #result_dict[disease]["otherName"]=otherName[0].text
        ## creating dict with name in google
        otherName=otherName[0].text
        disease=otherName
        result_dict[disease]=dict()
        if extraName[0].text=="":
            result_dict[disease]["extraName"]="None"
        else:
            result_dict[disease]["extraName"]=extraName[0].text
        result_dict[disease]["diagnoseType"]=diagnoseType.text
        result_dict[disease]["symptomDescription"]=symptomDesc.text
        result_dict[disease]["symptoms"]=symptoms_join(symtpoms.text[23:])

    # moving to OVERVIEW
        #click overview
        driver.find_element_by_xpath(overview_span).click()
        time.sleep(page_load_time)
        #find elements
        overview=driver.find_element_by_xpath(overview_div)
        occurance=driver.find_element_by_xpath(occurance_span)
        overview=overview.text[:-130].splitlines()
        slip_index=overview.index(occurance.text)
        result_dict[disease]["occurance"]=occurance.text
        result_dict[disease]["overview"]="\n".join(overview[:slip_index][:12]) 
        result_dict[disease]["notes"]="\n".join(overview[slip_index+2:])

    # moving to TREATMENTS
        driver.find_element_by_xpath(treatments_span).click()
        time.sleep(page_load_time)
        obj=driver.find_element_by_xpath(common_treat_div)
        child_ele=obj.find_elements_by_xpath('.//*')
        child_ele=child_ele[5:]
        tempdict=dict()
        childNum=2
        for r in range(0,len(child_ele),4):
            time.sleep(2)
            child_ele[r].click()
            res=child_ele[r+1]
            #print(res.text)
            time.sleep(2)
            common_treat_details_div="/html/body/div[7]/div/div[9]/div[2]/div/div/div[2]/div[4]/div/div[3]/div/div/div/div/div[{}]/div/div/div/div[3]/div[1]/div/div/div/div/div/div/div/div[1]".format(childNum)
            details=driver.find_element_by_xpath(common_treat_details_div)
            tempdict[res.text]=split_joins(details.text)
            # print(details.text[:-84])
            childNum+=1
        result_dict[disease]["treatments"]=tempdict

    # moving to SPECIALIST
        #click specialist
        driver.find_element_by_xpath(specialist_span).click()
        time.sleep(page_load_time)
        specialists=driver.find_element_by_xpath(specialist_div)
        specialists=split_joins(specialists.text[:-130])
        result_dict[disease]["specialists"]=specialists
    #returning resultdict
        return result_dict

    except:
        if "symptoms" in result_dict.keys():
            return result_dict
        return None