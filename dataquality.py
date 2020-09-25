import pandas
pandas.set_option('display.max_columns', None)

_VARIABLES_TYPES = {'hyperlink':str,
 'locality':str,
 'postcode':int,
 'house_is':bin, #1.0 or None
 'property_subtype':str,
 'price':int,
 'sale':int,
 'rooms_number':int,
 'area':float,
 'kitchen_has':bin,
 'furnished':bin,
 'open_fire':bin,
 'terrace':bin,
 'terrace_area':float,
 'garden':bin,
 'garden_area':float,
 'land_surface':float,
 'land_plot_surface':float,
 'facades_number':int,
 'swimming_pool_has':bin}

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
            if self.df_flagged.loc["count", column] == countmax:
                self.unique_identifiers.append(column)
        print(self.report)
    def __check_with_headers__(self,values_to_check):
        if isinstance(values_to_check,dict):
            values_to_check = values_to_check.keys()
        if isinstance(values_to_check,list):
            values_to_check = values_to_check
        if any([key not in self.df_cleaned.columns for key in values_to_check]):
            raise Exception("Provided values(s) not in the table headers")
    def domain_integrity(self, variables_types: dict):
        self.__check_with_headers__(variables_types)
        if variables_types is None:
            variables_types = _VARIABLES_TYPES
        def type_change(value, variable_type):
            if value is not None:
                if variable_type == int:
                    value = int(value)
                if variable_type == bin:
                    value = bin(value)
                if variable_type == str:
                    value = str(value)
                if variable_type == float:
                    value = float(value)
                if variable_type == bool:
                    value = bool(value)
            return value
        for header, variable_type in variables_types.items():
            self.df_flagged[str("integrity_" + header)] = self.df_flagged[header].apply(
                lambda x: isinstance(x, variable_type))
            integrity_series = self.df_flagged[:,self.df_flagged[str("integrity_" + header)]==True]
            self.df_cleaned = self.df_cleaned[self.df_cleaned.index.isin(integrity_series)]
            self.df_cleaned[header] = self.df_cleaned[header].apply(
                lambda x: type_change(x, variable_type))
            self.report.loc["none", header] = self.df_flagged.loc[:, header].isnull().sum(axis=0)
        return self.df_flagged, self.df_flagged, self.report
    def entity_integrity(self, unique_identifiers):
        if isinstance(unique_identifiers,list) == False:
            unique_identifiers = self.unique_identifiers
        duplicates_check = self.df_flagged[:,self.df_cleaned.columns].duplicated(subset=unique_identifiers)
        unique_series = duplicates_check[duplicates_check == True]
        self.df_flagged["duplicates"] = duplicates_check
        self.df_cleaned = self.cleaned[self.df_cleaned.index.isin(unique_series)]
        return self.df_flagged, self.df_flagged, self.report