# "Collecting real estate sales in Belgium" (What)
A tool to scrap real estate sales data from Belgium to obtain a valuable insight of the real estate market.

# The Mission (Why)
The real estate company "ImmoEliza" wants to create a machine learning model to make price predictions on real estate sales in Belgium. 

## Features 
The dataset holds the following information.

information|variable name|variable type|example(s)
---|---|---|---
Hyperlink|hyperlink|str||
Locality|locality|str||
Postcode|postcode|int||
Type of property (House/apartment)|house_is|bin||
Subtype of property|property_subtype|str|Bungalow, Chalet, Mansion, ...|
Price|price|float||
Type of sale (Exclusion of life sales)|sale|str|
Number of rooms|rooms_number|int|
Area|area|float|
Fully equipped kitchen (Yes/No)|kitchen_has|bin|
Furnished (Yes/No)|furnished|bin|
Open fire (Yes/No)|open_fire|bin|
Terrace (Yes/No)|terrace|bin|
Terrace Area|terrace_area|float| 
Garden (Yes/No)|garden|bin|
Garden Area|garden_area|float|
Surface of the land|land_surface|float|
Surface area of the plot of land|land_plot_surface|float|
Number of facades|facades_number|int|
Swimming pool (Yes/No)|swimming_pool_has|bin|
State of the building|building_state|str|(New, to be renovated, ...)

Everything in a csv file.

## Highlights
- Data for all of Belgium.
- Minimum 10 000 inputs
- No empty row. If information is missing, the value is set to None.
- No duplicates. 
- Binary values replacing "Yes" or "Not" 

# Who did the project (Who):
Contributors : Philippe Fimmers (PF), Francesco Mariottini (FM), Opap's Ditudidi (OD)

# Development (How)
First brainstorm identified four main independent modules:
1) Scrapping links of valid search results from Immoweb (started by OD).
2) Scrapping required information from each building (started by PF).
3) Filling founded parameters into a csv (started by FM).
4) Cleaning result through quality checks.

OD started (1) after realising challenge of scrapping search results through only BeautifulSoup function.
PF found a solution to it by using Selenium. OD then supported part (2) development.
Testing of modules started on small sample of the datasets.

Since the single building page provides information only about the subtype, and not if it is an house or an apartment, the type of property parameter (house_is) was checked during module (1).

# Collecting Data (When)
- Repository: `challenge-collecting-data`
- Type of Challenge: `Consolidation`
- Duration: `3 days`
- Deadline: `25/09/2020 17:00`
- Team challenge : 3



