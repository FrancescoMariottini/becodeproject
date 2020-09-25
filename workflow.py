import get_search_results as search
import scrap_search_result as scrap
import dataquality as dataquality
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

dict_urls = search.get_search_results(1)
print(dict_urls)

dict_dataframe = scrap.scrap_list(dict_urls)
print(dict_dataframe)

dq = dataquality.DataQuality(dict_dataframe)

df_flagged, df_cleaned, report = dq.domain_integrity(values_format = _VALUES_FORMAT)

df_flagged, df_cleaned, report = dq.entity_integrity()

path = os.path.abspath('')
filepath = os.path.join(path, "flagged.csv")
df_flagged.to_csv(filepath)
filepath = os.path.join(path, "cleaned.csv")
df_cleaned.to_csv(filepath)
filepath = os.path.join(path, "report.csv")
report.to_csv(filepath)
print("CSVs created at: " + str(path))