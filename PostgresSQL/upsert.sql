insert into sales_data(brand, product_name, sale_price, link, date)
select brand, product_name, sale_price, link, date from new_data 
on conflict  (link) 
do 
  update set atl = excluded.sale_price, atl_date = excluded.date where (excluded.sale_price < sales_data.atl or excluded.sale_price < sales_data.sale_price)
