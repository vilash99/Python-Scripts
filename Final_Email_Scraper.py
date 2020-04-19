####Get Email from website####
# Step 1: Find string in current url home page if there is email text, if found
#         Then save it and continue to step 3
# Step 2: If not found then goto contact page and check same.
# Step 3: Save data and move to next url.

import mechanize
from bs4 import BeautifulSoup
import csv
import time
import re

IP_csv = r'D:\emailData.csv'
OP_csv = r'D:\Scraped_Email.csv'

def SaveDataInCSV(mRow):    
    with open(OP_csv, 'a', newline='') as appendFile:
        writer = csv.writer(appendFile)
        writer.writerow(mRow)
    appendFile.close() 


def checkProperEmail(soup, emailFormat):
    try:
        foundEmail = str(soup.find(string=re.compile("@"+emailFormat, re.IGNORECASE)))
        
        if foundEmail.find('href="mailto:') >= 0:
            foundEmail = foundEmail.split('href="mailto:')[1]
    except:
        foundEmail = "None"
    
    return foundEmail
     

def checkUnknowDomainEmail(soup):
    try:
        #foundAllEmail = soup.find_all(string=re.compile("\S+@\S+", re.IGNORECASE))
        foundAllEmail = soup.find_all(string=re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", re.IGNORECASE))
        
    except:
        return "None"
    
    #Loop throuh all found email and get less length email
    for e in foundAllEmail:
        if str(e).find('href="mailto:') >= 0:
            return str(e).split('href="mailto:')[1]
        elif len(str(e)) <= 500:
            return str(e)
    return "None"
    
            
            
# Browser
br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


###Open CSV file to get website url and email format
with open(IP_csv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    for row in csv_reader:
        pageURL = row[0] 
        pageEmail = ""
        mainURL = pageURL       
        
        
        try:
            page_url = br.open(pageURL)
        except:             
            SaveDataInCSV([mainURL, pageURL, "NOT FOUND"])
            continue        
        
        soup = BeautifulSoup(br.response().read())
        
        #Get refrshed Page URL
        pageURL = br.geturl()
        print("Running URL:", pageURL)
        
        
        ##Remove any extra data after /
        pageURL = pageURL.replace("://", "XEFXR")
        pageURL = pageURL.split("/")[0]
        pageURL = pageURL.replace("XEFXR", "://")
        
        pageEmail = pageURL.replace("www.", "")
        pageEmail = pageEmail.replace("http://", "")
        pageEmail = pageEmail.replace("https://", "")
        pageEmail = pageEmail.replace("/", "")
        
        
        ##Check if there is email in current page
        foundEmail = checkProperEmail(soup, pageEmail)          
        
        ##Check if there is email which have diffrent domain name
        if foundEmail == "None":
            foundEmail = checkUnknowDomainEmail(soup)                
        
        ###Email not found in main page. Try to look contact us page and find there    
        if foundEmail == "None":
            #Search Contact us page and open URL
            try:
                contactUsURL = soup.find("a", href=re.compile("contact", re.IGNORECASE))
                if contactUsURL['href'].find("http") >= 0:
                    contactUsURL = contactUsURL['href']                    
                else:
                    if contactUsURL['href'].startswith("/"):
                        contactUsURL = pageURL + contactUsURL['href']                
                    else:
                        contactUsURL = pageURL + "/" + contactUsURL['href']                
            except:            
                #Check if contact us page is not found in webpage                
                SaveDataInCSV([mainURL, pageURL, "NOT FOUND"])
                continue
            
            ##Open contact us page, if found
            try:
                page_url = br.open(contactUsURL)
            except:                          
                SaveDataInCSV([mainURL, pageURL, "NOT FOUND"])
                continue            
            
            soup = BeautifulSoup(br.response().read())
            
            ##Check if there is email in current page
            foundEmail = checkProperEmail(soup, pageEmail)                
        
            ##Check if there is email which have diffrent domain name
            if foundEmail == "None":
                foundEmail = checkUnknowDomainEmail(soup)                   
            
            
            if foundEmail == "None":                   
                SaveDataInCSV([mainURL, pageURL, "NOT FOUND"])
            else:
                #Remove other encode
                foundEmail = foundEmail.encode('ascii', 'ignore')
                SaveDataInCSV([mainURL, pageURL, foundEmail])
        else:   
            #Remove other encode
            foundEmail = foundEmail.encode('ascii', 'ignore')
            SaveDataInCSV([mainURL, pageURL, foundEmail])            
            
        
        #Wait for 1 second
        #time.sleep(1)