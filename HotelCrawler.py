from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random 
from time import sleep
import expedia
import Goibibo
import Hotelsdotcom

ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]
otas = ['https://www.expedia.co.in','https://www.goibibo.com/hotels/','https://www.hotels.com']
'''
Retrieve latest proxies
'''
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
def random_proxy():
    return random.randint(0, len(proxies) - 1)
'''
Keys to be searched
'''
searchKey = input('Enter the location') # Change this to your city 
checkInDate = input('Enter the Check In Date') #Format %d/%m/%Y
checkOutDate = input('Enter the Check Out Date') #Format %d/%m/%Y
inputs = [searchKey, checkInDate, checkOutDate]
'''
Crawling through the wepages in otas
'''
for url in otas:
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]
    driver = random.choice([1, 2])
    while True: 
        req = Request('http://icanhazip.com')
        req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
        try:
            my_ip = urlopen(req).read().decode('utf8')
            print('#' + str(1) + ': ' + my_ip)
            temp = otas.index(url)
            if temp == 0:
                df = expedia.parse(url, proxy, driver, inputs)
                df.to_csv('expedia.csv')
                break
            if temp == 1:
                df = Goibibo.parse(url, proxy, driver, inputs)
                df.to_csv('Goibibo.csv')
                break
            if temp == 2:
                df = Hotelsdotcom.parse(url, proxy, driver, inputs)
                df.to_csv('Hotelsdotcom.csv')
                break
        except: # If error, delete this proxy and find another one
            del proxies[proxy_index]
            #print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]
    sleep(random.choice([1,2,3,4]))
    