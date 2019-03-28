from bs4 import BeautifulSoup
import requests
import urllib
import os
import re
from urllib.request import urlopen
from nltk import sent_tokenize
import pandas as pd
import numpy as np

def make_soup(url):
    '''
    INPUT: url string
    OUTPUT: BeautifulSoup object
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_recipe_links(url):
    '''
    Gets all links to recipe post on one archival page.
    Returns list of strings containing the URLs
    '''
    soup = make_soup(url)
    posts = soup.find_all('div', class_="archive-post")
    links = [item.find("a").get("href") for item in posts]
    return links

def grab_body(url):
    soup = make_soup(url)
    art = soup.article
    text_lines = [text.text for text in art.find_all("p", style='' )]
    inst = soup.find("div", class_="recipe").find("div", class_="instructions").text
    inst = re.sub('\xa0', ' ', inst)
    return ''.join(text_lines), soup.title.text, inst

def get_info_on_page(url):
    df = pd.DataFrame(columns=['title', 'body', 'instructions'])
    links = get_recipe_links(url)
    for link in links:
        try:
            body, title, instruct = grab_body(link)
            d = pd.DataFrame([[title, body, instruct]],columns=['title', 'body', 'instructions'])
            df = pd.concat([df, d], axis=0, ignore_index=True)
        except:
            continue
    return df

def get_cat_links(url):
    soup = make_soup(url)
    cats = soup.find_all("div", class_="archive-post")
    links = [cat.find("a").get("href") for cat in cats]
    return links

def scrape(url):  
    soup = make_soup(url)
    df = pd.DataFrame(columns=['title', 'body', 'instructions'])
    categories = [cat.find("a").get("href") for cat in soup.find_all("div", class_="archive-post")]
    cat_links = [url for url in categories if 'cookbook' not in url and 'dog-food' not in url and 'travel' not in url]
    for cat in cat_links:
        D = get_info_on_page(cat)
        df = pd.concat([df, D], axis=0, ignore_index=True)
        for i in range(10):
            try:
                url = cat+'page/{}/'.format(i)
                D = get_info_on_page(url)
                df = pd.concat([df, D], axis=0, ignore_index=True)
            except:
                continue
    return df

if __name__=='__main__':
    url = 'https://damndelicious.net/recipe-index/'
    data = scrape(url)
    data.to_csv('data/delicious.csv')