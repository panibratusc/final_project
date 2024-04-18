import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from io import StringIO
import argparse
import sys


#Making the arrays the same length 
def arrays_same_length(arr1, arr2):
    min_length = min(len(arr1), len(arr2))
    return arr1[:min_length], arr2[:min_length]

# Two NBC html elements we are searching for that contain the caption and description of recent articles
# <h2 class='wide-tease-item__headline'>
#<div class='wide-tease-item__description'>
def get_NBC():
    url = 'https://www.nbcnews.com/world'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        headlines_NBC = soup.find_all('h2', class_='wide-tease-item__headline')
        descriptions_NBC = soup.find_all('div', class_='wide-tease-item__description')
        return [headline_NBC.text for headline_NBC in headlines_NBC], [description_NBC.text for description_NBC in descriptions_NBC]
    else:
        print("Error: Response code", response.status_code)

#NYT retrieving data from the World Section
#<h3 class='css-1kv6qi>
#<p class='css-1pga48a>
def get_NYT():
    url = "https://www.nytimes.com/section/world"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        headlines_NYT = soup.find_all('h3', class_= 'css-1kv6qi')
        descriptions_NYT = soup.find_all('p', class_='css-1pga48a')
        headlines_NYT, descriptions_NYT = arrays_same_length(
            [headline.text for headline in headlines_NYT],
            [description.text for description in descriptions_NYT]
        )
        return headlines_NYT, descriptions_NYT
    else:
        print("Error: Response code", response.status_code)


#Retriving data from the Wall Street Journal
#span class = 'container__headline-text'
def get_CNN():
    url = "https://www.cnn.com/world"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        headlines_CNN = soup.find_all('span', class_='container__headline-text')
        headlines = [headline.text.strip() for headline in headlines_CNN]
        # descriptions_CNN = [[''] * len(headlines_CNN)]
        # headlines_CNN, descriptions_CNN = arrays_same_length(
        #     [headline.text for headline in headlines_CNN],
        #     [description.text for description in descriptions_CNN]
        # )
        return headlines
    else:
        print("Error: Response code", response.status_code)
        return []
    


#Creating a datatable for all the news sources
def create_data_table(headlines, descriptions,source):
    df = pd.DataFrame({
        'Headlines': headlines, 
        'Descriptions': descriptions,
        'Source': source
    })
    return df
def main():
    parser = argparse.ArgumentParser(description='create a data table of descriptions and headlines from the various news sources')
    parser.add_argument('--source', nargs = '+', choices=['CNN','NYT','NBC'], help="Specify the news source: 'NBC', 'NYT', or 'CNN'", required=True)
    parser.add_argument('--scrape', type=int, help="Specify the number of records")
    parser.add_argument('--save', type=argparse.FileType('w'), help="Specify the save location")
    args = parser.parse_args()
    data_tables = []
    for source in args.source:
        if source == 'NBC':
            headlines, descriptions = get_NBC()
        elif source == 'NYT':
            headlines, descriptions = get_NYT()
        elif source == 'CNN':
            headlines = get_CNN()
            descriptions = [''] * len(headlines)
        data_table = create_data_table(headlines, descriptions, source)
        data_tables.append(data_table)
        
    combined_data_table = pd.concat(data_tables, ignore_index=True)
    if args.save:
        combined_data_table.to_csv(args.save, index=False)
        # fieldnames = ["sources", "descriptions", "headlines"]
        # writer = csv.DictWriter(args.save, fieldnames=fieldnames)
        
        # # Write the header row
        # writer.writeheader()
        
        # # Write the data rows
        # for row in data_tables:
        #     writer.writerow(row)
        
        # # Close the file explicitly
        # args.save.close()
        
        print(f"Data has been saved to {args.save.name} in CSV format")

        # pass
    else:
        print(combined_data_table)
    
if __name__ == '__main__':
     main()