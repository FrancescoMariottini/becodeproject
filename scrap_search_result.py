from bs4 import BeautifulSoup 
import re 
import requests

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
    properties = ["hyperlink" ,"locality", "postcode", "house_is", "property_subtype",	"price", "sale", "rooms_number", "area", "kitchen_has", "furnished",	"open_fire", "terrace", "terrace_area", "garden", "garden_area", "land_surface", "land_plot_surface", "facades_number", "swimming_pool_has"]



    #making a dict with all the property names as key and an empty list as value
    dict_dataframe = {}
    for property_name in properties:
        dict_dataframe[property_name] = []

    #scrap each url of the input and put the result into a variable
    for key in dict_urls: 
        dict_result_scrapping = scrap(key, dict_urls[key])

        #for each property (key) of the scrapping out put, match it with dataframe property. If none exist, just use None
        for key1 in dict_dataframe:
            dict_dataframe[key1].append(dict_result_scrapping.get(key1, False) or None)            
    
    return dict_dataframe

def scrap(url, is_house): 
    dict = {} 
    r = requests.get(url) 
    soup = BeautifulSoup(r.content,'html.parser')     

    #for every property, call the right function to get the needed data
    dict["hyperlink"] = url
    dict["locality"] = url.split("/")[7]
    dict["postcode"] = url.split("/")[8]
    dict['house_is'] = is_house
    dict['property_subtype'] = url.split("/")[5]   
    dict['price'] = get_property_value(soup, "Price")     
    dict['sale'] = ''
    dict['rooms_number'] = get_property_value(soup, 'Bedrooms')
    dict['area'] = get_property_value(soup, 'Living area')
    dict['kitchen_has'] = get_property_bool(soup, 'Kitchen type')
    dict['furnished'] = get_property_bool(soup, 'Furnished')
    dict['open_fire'] = get_property_bool(soup, 'Fireplace')
    dict['terrace'] = get_property_bool(soup, 'Terrace')
    dict['terrace_area'] = get_property_value(soup, 'Terrace surface')
    dict['garden'] = get_property_bool(soup, 'Garden')
    dict['garden_area'] = get_property_value(soup, 'Garden surface')
    dict['land_surface'] = None
    dict['land_plot_surface'] = None
    dict['facades_number'] = get_property_value(soup, 'Facades')
    dict['swimming_pool_has'] = get_property_bool(soup, 'Swimming pool')
    
    return dict