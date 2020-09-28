from bs4 import BeautifulSoup 
import re 
import requests
import time

def get_property_value(soup, name):

    
    #Looks into every row of the tables
    for elem in soup.find_all('tr'):
        #If it finds an element with text equals to property name it will return it's equivalent value
         if elem.th and re.search(name, str(elem.th.string)):
            if name == "Price":              
                for descendant in elem.td.descendants:
                    if re.search("(\d{5,})\s€", str(descendant)):
                        return int(re.search("(\d{5,})\s€", str(descendant))[1])
            else:
                return elem.td.contents[0].strip()
    #If nothing was found, will return None 
    return None

def get_property_bool(soup, name):
    #Looks into every row of the tables
    for elem in soup.find_all('tr'):
        #If it finds an element with text equals to property name it will return true
        if elem.th and re.search(name, str(elem.th.string)):
            return True
    #If nothing was found, will return false
    return False

def scrap_list(dict_urls): 
    #listing all the property names
    properties = ["hyperlink" ,"locality", "postcode", "house_is", "property_subtype",  "price", "sale", "rooms_number", "area", "kitchen_has", "furnished",    "open_fire", "terrace", "terrace_area", "garden", "garden_area", "land_surface", "land_plot_surface", "facades_number", "swimming_pool_has"]

    #making a dict with all the property names as key and an empty list as value
    dict_dataframe = {}
    for property_name in properties:
        dict_dataframe[property_name] = []

    #scrap each url of the input and put the result into a variable
    url_number = 0
    for key in dict_urls:
        dict_result_scrapping = scrap(key, dict_urls[key])

        #for each property (key) of the scrapping out put, match it with dataframe property. If none exist, just use None
        for key1 in dict_dataframe:
            dict_dataframe[key1].append(dict_result_scrapping[key1])
        url_number += 1
        if url_number % 10 == 0:
            print(f"{time.asctime()}: {url_number} property searched. ")
    return dict_dataframe

def scrap(url, is_house): 
    dictionary = {} 
    r = requests.get(url) 
    soup = BeautifulSoup(r.content,'html.parser')     

    #for every property, call the right function to get the needed data

    dictionary["hyperlink"] = url
    dictionary["locality"] = url.split("/")[7]
    dictionary["postcode"] = url.split("/")[8]
    dictionary['house_is'] = is_house
    dictionary['property_subtype'] = url.split("/")[5]   
    dictionary['price'] = get_property_value(soup, "Price")     
    dictionary['sale'] = ''
    dictionary['rooms_number'] = get_property_value(soup, 'Bedrooms')
    dictionary['area'] = get_property_value(soup, 'Living area')
    dictionary['kitchen_has'] = get_property_bool(soup, 'Kitchen type')
    dictionary['furnished'] = get_property_bool(soup, 'Furnished')
    dictionary['open_fire'] = get_property_bool(soup, 'Fireplace')
    dictionary['terrace'] = get_property_bool(soup, 'Terrace')
    dictionary['terrace_area'] = get_property_value(soup, 'Terrace surface')
    dictionary['garden'] = get_property_bool(soup, 'Garden')
    dictionary['garden_area'] = get_property_value(soup, 'Garden surface')
    dictionary['land_surface'] = None
    dictionary['land_plot_surface'] = get_property_value(soup, 'Surface of the plot')
    dictionary['facades_number'] = get_property_value(soup, 'Facades')
    dictionary['swimming_pool_has'] = get_property_bool(soup, 'Swimming pool')
    
    return dictionary
