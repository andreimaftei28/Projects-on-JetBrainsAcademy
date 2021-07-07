"""Simple web scraper script"""

import os
import requests
import string
from bs4 import BeautifulSoup


def get_response(url, payload=None):
    """
    :param url: -address to be scrapped
    :param payload: - None by default
    :return: page content if status == 200 else a message with status code
    """
    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    r = requests.get(url, headers=headers, params=payload)
    if r.status_code == 200:
        return r.content
    return f"\nThe URL returned {r.status_code}!"


def find_news(content, typo):
    """

    :param content: the returned content from get_response function
    :param typo: type of the article desired by user
    :return: a list of article links if content is provided or a message with the status code
    """
    if isinstance(content, str):
        return content
    soup = BeautifulSoup(content, "lxml")
    articles = soup.find_all("article")
    links = []
    for article in articles:
        article_type = article.find("span", class_='c-meta__type').text
        if article_type == typo:
            links.append(article.find("a")["href"])
    return links


def get_body(data, num):
    """
    :param data: links from find_news function
    :param num: number of page to create dir
    :return: a list with all the saved articles
    """

    if isinstance(data, str):
        return data
    docs = []
    directory = f"Page_{num}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    for link in data:
        url = f"https://www.nature.com{link}"
        content = get_response(url)
        soup = BeautifulSoup(content, 'lxml')
        title = soup.find("meta", property="og:title")["content"]
        translator = str.maketrans("", "", string.punctuation)
        name = f"{title.translate(translator).replace(' ', '_')}.txt"
        with open(f"{directory}/{name}", "w", encoding="UTF-8") as file:
            try:
                body = soup.find("div", {"class": "c-article-body"}).get_text().lstrip().replace("\r", "").replace("\n", "")
            except AttributeError:
                body = soup.find("div", {"class": "article-item__body"}).get_text().lstrip().replace("\r", "").replace("\n", "")
            file.write(body)
        docs.append(name)
    return docs


url_ = "https://www.nature.com/nature/articles"
page_num = int(input())
article_typo = input()
for page in range(1, page_num + 1):
    payload_ = {"page": page}
    get_body(find_news(get_response(url_, payload_), article_typo), page)
print("Saved all articles")
