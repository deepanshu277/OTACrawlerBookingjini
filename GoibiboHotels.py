from re import findall
from lxml import html
from time import sleep
from selenium import webdriver
#from pprint import pprint
from datetime import date
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
#from xvfbwrapper import Xvfb
hotets = pd.read_csv('datasetHotelNames/goibibo.csv')
def parse(url, driver):
    searchKey = 'Hotel Vintage Villa' # Change this to your city 
    checkInDate = '07/03/2020' #Format %d/%m/%Y
    checkOutDate = '08/03/2020' #Format %d/%m/%Y
    if driver == 1:
        response = webdriver.Chrome(executable_path = r'C:\Users\TripleR\Downloads\chromedriver_win32\chromedriver.exe')
    if driver == 2:
        response = webdriver.Firefox(executable_path=r'C:\Users\TripleR\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe')
    today = str(date.today())
    #months = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    try:
        response.get(url)
    
        searchKeyElement = response.find_elements_by_xpath('//input[contains(@id,"gosuggest_inputL")]')
        checkInElement = response.find_element_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/input')
        checkOutElement = response.find_elements_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[2]/div/div/input')
        if checkInElement and checkOutElement:
            searchKeyElement[0].send_keys(searchKey)
            sleep(5)
            searchKeyElement[0].send_keys(Keys.TAB)
            sleep(5)
            checkInElement.click()
            dateWidget1 = response.find_element_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div[2]')
            #previous widget
            #preWidget = response.find_elements_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div[2]/div[1]/span[1]')
            nextWidget = dateWidget1.find_elements_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div[2]/div[1]/span')
            checkInDateSplit = checkInDate.split('/')
            checkOutDateSplit = checkOutDate.split('/')
            todaySplit = today.split('-')
            flag = 0
            for ran in range(int(todaySplit[1])-int(checkInDateSplit[1])):
                nextWidget[0].click()
            for x in range(1,6):
                for y in range(1,8):
                    day = dateWidget1.find_element_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div['+str(x)+']/div['+str(y)+']')
                    intday = day.text
                    if len(intday)>0:
                        intday = int(intday)
                    if intday == int(checkInDateSplit[0]):
                        sleep(5)
                        day.click()
                        flag = 1
                        break
                if flag == 1:
                    break
            randomClick = response.find_elements_by_xpath('//h1')
            if randomClick:
                randomClick[0].click()
            sleep(5)
            submitButton = response.find_elements_by_xpath('//button[@type="submit"]')
            submitButton[0].click()
            sleep(5)
        sleep(15)
        hotelNames = []
        prices = []
        parser = html.fromstring(response.page_source,response.current_url)
        hotels = parser.xpath('//aside[@class="roomType"]')
        for hotel in hotels[:]: #Replace 5 with 1 to just get the cheapest hotel
            hotelName = hotel.xpath('.//div/div[1]/p[1]')
            hotelName = hotelName[0].text_content() if hotelName else None
            price = hotel.xpath('.//div/div[2]/div[1]/p[2]/span')
            price = price[0].text_content().replace(",","").strip() if price else None
            '''
            if price==None:
                price = hotel.xpath('//*[@id="app"]/div[1]/div/div/div/div[1]/main/div/section[2]/ol/li[1]/div/div/div/div[2]/div[1]/div[1]/span/span[2]')
                price = price[0].text_content().replace(",","").strip() if price else None
            '''
            price = findall('([\d\.]+)',price) if price else None
            price = price[0] if price else None
            hotelNames.append(str(hotelName))
            prices.append(str(price))
        response.close()
        item = {
                "hotelName":hotelNames,
                "price":prices
        }
        df = pd.DataFrame(item)
        df = pd.DataFrame.drop_duplicates(df)
        df.reset_index(drop = True, inplace = True)
        return df
    except:
        response.close()
df = parse('https://www.goibibo.com/hotels/',1)