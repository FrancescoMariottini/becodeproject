from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from random import randint
import re

def get_search_results(results=120):
    """Collect property urls and types by going through the search result pages of new 'house' and new 'appartment',
    stopping at {results} and returning a dictionary of {'url1':True/False, 'url2':True/False, ...}. True means house. False means apartment."""
    # initialise the dictionary with the results
    search_results = {}
    # initialise the result count
    result_count = 0
    # set the startpage of the search
    page_number = 1
    # start the loop
    while result_count < results:
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
        if page_number % 10 == 0:
            print("{}: {} results pages searched. ".format(time.asctime(),page_number)) #print current time and search results for internal checks
    return search_results

def results_page_scrape(page_number,property_type):
    '''A subroutine scraping links from 1 specific search result page, links to projects are ignored'''
    # initialise the return
    links = []
    # I slow down the frequency of requests to avoid being identified and therefore ban from the site
    time.sleep(random.uniform(1.0, 2.0))
    # setup the selenium webdriver; if able to find elements within the given
    # span it returns as soon as finding them, else it raises an exception after 10 seconds.
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    url=f'https://www.immoweb.be/en/search/{property_type}/for-sale?countries=BE&isALifeAnnuitySale=false&page={page_number}&orderBy=newest'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    for elem in soup.find_all('a', attrs={"class":"card__title-link"}):
        # get hyperlink to property page
        hyperlink = elem.get('href')
        # cut the searchID off
        hyperlink = re.match("(.+)\?searchId=.+", hyperlink).group(1)
        # include in the return if it is not a -project-
        if "-project-" not in hyperlink:
            links.append(hyperlink)
    driver.close()
    return links