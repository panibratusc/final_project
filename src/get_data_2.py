import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from io import StringIO

# Two NBC html elements we are searching for that contain the caption and description of recent articles
# <h2 class='wide-tease-item__headline'>
#<div class='wide-tease-item__description'>
url = 'https://www.nbcnews.com/world'
response = requests.get(url)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    headlines_NBC = soup.find_all('h2', class_='wide-tease-item__headline')
    descriptions_NBC = soup.find_all('div', class_='wide-tease-item__description')
    for headline_NBC in headlines_NBC:
        print(headline_NBC.text)
    for description_NBC in descriptions_NBC:
        print(description_NBC.text)