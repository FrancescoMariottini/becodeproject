# Results overview 
The following CSV files, containing the results, are provided.
1. flagged.csv: dataset of the originally extracted information including also the "duplicates" and "null" (count of null per row) check columns.
1. description.csv: overview of the dataset before the cleaning.
1. cleaned.csv: dataset after the cleaning and formatting 
1. cleaned_description.csv: overview of the cleaned dataset.

Hereby the results and conclusions of the process are described through the files description.csv. No sensible differences are found in the cleaned_description.csv file. 

## description.csv results 
No duplicates and no empty rows are found. However only null values are found for important parameters such as price, rooms number and area (see the row "count"). The scrapping doesn't recover "sale" data. In 50% of the rows at least 6 null values are found. 5% of the rows have from 8 to 10 empty values. 5% of the rows have only 3 empty values. 

## description.csv conclusions.
Immoweb website is probably already performing internal quality checks which prevents data quality checks. While no empty rows are found, it would be better to analyse only data for which price, rooms number and area are available. Depending on analysis objectives, percentile 5% and 95% could be also considered as outliers and excluded from further processing.

