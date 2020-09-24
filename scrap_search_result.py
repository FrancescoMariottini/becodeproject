from bs4 import BeautifulSoup
import re
import requests

def scrap(url):
	'''Takes a property url and returns a dictionary of all the elements we could find'''
    dict = {}
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    #dict["locality"] = 'k'
    dict["postcode"] = re.findall('/[0-9]{4}/', url)[0].replace('/', '')
        
    return dict