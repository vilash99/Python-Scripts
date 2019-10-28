from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv


mStates = ["al", "ak", "az", "ar", "ca", "co", "ct", "de", "dc", "fl", "ga", "hi", "id", "il",
    "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj", "nm",
    "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy"]


chrome_option = Options()
chrome_option.add_argument("--headless")
chrome_option.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_option, executable_path=r"C:\chromedriver\chromedriver.exe")
#driver = webdriver.Chrome(executable_path=r"C:\chromedriver\chromedriver.exe")
for cState in mStates:
    print("Working URL: " + "https://www.stifel.com/fa/search?state=" + cState)

    try:
        driver.get("https://www.stifel.com/fa/search?state=" + cState)
    except:
        print("Can not open url!")
        break

    #time.sleep(1)
    bsObj = BeautifulSoup(driver.page_source, "html.parser")

    allAgentURL = []
    while True:
        #Get Current Page Link
        allAgentURL = allAgentURL + bsObj.find_all("a", {"class":"search-results-fa-link"})
        try:
            driver.find_element_by_id("btnNextPage").click()
            #time.sleep(2)
            bsObj = BeautifulSoup(driver.page_source, "html.parser")
        except:
            #All Page is clicked next, exit loop
            break

    for currURL in allAgentURL:
        #Open each agent url one-by-one and scrap data
        pURL = "https://www.stifel.com" + currURL["href"]
        driver.get(pURL)
        #time.sleep(1)
        bsObj = BeautifulSoup(driver.page_source, "html.parser")

        #Initlize variable
        aarepname = aarepphn = ""
        aabchadd1 = aabchadd2 = aabchcity = aabchst = aabchzip = ""

        #Extract Agent Name
        try:
            aarepname = bsObj.find("span", {"class":"fa-landing-name"}).text
        except:
            continue
            #print("Error: Name not found!")

        #Extract Phone Number
        try:
            aarepphn = bsObj.find("dd", {"class":"fa-landing-phone-desktop"}).text
        except:
            aarepphn = ""

        #Extact Address
        try:
            tmpAddress = bsObj.find("div", {"class":"col-lg-4 col-md-5 col-sm-6 col-xs-12 fa-landing-address"})
            tmpAddress = tmpAddress.find_all("dd")

            if len(tmpAddress) < 5:
                aabchadd1 = tmpAddress[1].text.strip()
                aabchcity = tmpAddress[2].text.strip()
            else:
                aabchadd1 = tmpAddress[1].text.strip()
                aabchadd2 = tmpAddress[2].text.strip()
                aabchcity = tmpAddress[3].text.strip()
        except:
            tmpAddress = ""

        #Seprate City, State and Zip
        if aabchcity != "":
            aabchst = aabchcity
            aabchzip = aabchcity
            aabchzip = aabchzip.split(", ")[1]
            aabchzip = aabchzip.split(" ")[1]
            aabchcity = aabchcity.split(", ")[0]
            aabchst = aabchst.split(", ")[1]
            aabchst = aabchst.split(" ")[0]

        row = [pURL, aarepname, aarepphn, aabchadd1, aabchadd2, aabchcity, aabchst, aabchzip]
        #Save all data in CSV
        with open(r'D:\tempdata.csv', 'a', newline='') as appendFile:
            writer = csv.writer(appendFile)
            writer.writerow(row)

        appendFile.close()
driver.quit()
#End of Macro
