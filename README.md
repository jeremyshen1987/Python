Thanks for taking your time and read my script :)    ( https://github.com/jeremyshen1987/Python/blob/main/HR_Scraper.py )


This is a webs scrapper for Harry Rosen sales page. 

You must apply a filter on the left panel and use the URL as input.



Code breakdown:

Line 73 - 84
Take the the URL from user input. It must satisfy two conditions in order to break the while loop.
(expect 20 seconds hiccups after you see - Reminder: Each page takes 1 minute to process)


Line 89 - 92
Create a csv file using current date as filename. Generate headers columns



Line 96 - 105
Format the URL from user input by append the page number. Requests-HTML is used to render the webpage (Line 105) in the backgroud because sales page containing multiple product links are generated from javascript, which cannot be processed by beautifulsoup. Timeout are increased since rendering take more than 8 seconds, the default setting. 

Line 107 - 111
Detect the last page and end the script. I'm using xpath to locate the first product of the webpage, if there are 3 pages and it hit page 4 (a blank page), the first product doesn't exist, hence the length of that element is 0 as opposed to 1.  Script is ended as a result. 

Line 113 -> Line 16 - 24
Find the link containing 'a' tag. the search result includes all the products we want to parse and a few other irrelevant links such as "contact us","careers". I use the keyword "product" to filter out these irrelevant links. 

Example: 

https://www.harryrosen.com/en/product/kiton-stretch-cotton-cashmere-chinos-20086016061 -> We want it!
https://www.harryrosen.com/en/careers -> We want get rid of it!

Then I'm looping through each product in the sales page to extract the data.



Line 26 (Line 61 - 68)
Error handling. Occationally I have encountered some products are sold out but not removed from Harry Rosen's search result, this will cause script to end prematurely. The more specific attribute error are placed before the generic exceptions.

Line 28 - 52
Extract data (prod_name, sales/original price...) from individual product page. Rendering is not need here as they have nothing to do with javascript. 

Line 56 - 59
Use the csv file we just created and write the data one by one.


