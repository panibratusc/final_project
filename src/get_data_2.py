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
def get_NBC(limit=None):
    url = 'https://www.nbcnews.com/world'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        headlines_NBC = soup.find_all('h2', class_='wide-tease-item__headline')
        descriptions_NBC = soup.find_all('div', class_='wide-tease-item__description')
        if limit:
            headlines_NBC = headlines_NBC[:limit]
            descriptions_NBC = descriptions_NBC[:limit]
        return [headline_NBC.text for headline_NBC in headlines_NBC], [description_NBC.text for description_NBC in descriptions_NBC]
    else:
        print("Error: Response code", response.status_code)

#NYT retrieving data from the World Section
#<h3 class='css-1kv6qi>
#<p class='css-1pga48a>
def get_NYT(limit=None):
    url = "https://www.nytimes.com/section/world"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        headlines_NYT = soup.find_all('h3', class_= 'css-1kv6qi')
        descriptions_NYT = soup.find_all('p', class_='css-1pga48a')
        if limit:
            headlines_NYT = headlines_NYT[:limit]
            headlines_NYT = headlines_NYT[:limit]
        headlines_NYT, descriptions_NYT = arrays_same_length(
            [headline.text for headline in headlines_NYT],
            [description.text for description in descriptions_NYT]
        )
        return headlines_NYT, descriptions_NYT
    else:
        print("Error: Response code", response.status_code)


#Retriving data from the CNN website
#span class = 'container__headline-text'
def get_CNN_general(urls,limit=None):
    all_headlines = []
    all_content = []
    all_subheadings = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            subheadings_CNN = soup.find_all('h2')
            headlines_CNN = soup.find_all('h1', class_='headline__text')
            contents_CNN = soup.find_all('p', class_='paragraph')
            headlines = [headline.text.strip() for headline in headlines_CNN]
            subheadings = [subheading.text.strip() for subheading in subheadings_CNN]
            content = [content.text.strip() for content in contents_CNN]
            if limit:
                subheading_CNN = subheading_CNN[:limit]
                headlines_CNN = headlines_CNN[:limit]
                content_CNN = content_CNN[:limit]
                print(headlines, content, subheadings)
                return headlines, content, subheadings
        else:
            print("Error: Response code", response.status_code)
            return []
urls = ["https://www.cnn.com/2024/04/20/europe/russia-belgorod-impact-ukraine-war-intl-cmd/index.html","https://www.cnn.com/2024/04/14/europe/russia-tactics-ukraine-energy-power-strikes-intl/index.html", 
 "https://www.cnn.com/2024/04/20/middleeast/palestinian-ambulance-driver-shot-intl-latam/index.html"]
#
# def get_CNN(limit=None):
#     url = "https://www.cnn.com/world"
#     response = requests.get(url)
#     if response.status_code == 200:
#         html = response.text
#         soup = BeautifulSoup(html, 'html.parser')
#         headlines_CNN = soup.find_all('span', class_='container__headline-text')
#         headlines = [headline.text.strip() for headline in headlines_CNN]
#         if limit:
#             headlines_CNN = headlines_CNN[:limit]
#         return headlines
#     else:
#         print("Error: Response code", response.status_code)
#         return []

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
             headlines, descriptions = get_NBC(limit=args.scrape)
        elif source == 'NYT':
            headlines, descriptions = get_NYT(limit=args.scrape)
        elif source == 'CNN':
             headlines = get_CNN_general(limit=args.scrape)
             descriptions = [''] * len(headlines)
        data_table = create_data_table(headlines, descriptions, source)
        data_tables.append(data_table)
        
    combined_data_table = pd.concat(data_tables, ignore_index=True)
    if args.save:
        combined_data_table.to_csv(args.save, index=False)
        print(f"Data has been saved to {args.save.name} in CSV format")

        # pass
    else:
        print(combined_data_table)
    
if __name__ == '__main__':
     main()