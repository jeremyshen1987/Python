import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pytz
import csv
import os


Current_Time = datetime.datetime.now(tz=pytz.timezone('Canada/Mountain'))
Current_Date = Current_Time.date()
File_Name = str(Current_Date)


def scrapper(property_url):

    try:
    
        df = pd.read_html(property_url)

        if len(df[0][1]) <5:
            print('\nSkipped: Missing Critical Informatino: Land Size / Years Built\n')
            return


        baths = df[0][1][0]
        beds = df[0][1][1]
        floor_space = df[0][1][2].split('(')[1].split('s')[0].replace(',','')
        land_size = df[0][1][3].split('(')[1].split('s')[0].replace(',','')
        years_built = df[0][1][4]


        if df[2]["Value"][0] == None:

            print('cannot find transaction field')
            last_sold='Unknown'
            last_sold_date=df[1]["Date"][0]
            
        else:

            last_sold = df[2]["Value"][0].replace('$','').replace(',','')
            last_sold_date = df[2]["Date"][0]



        
        get_html = s.get(property_url).text
        soup = BeautifulSoup(get_html,'lxml')

        assessment = soup.find_all('p', class_ = 'chakra-text css-23jksx')
        city_appraisal = assessment[1].text.replace('$','').replace(',','')

        community = soup.find('a',class_ = 'chakra-button css-15ptba5').text

        addr = soup.find('h1', class_ = 'chakra-text css-1qktfcj').text
    



        with open(f'{File_Name}.csv', 'a', newline='', encoding='utf-8') as f:

            w = csv.writer(f, delimiter = '\t')
            w.writerow([addr, community, years_built, beds, baths, floor_space, land_size, last_sold, last_sold_date, city_appraisal, File_Name, property_url])

    except Exception as e:
        print(e)




def control_flow(page_num):

    try:

        while True:
        
            url = f'https://www.honestdoor.com/recently-sold/ab/calgary?page={page_num}'

            source = requests.get(url).text
            soup = BeautifulSoup(source,'lxml')

            dat = soup.find_all('p',class_ = 'chakra-text css-1uss9mh')

            days_ago_list = []

            for li in dat:
                days_ago = li.text.split('d ')[1].split(' d')[0]
                days_ago_list.append(days_ago)


            property_list = []

            link = soup.find_all('a', class_ = 'chakra-link css-1lfxdey')

            for every_url in link:
                if 'property' in every_url['href']:

                    absolute_url = 'https://www.honestdoor.com' + every_url['href']
                    property_list.append(absolute_url)


            for days, property_url in zip(days_ago_list,property_list):
                if int(days) < 16:
                    
                    print(property_url)
                    scrapper(property_url)
                  

            if int(days_ago_list[-1]) > 15:
                print('\n\n Task complete!')
                break


            page_num+=1
            print(f'\n\n\nMoving on to page: {page_num}\n\n\n')

    except Exception as e:
        print(e)



login_url = 'https://honestdoor.auth0.com/u/login?state=hKFo2SB5T0h2XzhqSDBaeHlnRmZJRDlMR05vRV93bXZZdmpqbqFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIGlXUmJDazdmbEtCTTRmdHhvMHpLRTNkOTRPblBWVERHo2NpZNkgR3Rsa1FHN2g3d2NxNjNhemlsQXZndkUxNjFPRklpSXk'


user = os.environ.get('HD_User')
password = os.environ.get('HD_PW')

payload = {

    'state': 'hKFo2SB5T0h2XzhqSDBaeHlnRmZJRDlMR05vRV93bXZZdmpqbqFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIGlXUmJDazdmbEtCTTRmdHhvMHpLRTNkOTRPblBWVERHo2NpZNkgR3Rsa1FHN2g3d2NxNjNhemlsQXZndkUxNjFPRklpSXk',
    'username':user,
    'password':password,
    'action': 'default'

}


Pg_Num = 1

with requests.session() as s:

    p = s.post(login_url, data = payload)

    print(p.status_code)

    with open(f'{File_Name}.csv', 'a', newline='', encoding='utf-8') as f:

        w = csv.writer(f, delimiter = '\t')
        w.writerow(['addr', 'community', 'years_built', 'beds', 'baths', 'floor_space', 'land_size', 'last_sold', 'last_sold_date', 'city_appraisal', 'record_date','link'])

    control_flow(Pg_Num)



