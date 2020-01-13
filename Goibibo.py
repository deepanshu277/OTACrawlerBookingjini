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
submitButton = response.find_element_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[3]/div/button')
if searchKeyElement and checkInElement and checkOutElement:
    searchKeyElement[0].send_keys(searchKey)
    checkInElement.click()
    dateWidget = response.find_element_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div[2]')
    #previous widget
    #preWidget = response.find_elements_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div[2]/div[1]/span[1]')
    nextWidget = dateWidget.find_elements_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div[2]/div[1]/span')
    checkInDateSplit = checkInDate.split('/')
    checkOutDateSplit = checkOutDate.split('/')
    todaySplit = today.split('-')
    for ran in range(int(todaySplit[1])-int(checkInDateSplit[1])):
        nextWidget[0].click()
    for x in range(1,6):
        for y in range(1,8):
            day = dateWidget.find_element_by_xpath('//*[@id="Home"]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div['+str(x)+']/div['+str(y)+']')
            intday = day.text
            if len(intday)>0:
                intday = int(intday)
            if intday == int(checkInDateSplit[0]):
                sleep(20)
                day.click()
                print('day clicked')
                break
    randomClick = response.find_elements_by_xpath('//h1')
    if randomClick:
        randomClick[0].click()
    #submitButton.click()
    sleep(15)
"""
        dropDownButton = response.find_elements_by_xpath('//fieldset[contains(@id,"dropdown")]')
        if dropDownButton:
            dropDownButton[0].click()
            priceLowtoHigh = response.find_elements_by_xpath('//li[contains(text(),"low to high")]')
            if priceLowtoHigh:
                priceLowtoHigh[0].click()
                sleep(10)
        

    parser = html.fromstring(response.page_source,response.current_url)
    hotels = parser.xpath('//section[@class="hotel-wrap"]')
    for hotel in hotels[:5]: #Replace 5 with 1 to just get the cheapest hotel
        hotelName = hotel.xpath('.//h3/a')
        hotelName = hotelName[0].text_content() if hotelName else None
        price = hotel.xpath('.//div[@class="price"]/a//ins')
        price = price[0].text_content().replace(",","").strip() if price else None
        if price==None:
            price = hotel.xpath('.//div[@class="price"]/a')
            price = price[0].text_content().replace(",","").strip() if price else None
        price = findall('([\d\.]+)',price) if price else None
        price = price[0] if price else None
        rating = hotel.xpath('.//div[@class="star-rating"]/span/@data-star-rating')
        rating = rating[0] if rating else None
        address = hotel.xpath('.//span[contains(@class,"locality")]')
        address = "".join([x.text_content() for x in address]) if address else None
        locality = hotel.xpath('.//span[contains(@class,"locality")]')
        locality = locality[0].text_content().replace(",","").strip() if locality else None
        region = hotel.xpath('.//span[contains(@class,"locality")]')
        region = region[0].text_content().replace(",","").strip() if region else None
        postalCode = hotel.xpath('.//span[contains(@class,"postal-code")]')
        postalCode = postalCode[0].text_content().replace(",","").strip() if postalCode else None
        countryName = hotel.xpath('.//span[contains(@class,"country-name")]')
        countryName = countryName[0].text_content().replace(",","").strip() if countryName else None

        item = {
                    "hotelName":hotelName,
                    "price":price,
                    "rating":rating,
                    "address":address,
                    "locality":locality,
                    "region":region,
                    "postalCode":postalCode,
                    "countryName":countryName,
        }
        pprint(item)
"""
