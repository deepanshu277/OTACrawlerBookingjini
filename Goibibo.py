# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:21:57 2020

@author: TripleR
"""
from re import findall
from lxml import html
from time import sleep
from selenium import webdriver
from pprint import pprint
from datetime import date
from selenium.webdriver.common.keys import Keys
#from xvfbwrapper import Xvfb


searchKey = "Bhubaneswar" # Change this to your city 
checkInDate = '14/01/2020' #Format %d/%m/%Y
checkOutDate = '15/01/2020' #Format %d/%m/%Y
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
"""
        dropDownButton = response.find_elements_by_xpath('//fieldset[contains(@id,"dropdown")]')
        if dropDownButton:
            dropDownButton[0].click()
            priceLowtoHigh = response.find_elements_by_xpath('//li[contains(text(),"low to high")]')
            if priceLowtoHigh:
                priceLowtoHigh[0].click()
                sleep(10)
"""        

parser = html.fromstring(response.page_source,response.current_url)
hotels = parser.xpath('//section[@class="newSrpCard"]')
for hotel in hotels[:5]: #Replace 5 with 1 to just get the cheapest hotel
    hotelName = hotel.xpath('//*[@id="srpContainer"]/div[2]/div[2]/div/div[2]/div/div[4]/div[1]/div/div/section[1]/div[1]/div[2]/div[1]/a/div/p')
    hotelName = hotelName[0].text_content() if hotelName else None
    price = hotel.xpath('//*[@id="srpContainer"]/div[2]/div[2]/div/div[2]/div/div[4]/div[1]/div/div/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/span[2]/text()')
    price = price[0].text_content().replace(",","").strip() if price else None
    '''
    if price==None:
        price = hotel.xpath('.//div[@class="price"]/a')
        price = price[0].text_content().replace(",","").strip() if price else None
    
    price = findall('([\d\.]+)',price) if price else None
    price = price[0] if price else None
    '''
    item = {
                    "hotelName":hotelName,
                    "price":price
        }
    pprint(item)
