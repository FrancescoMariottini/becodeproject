## "Collecting real estate sales in Belgium" (What)
A tool to scrap real estate sales data from Belgium to obtain a valuable insight of the real estate market.

## The Mission (Why)
The real estate company "ImmoEliza" wants to create a machine learning model to make price predictions on real estate sales in Belgium. 

### Features  (Why)
The dataset holds the following columns:
- Locality
- Postcode
- Type of property (House/apartment)
- Subtype of property (Bungalow, Chalet, Mansion, ...)
- Price
- Type of sale (Exclusion of life sales)
- Number of rooms
- Area
- Fully equipped kitchen (Yes/No)
- Furnished (Yes/No)
- Open fire (Yes/No)
- Terrace (Yes/No) 
    - If yes: Area
- Garden (Yes/No)
   - If yes: Area
- Surface of the land
- Surface area of the plot of land
- Number of facades
- Swimming pool (Yes/No)
- State of the building (New, to be renovated, ...)

Everything in a csv file.

#### Highlight features 
- Data for all of Belgium.
- Minimum 10 000 inputs
- No empty row. If information is missing, the value is set to None.
- No duplicates. 
- Binary values replacing "Yes" or "Not" 

### Who did the project (Who):
Contributors : Philippe Fimmers (PF), Francesco Mariottini (FM), Opap's Ditudidi (OD)

### Development (How)
First brainstorm identified four main independent modules:
1) Scrapping links of valid search results from Immoweb (started by OD).
2) Scrapping required information from each building (started by PF).
3) Filling founded parameters into a csv (started by FM).
4) Cleaning result through quality checks.

OD started (1) after realising challenge of scrapping search results through only BeautifulSoup function.
PF found a solution to it by using Selenium. OD then supported part (2) development.
Testing of modules started on small sample of the datasets.

# Collecting Data (When)
- Repository: `challenge-collecting-data`
- Type of Challenge: `Consolidation`
- Duration: `3 days`
- Deadline: `25/09/2020 17:00`
- Team challenge : 3



