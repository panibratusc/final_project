import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_author_and_date(url_series):
    result = []
    for url in url_series:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        article_date = soup.select('div[data-testid="article-body-timestamp"] time')[0].contents[0]
        article_author = soup.select('span.byline-name')[0].text
        result.append((article_author, article_date))
    return result

def get_NBC(limit=None):
    url = 'https://www.nbcnews.com/Israel-Hamas-war-Gaza-Strip-conflict'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        df_NBC = pd.DataFrame(columns=['headline', 'description', 'url'])
        article_wrappers = soup.find_all('div', class_='wide-tease-item__info-wrapper')
        headlines_NBC = [article.find('h2', class_='wide-tease-item__headline') for article in article_wrappers]
        df_NBC['headline'] = [headline_NBC.text for headline_NBC in headlines_NBC]
        df_NBC['description'] = [article.find('div', class_='wide-tease-item__description').text for article in article_wrappers]
        df_NBC['url'] = [headline.parent['href'] for headline in headlines_NBC]
        authors_and_dates = get_author_and_date(df_NBC['url'])
        df_NBC['author'] = [author_and_date[0] for author_and_date in authors_and_dates]
        df_NBC['date'] = [author_and_date[1] for author_and_date in authors_and_dates]
        
        if limit:
            df_NBC = df_NBC.head(limit)
        print(df_NBC)
        return df_NBC
        
    else:
        print("Error: Response code", response.status_code)
    
#results = get_NBC()

#Ukraine
def get_NBC_Ukraine(limit=None):
    url = 'https://www.nbcnews.com/world/russia-ukraine-news'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        df_NBC_Ukraine = pd.DataFrame(columns=['headline', 'description', 'url'])
        article_wrappers = soup.find_all('div', class_='wide-tease-item__info-wrapper')
        headlines_NBC = [article.find('h2', class_='wide-tease-item__headline') for article in article_wrappers]
        df_NBC_Ukraine['headline'] = [headline_NBC.text for headline_NBC in headlines_NBC]
        df_NBC_Ukraine['description'] = [article.find('div', class_='wide-tease-item__description').text for article in article_wrappers]
        df_NBC_Ukraine['url'] = [headline.parent['href'] for headline in headlines_NBC]
        authors_and_dates = get_author_and_date(df_NBC_Ukraine['url'])
        df_NBC_Ukraine['author'] = [author_and_date[0] for author_and_date in authors_and_dates]
        df_NBC_Ukraine['date'] = [author_and_date[1] for author_and_date in authors_and_dates]
        
        if limit:
            df_NBC_Ukraine = df_NBC_Ukraine.head(limit)
        print(df_NBC_Ukraine)
        return df_NBC_Ukraine
        
    else:
        print("Error: Response code", response.status_code)
    
#results = get_NBC_Ukraine()

#NYT Israel
def get_author_and_date_NYT(url_series):
    result = []
    for url in url_series:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        article_date = soup.select('div[class_ = "css-agrsgss"] time')[0].contents[0]
        article_author = soup.select('div[class_ = "css-1i4y2t3]')[0].text
        result.append((article_author, article_date))
    return result

def get_NYT_IsraelPalestine(limit=None):
    url = 'https://www.nytimes.com/news-event/israel-hamas-gaza'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        df_NYT_IsraelPalestine = pd.DataFrame(columns=['headline', 'description', 'url'])
        article_wrappers = soup.find_all('article', class_='css-1l4spti')
        headlines_NYTIsraelPalestine = [article.find('h3', class_='css-1kv6qi') for article in article_wrappers]
        df_NYT_IsraelPalestine['headline'] = [headline_NYT.text if headline_NYT else None for headline_NYT in headlines_NYTIsraelPalestine]
        #df_NYT_IsraelPalestine['headline'] = [headline_NYT.text for headline_NYT in headlines_NYTIsraelPalestine]
        df_NYT_IsraelPalestine['description'] = [article.find('p', class_='css-1n8orw4').text if article.find('p', class_='css-1n8orw4') else None for article in article_wrappers]
        #df_NYT_IsraelPalestine['description'] = [article.find('p', class_='css-1n8orw4').text for article in article_wrappers]
        df_NYT_IsraelPalestine['url'] = [headline.parent['href'] for headline in headlines_NYTIsraelPalestine]
        authors_and_dates = get_author_and_date(df_NYT_IsraelPalestine['url'])
        df_NYT_IsraelPalestine['author'] = [author_and_date[0] for author_and_date in authors_and_dates]
        df_NYT_IsraelPalestine['date'] = [author_and_date[1] for author_and_date in authors_and_dates]
        
        if limit:
            df_NYT_IsraelPalestine = df_NYT_IsraelPalestine.head(limit)
        print(df_NYT_IsraelPalestine)
        return df_NYT_IsraelPalestine
        
    else:
        print("Error: Response code", response.status_code)

get_NYT_IsraelPalestine()

#NYT Ukraine_Russia
def get_NYT_UkraineRussia(limit=None):
    url = 'https://www.nytimes.com/news-event/ukraine-russia'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        df_NYT_Ukraine_Russia = pd.DataFrame(columns=['headline', 'description', 'url'])
        article_wrappers = soup.find_all('article', class_='css-1l4spti')
        headlines_NYTUkraineRussia = [article.find('h3', class_='css-1kv6qi') for article in article_wrappers]
        df_NYT_Ukraine_Russia['headline'] = [headline_NYT.text if headline_NYT else None for headline_NYT in headlines_NYTUkraineRussia]
        #df_NYT_IsraelPalestine['headline'] = [headline_NYT.text for headline_NYT in headlines_NYTIsraelPalestine]
        df_NYT_Ukraine_Russia['description'] = [article.find('p', class_='css-1n8orw4').text if article.find('p', class_='css-1n8orw4') else None for article in article_wrappers]
        #df_NYT_IsraelPalestine['description'] = [article.find('p', class_='css-1n8orw4').text for article in article_wrappers]
        df_NYT_Ukraine_Russia['url'] = [headline.parent['href'] for headline in headlines_NYTUkraineRussia]
        authors_and_dates = get_author_and_date(df_NYT_Ukraine_Russia['url'])
        df_NYT_Ukraine_Russia['author'] = [author_and_date[0] for author_and_date in authors_and_dates]
        df_NYT_Ukraine_Russia['date'] = [author_and_date[1] for author_and_date in authors_and_dates]
        
        if limit:
            df_NYT_Ukraine_Russia = df_NYT_Ukraine_Russia.head(limit)
        print(df_NYT_Ukraine_Russia)
        return df_NYT_Ukraine_Russia
        
    else:
        print("Error: Response code", response.status_code)

get_NYT_UkraineRussia()

