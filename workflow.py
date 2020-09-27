import get_search_results as search
import scrap_search_result as scrap
import dataquality as dataquality
import pandas as pandas
import os

urls_dict = search.get_search_results(results=2)
print("{} links scrapped".format(len(urls_dict)))

lists_dict = scrap.scrap_list(urls_dict)

# df = pandas.read_csv(os.path.join(os.path.abspath('') + "\lists.csv")) #local testing version
# dq = dataquality.DataQuality(df)

dq = dataquality.DataQuality(lists_dict)

_VALUES_FORMAT = dict(hyperlink='str', locality='str', postcode='int', house_is='yn', property_subtype='str',
                      price='int', sale='str', rooms_number='int', area='int', kitchen_has='yn', furnished='yn',
                      open_fire='yn', terrace='yn', terrace_area='int', garden='yn', garden_area='int',
                      land_surface='int', land_plot_surface='int', facades_number='int', swimming_pool_has='yn')

flagged = dq.flag()

description = dq.describe()

cleaned = dq.clean()
cleaned = dq.values_format(df=cleaned, columns_dtypes=_VALUES_FORMAT)

description_cleaned = dq.describe(df=cleaned)

output_csvs = {"flagged": flagged, "description": description, "cleaned": cleaned, "description_cleaned": description_cleaned}

def table_to_csv(table, filename: str, path=os.path.abspath('')):
    if isinstance(table, dict):
        table = pandas.DataFrame(table)
    elif not isinstance(table, pandas.DataFrame):
        raise Exception("Provided table is neither a dataframe nor a dictionary of lists")
    table.to_csv(os.path.join(path, filename + ".csv"))
    print(filename + ".csv" + " created at: " + path)
    return None


for key, value in output_csvs.items():
    table_to_csv(value, key)
