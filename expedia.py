from re import findall
from lxml import html
from time import sleep
from selenium import webdriver
from pprint import pprint
from selenium.webdriver.common.keys import Keys
#from xvfbwrapper import Xvfb

def parse(url):
    searchKey = "Haldia" # Change this to your city 
    checkInDate = '16/01/2020' #Format %d/%m/%Y
    checkOutDate = '17/01/2020' #Format %d/%m/%Y
    response = webdriver.Chrome(r'C:\Users\TripleR\Downloads\chromedriver_win32\chromedriver.exe')
    response.get(url)
    searchKeyElement = response.find_elements_by_xpath('//*[@id="hotel-destination-hp-hotel"]')
    checkInElement = response.find_elements_by_xpath('//*[@id="hotel-checkin-hp-hotel"]')
    checkOutElement = response.find_elements_by_xpath('//*[@id="hotel-checkout-hp-hotel"]')
    submitButton = response.find_elements_by_xpath('//*[@id="gcw-hotel-form-hp-hotel"]/div[10]/label/button')
    if searchKeyElement and checkInElement and checkOutElement:
        searchKeyElement[0].send_keys(searchKey)
        sleep(5)
        searchKeyElement[0].send_keys(Keys.TAB)
        sleep(5)
        checkInElement[0].clear()
        checkInElement[0].send_keys(checkInDate)
        checkOutElement[0].clear()
        checkOutElement[0].send_keys(checkOutDate)
        randomClick = response.find_elements_by_xpath('//h1')
        if randomClick:
            randomClick[0].click()
        sleep(3)
        submitButton[0].click()
        sleep(5)
       
    current_scroll_position, new_height,speed= 0, 1, 8
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        response.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = response.execute_script("return document.body.scrollHeight")
    sleep(5)
    #response.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    parser = html.fromstring(response.page_source,response.current_url)
    hotels = parser.xpath('//div[@class="uitk-card-content uitk-grid uitk-cell all-y-padding-three all-x-padding-three listing-content"]')
    a = 0
    for hotel in hotels[:]: #Replace 5 with 1 to just get the cheapest hotel
        hotelName = hotel.xpath('.//h3')
        hotelName = hotelName[0].text_content() if hotelName else None
        price = hotel.xpath('.//div[2]/div[1]/div[1]/span/span[2]')
        price = price[0].text_content().replace(",","").strip() if price else None
        '''
        if price==None:
            price = hotel.xpath('//*[@id="app"]/div[1]/div/div/div/div[1]/main/div/section[2]/ol/li[1]/div/div/div/div[2]/div[1]/div[1]/span/span[2]')
            price = price[0].text_content().replace(",","").strip() if price else None
        '''
        price = findall('([\d\.]+)',price) if price else None
        price = price[0] if price else None
        
        item = {
                    "hotelName":hotelName,
                    "price":price
        }
        pprint(item)
        a = a + 1
    print(a)
parse('https://www.expedia.co.in')