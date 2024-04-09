import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from io import StringIO

# flu_2022_df = pd.read_csv("/Users/macbook/DS510/final_project/data/raw/Influenza_Vaccination_Coverage_for_All_Ages__6__Months_.csv")
# print(flu_2022_df.head())
# # I'm choosing the range of the Flu Vaccination between 2022-2023
# flu_2022_23 = flu_2022_df[flu_2022_df['Season/Survey Year'] == '2022-23']
#flu_2022_23.loc[:,'Estimate (%)'] = pd.to_numeric(flu_2022_23['Estimate (%)'], errors='coerce')
#I'm trying to find the average precentage of people vaccinated between the years 2022-2023 
# average_percentage = flu_2022_23['Estimate (%)'].mean()
#print(average_percentage)
#retriving data from the cdc website and get html "response to get CSV data using beautifulsoup
# url = "https://covid.cdc.gov/covid-data-tracker/#vaccinations_vacc-people-booster-percent-pop5"
# response  = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
# csv_link = soup.find("button",href = True, text = " Download Data ")
# if csv_link:
#     csv_url = csv_link["href"]
#     csv_response = requests.get(csv_url)
    #print(csv_response.text)
    # csv_data_covid = csv_response.text
    # rows = csv_data_covid.split("\n")
    # for row in rows:
    #     columns = row.split(",")
    #     for column in columns:
    #         print(column)
    #     print()
    # csv_data_covid = csv_response.content.decode("utf-8")
    # covid_df = pd.read_csv(StringIO(csv_data_covid))
    # print(covid_df.head())
    

    


# #csv_data_tag = soup.find("pre")
# #if csv_data_tag:
#     csv_data = csv_data_tag.get_text()
#     csv_reader = csv.reader(csv_data.splitlines())
#     for row in csv_reader:
#         print(row)
# #else:
#     print("CSV data not found.")


#scrapping data using table
def scrape_data(url):
    
    response  = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup.prettify())
        table = soup.find('table')
        
        if table:
            data = []
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                cols = [col.text.strip() for col in cols]
                data.append(cols)
            return data
        
        else:
            print('error no table with class name')
            return None
            
    else:
        print('error failed to retrive data')
        return None
    
url = 'https://covid.cdc.gov/covid-data-tracker/#vaccinations_vacc-total-admin-count-total'
scraped_data = scrape_data(url)

if scraped_data:
    for row in scraped_data:
        print(row)
