This script retrieve listing of properties in Calgary sold within last 14 days.  

Line 123 - 145
I'm using module 'requests' to login and maintain the session. Credentials are stored in .bash_profile

Line 147 - 150
Create CSV column names

Line 85 & 92
Two empty lists are created to store property url and its tag 'last sold X days ago', respectively. if X is less than 14, url is passed to the next function for processing.
Otherwise, the loop ends.

Line 20 - 31
Pandas are perfect tool to grab all the tables from webpage. the data in dataframe can be narrowed down use a few index: table index -> column name -> row name
The first table contains important info about property: beds/bath/land_size/floor_space/years_built. script will skip to the next listing if anything missing here.

Line 34 - 43
Second table "tax information" isn't always present,which will affect the index of "sold price" in the next table 







