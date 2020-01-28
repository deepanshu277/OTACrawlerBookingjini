from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random 
from time import sleep
import expedia
import Goibibo
import Hotelsdotcom
import pandas as pd
from tkinter import *

window = Tk()
window.columnconfigure(0, weight=1)
window.title("Bookingjini")
window.geometry('500x300')
window.configure(bg="orange red")

lbl = Label(window, text="Location")
lbl.grid(column=0, row=0)

txt1 = Entry(window,width=10)
txt1.grid(column=1, row=0)

lb2 = Label(window, text="Check-In")
lb2.grid(column=0, row=1)

txt2 = Entry(window,width=10)
txt2.grid(column=1, row=1)

lb3 = Label(window, text="Check-Out")
lb3.grid(column=0, row=2)

txt3 = Entry(window,width=10)
txt3.grid(column=1, row=2)

def scrape():
    searchKey = txt1.get() # Change this to your city 
    checkInDate = txt2.get() #Format %d/%m/%Y
    checkOutDate = txt3.get() #Format %d/%m/%Y

    inputs = [searchKey, checkInDate, checkOutDate]

    ua = UserAgent() # From here we generate a random user agent
    proxies = [] # Will contain proxies [ip, port]
    otas = ['https://www.expedia.co.in','https://in.hotels.com','https://www.goibibo.com/hotels/']
    '''
    Retrieve latest proxies
    '''
    def proxyGenerator():
        proxies_req = Request('https://www.sslproxies.org/')
        proxies_req.add_header('User-Agent', ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')
        
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')
        
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
          })
    '''
    errorProxies = []
    for proxy in proxies:
        req = Request('http://icanhazip.com')
        req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
        try:
            my_ip = urlopen(req).read().decode('utf8')
            print('#' + str(1) + ': ' + my_ip)
        except: # If error, delete this proxy and find another one
            errorProxies.append(proxy)
            print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
    
    proxies = [x for x in proxies if x not in errorProxies]
    '''
    proxyGenerator()
    def random_proxy():
        return random.randint(0, len(proxies) - 1)
    
    '''
    Crawling through the wepages in otas
    '''
    df = []
    for url in otas:
        proxy_index = random_proxy()
        proxy = proxies[proxy_index]
        while True: 
            driver = random.choice([1, 2])
            req = Request('http://icanhazip.com')
            req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
            try:
                my_ip = urlopen(req).read().decode('utf8')
                print('#' + str(1) + ': ' + my_ip)
                temp = otas.index(url)
                if temp == 0:
                    df = expedia.parse(url, proxy, driver, inputs)
                    if len(df) > 1:
                        df.to_csv('expedia.csv')
                        df = []
                        break
                if temp == 1:
                    df = Hotelsdotcom.parse(url, proxy, driver, inputs)
                    if len(df) > 1:
                        df.to_csv('Hotelsdotcom.csv')
                        df = []
                        break
                if temp == 2:
                    df = Goibibo.parse(url, proxy, driver, inputs)
                    if len(df) > 1:
                        df.to_csv('goibibo.csv')
                        df = []
                        break
            except: # If error, delete this proxy and find another one
                #del proxies[proxy_index]
                #print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
                del proxies[proxy_index]
                try:
                    proxy_index = random_proxy()
                except:
                    proxyGenerator()
                proxy = proxies[proxy_index]
        sleep(random.choice([1,2,3,4]))

btn = Button(window, text="Scrape", command=scrape)
btn.grid(column=1, row=3)

window.mainloop()