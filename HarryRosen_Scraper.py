from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import csv
import datetime
import pytz


Current_Time = datetime.datetime.now(tz=pytz.timezone('Canada/Mountain'))
Current_Date = Current_Time.date()
File_Name = str(Current_Date)


def parse():

    url = request.html.find('a')

    for line in url:
        links = line.absolute_links

        for li in links:
            if "product" in str(li):
                print(li)
                Product_URL = str(li)
                
                try:

                    source = requests.get(f'{Product_URL}').text

                    soup = BeautifulSoup(source,'lxml')


                    Product_Info = soup.find('div', class_="mt-6 px-3 lg:px-0")


                    Category = soup.find('a', class_ = "text-xs uppercase text-primary leading-none font-bold tracking-wider whitespace-nowrap text-primary").text

                    Brand = Product_Info.h1.a.text

                    Product_Name=Product_Info.h1.next_sibling.text


                    Product_Color = Product_Info.find('span', class_="block text-sm sm:text-base mt-2 text-grays-600 capitalize").text
                    Color = Product_Color.split(": ")[1]


                    Sale_Section = Product_Info.find('div','span', class_='flex flex-wrap')
                    Sale_Tag = Sale_Section.text.split('$')


                    Sale_Price = float(Sale_Tag[1])
                    Original_Price = float(Sale_Tag[2].split('S')[0])



                    with open(f'{File_Name}.csv', 'a', newline='', encoding='utf-8') as f:

                        w = csv.writer(f, delimiter = '\t')
                        w.writerow([Category, Brand, Product_Name, Color, Sale_Price, Original_Price, Product_URL, File_Name])
                
                except AttributeError as e:
                    print('Product probably sold out!')
                    print(Product_URL)
                    print(e) 
                except Exception as e:
                    print('Oops! Unkonwn error retrieve this page: ')
                    print(Product_URL)
                    print(e)




while True:
    try:
        URL_From_User = input('Provide URL fromn Harry Rosen Sales page: ')
        if 'harryrosen.com/en/shop/sale' in URL_From_User and '&page=' not in URL_From_User:
            break
        print('please remove "&page=x" from url')
        print('"harryrosen.com/en/shop/sale" should be part of url')
    
    except Exception as e:
        print(e)

print('\n\nReminder: Each page takes 1 minute to process')




with open(f'{File_Name}.csv', 'a', newline='', encoding='utf-8') as f:

                        w = csv.writer(f, delimiter = '\t')
                        w.writerow(['category', 'brand', 'product_name', 'color', 'sale_price', 'original_price', 'link', 'date'])



Page_Num =1

while True:
    
    URL = str(URL_From_User) + f'&page={Page_Num}'

    session = HTMLSession()
    request = session.get(f'{URL}')

    request.html.render(sleep=1,timeout=20)

    First_Product = request.html.xpath('//*[@id="prp_product_1"]')

    if len(First_Product) == 0:
        print(f'Task complete! {Page_Num-1} page(s) processed in total\n')
        break
    
    parse()
    
    print(f"\n\n\nMoving on to page {Page_Num+1}\n\n\n")
    Page_Num+=1

    



# Sample URL:  https://www.harryrosen.com/en/shop/sale?level3Category=Coats

