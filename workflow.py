import get_search_results as search
import scrap_search_result as scrap
import dataquality as dataquality
import pandas as pandas
import os

_VALUES_FORMAT = {'hyperlink': 'str',
                  'locality': 'str',
                  'postcode': 'int',
                  'house_is': 'yn',
                  'property_subtype': 'str',
                  'price': 'int',
                  'sale': 'str',
                  'rooms_number': 'int',
                  'area': 'int',
                  'kitchen_has': 'yn',
                  'furnished': 'yn',
                  'open_fire': 'yn',
                  'terrace': 'yn',
                  'terrace_area': 'int',
                  'garden': 'yn',
                  'garden_area': 'int',
                  'land_surface': 'int',
                  'land_plot_surface': 'int',
                  'facades_number': 'int',
                  'swimming_pool_has': 'yn'}


def table_to_csv(table, filename: str, path=os.path.abspath('')):
    if isinstance(table, dict):
        table = pandas.DataFrame(table)
    elif not isinstance(table, pandas.DataFrame):
        raise Exception("Provided table is neither a dataframe nor a dictionary of lists")
    table.to_csv(os.path.join(path, filename + ".csv"))
    print(filename + ".csv" + " created at: " + path)
    return None


urls_dict = search.get_search_results(1)
lists_dict = scrap.scrap_list(urls_dict)

# table_to_csv(dict_dataframe, "lists") #local testing version
#df = pandas.read_csv(os.path.join(os.path.abspath('') + "\lists.csv")) #local testing version
#dqp = dataquality.DataQuality(df)

dqp = dataquality.DataQuality(lists_dict)

flagged = dqp.flag()
table_to_csv(flagged, "flagged")

description = dqp.describe()
table_to_csv(description, "description")

cleaned = dqp.clean()
cleaned = dqp.values_format(df=cleaned, columns_dtypes=_VALUES_FORMAT)

table_to_csv(cleaned, "cleaned")
