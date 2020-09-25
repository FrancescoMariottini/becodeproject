import pandas

pandas.set_option('display.max_columns', None)

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


class DataQuality:
    def __init__(self, table):
        if isinstance(table, pandas.DataFrame):
            self.df_flagged = table
        if isinstance(table, dict):
            self.df_flagged = pandas.DataFrame(table)
        else:
            raise Exception("Provided table is neither a dictionary nor a dataframe")
        self.df_cleaned = self.df_flagged
        self.report = self.df_flagged.describe(include='all')
        countmax = max(self.report.loc["count", :].values)
        self.unique_identifiers = []
        for column in self.df_flagged.columns:
            if self.report.loc["count", column] == countmax:
                self.unique_identifiers.append(column)
        print(self.report)

    def __check_with_headers__(self, values_to_check):
        if isinstance(values_to_check, dict):
            values_to_check = values_to_check.keys()
        if isinstance(values_to_check, list):
            values_to_check = values_to_check
        if any([key not in self.df_cleaned.columns for key in values_to_check]):
            raise Exception("Provided values(s) not in the table headers")

    def domain_integrity(self, values_format: dict):
        self.__check_with_headers__(values_format)
        if values_format is None:
            values_format = _VALUES_FORMAT

        def type_change(value, value_type):
            try:
                if value is not None:
                    if value_type == "float":
                        try:
                            value = float(value)
                        except TypeError:
                            value = None
                    if value_type == "int":
                        try:
                            value = int(value)
                        except TypeError:
                            value = None
                    if value_type == "yn":
                        if (value == 1) or (value == "1") or (value == True) or (value == "True"):
                            value = "Yes"
                        elif (value == 0) or (value == "0") or (value == False) or (value == "False"):
                            value = "No"
                    else:
                        value = value
            except:
                value = None
            return value

        for header, value_type in values_format.items():
            # try:
            #
            #self.df_flagged[str("integrity_" + header)] = self.df_flagged[header].apply(
            #    lambda x: isinstance(x, value_type))
            # except TypeError:
            # print(value_type)
            #integrity_series = self.df_flagged[self.df_flagged.loc[:, "integrity_" + str(header)] == True]
            #self.df_cleaned = self.df_cleaned[self.df_cleaned.index.isin(integrity_series)]
            self.df_cleaned[header] = self.df_cleaned[header].apply(
                lambda x: type_change(x, value_type))
            self.report.loc["none", header] = self.df_flagged.loc[:, header].isnull().sum(axis=0)
        return self.df_flagged, self.df_cleaned, self.report

    def entity_integrity(self, unique_identifiers = None):
        if unique_identifiers is None:
            unique_identifiers = self.unique_identifiers
        #if isinstance(unique_identifiers, list) == False:
        duplicates_check = self.df_flagged.duplicated(subset=unique_identifiers)
        unique_series = duplicates_check[duplicates_check == False]
        self.df_flagged["duplicates"] = duplicates_check
        self.df_cleaned = self.df_cleaned[self.df_cleaned.index.isin(unique_series)]

        return self.df_flagged, self.df_cleaned, self.report
