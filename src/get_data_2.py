import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from io import StringIO

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
        return [headline_NYT.text for headline_NYT in headlines_NYT], [description_NYT.text for description_NYT in descriptions_NYT]
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
        headlines_text_CNN = soup.find_all('span', class_='container__headline-text')
        return [headline_text_CNN.text for headline_text_CNN in headlines_text_CNN]
    else:
        print("Error: Response code", response.status_code)

def combine_data():
    NBC_words = get_NBC()
    NYT_words = get_NYT()
    CNN_words = get_CNN()
    all_words = list(CNN_words + NYT_words + NBC_words)
    all_words = [word.lower() for word in all_words]
    df = pd.DataFrame(all_words, columns=['Words'])
    print(df)
    
combine_data()
    