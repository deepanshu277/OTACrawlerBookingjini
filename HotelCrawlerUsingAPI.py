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
from PIL import Image, ImageTk
from datetime import timedelta, date


background_color= "orange red"
window_size = (500, 300)
logo_path = "capture.png"


class Application(Frame):

    def __init__(self):
        super().__init__()
        global background_color, logo_path
        self.location = None #1st input, Location
        self.check_in = None #2nd input, Check-In
        self.check_out = None #3rd input, Check-Out
        self.bgcolor = background_color #background color
        self.logo_path = logo_path #path of the image 
        self.label_width = 8 #width for labels
        self.entry_width = 10 #width for entry boxes, may not work as intended
        self.logo_size = (124, 70) #define a tuple with width, height for logo

    #this will be the scrape function, do anything in here. Will be invoked when button is pressed
    #use the text input referring to the variables names stated above in _init_()
    def scrape(self):
        searchKey = self.location.get() # Change this to your city 
        startDate = self.check_in.get() #Format %d/%m/%Y
        endDate = self.check_out.get() #Format %d/%m/%Y
        startDate = startDate.split('/')
        endDate = endDate.split('/')
    
        ua = UserAgent() # From here we generate a random user agent
        #otas = ['https://www.expedia.co.in','https://in.hotels.com','https://www.goibibo.com/hotels/']
        otas = ['https://www.goibibo.com/hotels/']
        '''
        Gives a range of dates
        '''
        dateRange = []
        def daterange(date1, date2):
            for n in range(int ((date2 - date1).days)+1):
                yield date1 + timedelta(n)
        
        startDate = date(int(startDate[2]), int(startDate[1]), int(startDate[0]))
        endDate = date(int(endDate[2]), int(endDate[1]), int(endDate[0]))
        for dt in daterange(startDate, endDate):
            dateRange.append(dt.strftime("%d/%m/%Y"))
        '''
        Retrieve latest proxies
        '''
        def proxyGenerator():
            proxies_req = Request('http://list.didsoft.com/get?email=rajatavdutta@gmail.com&pass=r6gt4j&pid=http3000&showcountry=no&https=yes')
            proxies_req.add_header('User-Agent', ua.random)
            proxies_doc = urlopen(proxies_req).read().decode('utf8')
            proxies = proxies_doc.split('\n')
            return proxies
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
        proxies = proxyGenerator()
        def random_proxy():
            return random.randint(0, len(proxies) - 1)
        
        '''
        Crawling through the wepages in otas
        '''
        df = []
        for oneDate in dateRange:
            inputs = [searchKey, oneDate, '01/05/2020']
            for url in otas:
                proxy_index = random_proxy()
                proxy = proxies[proxy_index]
                while True: 
                    #driver = random.choice([1, 2])
                    driver = 1
                    req = Request('http://icanhazip.com')
                    req.set_proxy(proxy, 'http')
                    try:
                        my_ip = urlopen(req).read().decode('utf8')
                        print('#' + str(1) + ': ' + my_ip)
                        temp = otas.index(url)
                        if temp == 1:
                            df = expedia.parse(url, proxy, driver, inputs)
                            if len(df) > 1:
                                df.to_csv('datasetHotelNames/expedia'+oneDate+'.csv')
                                df = []
                                break
                        if temp == 2:
                            df = Hotelsdotcom.parse(url, proxy, driver, inputs)
                            if len(df) > 1:
                                df.to_csv('datasetHotelNames/Hotelsdotcom'+oneDate+'.csv')
                                df = []
                                break
                        if temp == 0:
                            df = Goibibo.parse(url, proxy, driver, inputs)
                            if len(df) > 1:
                                df.to_csv('datasetHotelNames/goibibo'+oneDate+'.csv')
                                df = []
                                break
                    except: # If error, delete this proxy and find another one
                        #del proxies[proxy_index]
                        #print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
                        del proxies[proxy_index]
                        try:
                            proxy_index = random_proxy()
                        except:
                            proxies = proxyGenerator()
                        proxy = proxies[proxy_index]
                sleep(random.choice([1,2,3,4]))

    def initUI(self):

        self.master.title("Bookingjini: Scraper")
        self.pack(fill=BOTH, expand=False)

        frame0 = Frame(self, bg = self.bgcolor)
        frame0.pack(fill=X)
        
        img = Image.open(self.logo_path)
        img.thumbnail(self.logo_size)  
        imgtk = ImageTk.PhotoImage(img)
        label1 = Label(frame0, image=imgtk)
        label1.image = imgtk
        label1.pack(side=LEFT, padx=5, pady=7)

        frame1 = Frame(self, bg=self.bgcolor)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Location", width=self.label_width)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        self.location = Entry(frame1, width=self.entry_width)
        self.location.pack(fill=X, padx=5)

        frame2 = Frame(self, bg=self.bgcolor)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Check-In", width=self.label_width)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        self.check_in = Entry(frame2, width=self.entry_width)
        self.check_in.pack(fill=X, padx=5)

        frame3 = Frame(self, bg=self.bgcolor)
        frame3.pack(fill=BOTH)

        lbl3 = Label(frame3, text="Check-Out", width=self.label_width)
        lbl3.pack(side=LEFT, padx=5, pady=5)
        
        self.check_out = Entry(frame3, width=self.entry_width)
        self.check_out.pack(fill=X, padx=5)

        frame4 = Frame(self, bg=self.bgcolor)
        frame4.pack(fill=X)

        btn = Button(frame4, text="Scrape", command=lambda: self.scrape())
        btn.pack(fill=X, padx=5, pady=5)      


def main():
    global window_size, background_color
    root = Tk()
    root.configure(background=background_color)
    root.geometry('{}x{}'.format(window_size[0], window_size[1]))
    
    #remove minsize and maxsize lines if u want the window to expand
    root.minsize(window_size[0], window_size[1])
    root.maxsize(window_size[0], window_size[1])

    app = Application()
    app.initUI()
    
    root.mainloop()


if __name__ == '__main__':
    main()