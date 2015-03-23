##################################################################################################################################
### Author: Shatrunjai Singh
### Date: 2-27-2015
### Description: Program to get the Prices from Cincinnati Criagslist for any item. Displays the average price, min and max price
#################################################################################################################################

import urllib2
import json
import re
import numpy as np
import urlparse


def craigslist(searcher, cityname):
    u=url_fix("https://"+cityname+".craigslist.org/search/sss?query="+searcher+"&sort=rel")
    print u
    htmlfile=urllib2.urlopen(u)
    #print ("result code: " + str(htmlfile.getcode()))
    htmltext=htmlfile.read()
    findtext='<span class="price">&#x0024;(\d*)</span></a>'
    pattern=re.compile(findtext)
    price=re.findall(pattern,htmltext)
    #print type(price)
    price = map(int, price)
    meanprice=np.mean(price)
    maxprice=np.max(price)
    minprice=np.min(price)
    numberofitem=np.count_nonzero(price)
    print json.dumps({'Name':searcher,'Prices':price,'TotalItemsCounted':numberofitem,'AveragePrice':meanprice,'MaximumPrice':maxprice,'MinPrice':minprice}, sort_keys=True,indent=4, separators=(',', ': '))
    #print "The Cincinnati craigslist local price (in $) for ",searcher," is  ",price
    
    return json.dumps

def main():
    searcher=raw_input ("Enter the item you want the prices for :")
    cityname=raw_input ("Enter the city name :")
    craigslist(searcher,cityname)
 
    
def url_fix(url, charset='utf-8'): #Code that i got from a website to replace blank spaces in urls with %20
      
    url = url.strip()
    if not url.startswith(('http://', 'https://', 'ftp://', 'ftps://')):
        # no schema
        url = 'http://' + url
    if '/' not in url.split('//')[-1]:
        # no path
        frags = [url.find(sep) for sep in ('?', '#') if sep in url]
        if frags:
            x = min(frags)
            host, qs = url[:x], url[x:]
        else:
            host, qs = url, ''
        url = host + '/' + qs
    if isinstance(url, unicode):
        url = url.encode(charset)
    host = url.split('//', 1)[1].split('/', 1)[0]
    if not host.replace('.', '').replace('-', '').isalnum():
        # idn
        host = host.decode('utf-8').encode('idna')
        schema = url.split('//', 1)[0]
        uri = url.split('/', 3)[-1]
        url = '%s//%s/%s' % (schema, host, uri)
    url = urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    return url
       

main()
