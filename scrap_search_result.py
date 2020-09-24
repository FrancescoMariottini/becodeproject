from bs4 import BeautifulSoup 
import re 
import requests

def scrap_list(dict_urls): 
    dict_dataframe = {}

    for key in dict_urls: 
        dict_result_scrapping = scrap(key, dict_urls[key])
        
        for key1 in dict_result_scrapping:
            dict_dataframe[key1].append(dict_result_scrapping[key1])
    
    return dict_dataframe

def scrap(url, is_house): 
    dict = {} 
    r = requests.get(url) 
    soup = BeautifulSoup(r.content,'html.parser') 
    
    dict["link"] = url
    #dict["locality"] = 'k'
    dict["postcode"] = re.findall('/[0-9]{4}/', url)[0].replace('/', '')
    dict['house_is'] = is_house
    
    return dict