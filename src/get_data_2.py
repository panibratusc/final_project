import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from io import StringIO
import argparse

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
#<p class='1pga48a>
def get_NYT():
    url = "https://www.nytimes.com/section/world"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        headlines_NYT = soup.find_all('h3', class_= 'css-1kv6qi')
        descriptions_NYT = soup.find_all('p', class_='1pga48a')
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
        return [headline_CNN.text for headline_CNN in headlines_CNN]
    else:
        print("Error: Response code", response.status_code)
        return []
    
#Making the arrays the same length 
def arrays_same_length(arr1, arr2):
    min_length = min(len(arr1), len(arr2))
    return arr1[:min_length], arr2[:min_length]
    
#Creating a datatable for all the news sources
def create_data_table(headlines, descriptions):
    df = pd.DataFrame({
        'Headlines': headlines, 
        'Descriptions': descriptions
    })
    return df
def main():
    parser = argparse.ArgumentParser(description='create a data table of descriptions and headlines from the various news sources')
    parser.add_argument('--source', choices=['CNN','NYT','NBC'], help="Specify the news source: 'NBC', 'NYT', or 'CNN'", required=True)
    args = parser.parse_args()
    if args.source == 'NBC':
        headlines, descriptions = get_NBC()
    elif args.source == 'NYT':
        headlines, descriptions = get_NYT()
    elif args.source == 'CNN':
        headlines = get_CNN()
        descriptions = [''] * len('headlines')
    
    data_table = create_data_table(headlines, descriptions)
    print(data_table)
    
if __name__ == '__main__':
     main()
#get_CNN()