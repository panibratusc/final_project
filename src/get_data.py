import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup

flu_2022_df = pd.read_csv("/Users/macbook/DS510/final_project/data/raw/Influenza_Vaccination_Coverage_for_All_Ages__6__Months_.csv")
#print(flu_2022_df.head())
# I'm choosing the range of the Flu Vaccination between 2022-2023
flu_2022_23 = flu_2022_df[flu_2022_df['Season/Survey Year'] == '2022-23']
flu_2022_23['Estimate (%)'] = pd.to_numeric(flu_2022_23['Estimate (%)'], errors='coerce')
#I'm trying to find the average precentage of people vaccinated between the years 2022-2023 
average_percentage = flu_2022_23['Estimate (%)'].mean()
#print(average_percentage)
#retriving data from the cdc website and get html response to get CSV data using beautifulsoup
url = "https://data.cdc.gov/api/views/fz77-au2z/rows.csv?accessType=GET"
response  = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
csv_data_tag = soup.find("pre")
if csv_data_tag:
    csv_data = csv_data_tag.get_text()
    csv_reader = csv.reader(csv_data.splitlines())
    for row in csv_reader:
        print(row)
else:
    print("CSV data not found.")