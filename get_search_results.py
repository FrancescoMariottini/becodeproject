from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from random import randint
import re

def get_search_results(minresults=40):
    """Collect property urls and types by going through the search result pages of new houses and appartments,
    stopping when having reached the minimum number of results and returning a dictionary of {'url1':True/False, 'url2':True/False, ...}.
    True means house. False means apartment. Without argument only the first page is collected (~60 results)"""
    # initialise the dictionary with the results
    search_results = {}
    # initialise the running result count
    result_count = 0
    # set on which page to start the search
    page_number = 1
    # initialise the webdriver globally for use inside the subroutine
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    
    # start the loop    
    while result_count < minresults:
        # for each loop, scrape one results page of houses and one of appartments
        # the results are added if they are not there yet
        for houselink in results_page_scrape(page_number,"house"):
            if houselink not in search_results:
                search_results[houselink] = True
        for apartmentlink in results_page_scrape(page_number,"apartment"):
            if apartmentlink not in search_results:
                search_results[apartmentlink] = False
        result_count = len(search_results)
        page_number += 1
    
    driver.close()
    
    return search_results

def results_page_scrape(page_number,property_type):
    '''A subroutine scraping links from 1 specific search result page, links to projects are ignored'''
    # initialise the return
    links = []
    # I slow down the frequency of requests to avoid being identified and therefore ban from the site
    time.sleep(random.uniform(1.0, 2.0))
    url=f'https://www.immoweb.be/en/search/{property_type}/for-sale?countries=BE&isALifeAnnuitySale=false&page={page_number}&orderBy=newest'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    
    for elem in soup.find_all('a', attrs={"class":"card__title-link"}):
        # get hyperlink to property page
        hyperlink = elem.get('href')
        # include in the return if it is not a -project-
        if "-project-" not in hyperlink:
            # cut the searchID off
            hyperlink = re.match("(.+)\?searchId=.+", hyperlink).group(1)
            links.append(hyperlink)
            
    return links
    