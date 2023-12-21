import pandas as pd
from bs4 import BeautifulSoup
import requests


# URLからBeautifulSoupオブジェクトを取得する関数
def ret_soup(url):
    response = requests.get(url)  # URLからHTTPレスポンスを取得
    response.encoding = response.apparent_encoding  # 文字コードを適切に設定

    # BeautifulSoupを使用してHTMLを解析し、soupオブジェクトを返す
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


# Qiitaのトップページから記事のデータを取得
soup = ret_soup('https://qiita.com/')
articles = soup.find_all('article')  # すべての記事要素を取得

article_list = []
for article in articles:
    article_url = article.find_all('a')[0]['href']  # 記事のURLを取得
    tags = [tag.text for tag in article.find_all(
        'a', class_='style-1a4ckru')]  # 記事に付けられたタグを取得

    article_list.append({'url': article_url, 'tags': tags})  # 記事情報をリストに追加


for article in article_list:
    article_soup = ret_soup(article['url'])  # 記事ページのsoupオブジェクトを取得
    article_text = article_soup.find(
        'div', id='personal-public-article-body').text  # 記事の本文を取得

    article['text'] = article_text  # 本文を記事情報に追加

# 取得したデータをCSVファイルに保存
pd.DataFrame(article_list).to_csv('qiita.csv', index=False)
