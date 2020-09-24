from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from random import randint
import re

def get_search_results(maxpage):
    """Collect property urls and types by going through the search result pages of new 'house' and new 'appartment',
    stopping at {maxpage} and returning a dictionary of {'url1':'0/1', 'url2':'0/1', ...}. 1 means house. 0 means apartment."""
    # initialise the dictionary with the results
    search_results = {}
    # start the loop
    for i in range(1, maxpage+1):
        # for each loop, scrape one results page of houses and one of appartments
        # the results are added if they are not there yet
        for houselink in results_page_scrape(i,"house"):
            if houselink not in search_results:
                search_results[houselink] = 1
        for apartmentlink in results_page_scrape(i,"apartment"):
            if apartmentlink not in search_results:
                search_results[apartmentlink] = 0
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
    