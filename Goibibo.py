from re import findall
from lxml import html
from time import sleep
from selenium import webdriver
from pprint import pprint
from datetime import date
from selenium.webdriver.common.keys import Keys
#from xvfbwrapper import Xvfb


searchKey = "Bhubaneswar" # Change this to your city 
checkInDate = '15/01/2020' #Format %d/%m/%Y
checkOutDate = '16/01/2020' #Format %d/%m/%Y
today = str(date.today())
months = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
response = webdriver.Chrome(r'C:\Users\TripleR\Downloads\chromedriver_win32\chromedriver.exe')
response.get('https://www.goibibo.com/hotels/')
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

current_scroll_position, new_height,speed= 0, 1, 8
while current_scroll_position <= new_height:
    current_scroll_position += speed
    response.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
    new_height = response.execute_script("return document.body.scrollHeight")
sleep(5)

parser = html.fromstring(response.page_source,response.current_url)
hotels = parser.xpath('//div[@class="width100 fl"]')
for hotel in hotels[:]:
    hotelName = hotel.xpath('./div[1]/div/a/div/p')
    hotelName = hotelName[0].text_content() if hotelName else None
    price = hotel.xpath('./div[1]/div[1]/div/div/div/span[1]/text()')

    if price==None:
        price = hotel.xpath('./div[1]/div[1]/div/div/div/span/text()')
    
    #price = findall('([\d\.]+)',price) if price else None
    price = price[0] if price else None
    
    item = {
                    "hotelName":hotelName,
                    "price":price
        }
    pprint(item)
