Data from web scrapping are uploaded to postgres. There are two tables: the main table, 'sales_data' has two extra columns - atl and atl_date (all time low)

Web scrapper ran again after a few weeks, the latest data are then transfered to the second table: 'new_data'. To compare the price, use the following command:

insert into sales_data(brand, product_name, sale_price, link, date)
select brand, product_name, sale_price, link, date from new_data 
on conflict  (link) 
do 
  update set atl = excluded.sale_price, atl_date = excluded.date where (excluded.sale_price < sales_data.atl or excluded.sale_price < sales_data.sale_price)
