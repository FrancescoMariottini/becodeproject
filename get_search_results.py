from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from random import randint
import re

def get_search_results(maxpage):
    """Collect search results running up to the maxpage number of both newest 'house'  and 'appartment' sales,
    returning a nested dictionary of {'url':{'house_is':'0/1','info2':'',...}}"""
    # initialise the dictionary with the results
    search_results = {}
    # start the loop
    for i in range(1, maxpage+1):
        # for each loop, scrape one results page of houses and one of appartments
        # the results are added if they are not there yet
        for houselink in results_page_scrape(i,"house"):
            if houselink not in search_results:
                search_results[houselink] = {}
                search_results[houselink]["house_is"] = 1
        for apartmentlink in results_page_scrape(i,"apartment"):
            if apartmentlink not in search_results:
                search_results[apartmentlink] = {}
                search_results[apartmentlink]["house_is"] = 0
    return search_results

def results_page_scrape(pagenumber,propertytype):
    '''A subroutine scraping links from search results on a propertytype/page'''
    # initialise the return
    links = []
    # I slow down the frequency of requests to avoid being identified and therefore ban from the site
    time.sleep(random.uniform(1.0, 2.0))
    # setup the selenium webdriver; if able to find elements within the given
    # span it returns as soon as finding them, else it raises an exception after 10 seconds.
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    url=f'https://www.immoweb.be/en/search/{propertytype}/for-sale?countries=BE&isALifeAnnuitySale=false&page={pagenumber}&orderBy=newest'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    for elem in soup.find_all('a', attrs={"class":"card__title-link"}):
        # get hyperlink to property page
        hyperlink = elem.get('href')
        # cut the searchID off
        hyperlink = re.match("(.+)\?searchId=.+", hyperlink).group(1)
        # append to the return
        links.append(hyperlink)
    driver.close()
    return links