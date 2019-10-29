from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

  
###Read ASIN from CSV file
with open('D:/Amazon_ASIN.csv') as csv_file:
    
    #Create Headless chrome object
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_option, executable_path=r"C:\chromedriver\chromedriver.exe")

    #Reading CSV file data
    csv_reader = csv.reader(csv_file, delimiter=',')    
    for row in csv_reader:
        mASIN = row[0] 
        pURL = "https://www.amazon.com/dp/" + mASIN
        
        print("Working URL: " + pURL)
        
        try:
            driver.get(pURL)
        except:
            print("Unabe to open URL for ASIN " + mASIN)
            continue
        
        #Wait some for 1 seconds
        time.sleep(1)
        
        bsObj = BeautifulSoup(driver.page_source, "html.parser")        
        
        #Get Amazon Page Title
        try:
            amzTitle = bsObj.find("span", {"id":"productTitle"}).text
            amzTitle = amzTitle.strip()
        except:
            amzTitle = ""
        

        #Get Price
        try:
            amzPrice = bsObj.find("span", {"id":"priceblock_ourprice"}).text
        except:
            amzPrice = ""
        
        
        #Get Image UrL
        try:
            amzURL = bsObj.find("div", {"class":"imgTagWrapper"})
            amzURL = amzURL.find("src")
        except:
            amzURL = ""       
        
        
        #Get Product description
        try:
            amzDesc = bsObj.find("div", {"id":"productDescription"})              
            amzDesc = amzDesc.find("p").text
            amzDesc = amzDesc.strip()
        except:
            amzDesc = ""     
        
        try:
            row = [pURL, amzTitle, amzPrice, amzURL, amzDesc]
            
            #Save all data in CSV
            with open(r'D:\Amazon_Scrap.csv', 'a', newline='') as appendFile:
                writer = csv.writer(appendFile)
                writer.writerow(row)
                
            appendFile.close()


csv_file.close()
driver.quit()
#End of Macro
