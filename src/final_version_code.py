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
    print(result)
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
    
results = get_NBC()