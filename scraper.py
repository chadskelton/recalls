#!/usr/bin/env python

import time
from datetime import datetime
import requests
from BeautifulSoup import BeautifulSoup
import re

def scrape_recallpage(url):
    
    url = 'http://inspection.gc.ca' + str(url)
    
    print url
    
    html = requests.get(url)
    htmlpage = html.content
    
    soup = BeautifulSoup(htmlpage)
    
    # print soup
    
    detailbox = soup.find("dl", {"class" : "dl-horizontal"})
    
    details = detailbox.findAll("dd")
    
    title = soup.find('h1')
    
    # print soup.text
    
    try:
        detailregex = re.search('RECALL-DETAILS BEGIN(.+?)WCMS:RECALL-DETAILS END', soup.text)
        detailtext = detailregex.group(1)
        
    except:
        print 'No detail text found'
        detailtext = 'NO DETAIL TEXT FOUND'
    
    # print detailtext
    
    record = {}
    record["uniqueid"] = str(datetime.now())
    record["title"] = title.text
    record["date"] = details[0].text
    record["reason"] = details[1].text
    record["classification"] = details[2].text
    record["company-firm"] = details[3].text
    record["distribution"] = details[4].text
    record["extent"] = details[5].text
    record["refnumber"] = details[6].text
    record["detailtext"] = detailtext
    record["url"] = url
    
    print record
    
    # scraperwiki.sqlite.save(['uniqueid'], record)
    scraperwiki.sqlite.save(unique_keys=['uniqueid'], data=record)
    time.sleep(3)

def scrape_foodyears(url): # in case page changes

    html = requests.get(url)
    htmlpage = html.content
    
    soup = BeautifulSoup(htmlpage)
    
    # print soup
    
    table = soup.find("table", {"class" : "table table-striped table-hover"})
    
    links = table.findAll("a")
    
    for link in links:
        url = link.get('href')
        try:
            scrape_recallpage(url)
        except:
            print 'Recall page scrape failed. Probably advisory page.'
    
years = ['2011'] # removed 2015, 2014, 2013 and 2012 because timed out

for year in years:
    print year
    url = 'http://inspection.gc.ca/about-the-cfia/newsroom/food-recall-warnings/complete-listing/eng/1351519587174/1351519588221?ay=' + str(year) + '&fr=0&fc=0&fd=0&ft=2'
    scrape_foodyears(url)
