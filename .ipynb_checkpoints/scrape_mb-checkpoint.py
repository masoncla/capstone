from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
from sys import argv, exit

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
    posts = soup.find_all('a', class_="entry-title-link")
    links = [post.get("href") for post in posts]
    return links

def grab_body(url):
    '''
    INPUT: blog post url
    OUTPUT: list of sentence strings
    '''
    soup = make_soup(url)
    art = soup.article
    recipe = art.find('div', class_="wprm-recipe-container")
    
    recipe_start = str(recipe)[:30]
    idx = str(art).index(recipe_start)
    data = str(art)[:idx]
    data = re.sub(r'<.*?>', '', data)
    data = re.sub('\xa0', '', data)
    data = re.sub('\n', ' ', data)
    return data, soup.title.text

def get_bodies_on_page(url):
    df = pd.DataFrame(columns=['title', 'body', 'url'])
    links = get_recipe_links(url)
    for link in links:
        body, title = grab_body(link)
        A = pd.DataFrame([[title, body, url]], columns=['title', 'body', 'url'])
        df = pd.concat([df,A], axis=0)
    return df

def scrape_mb(url):
    data = pd.DataFrame(columns=['title','body','url'])
    data = pd.concat([data, get_bodies_on_page(url)], axis=0)
    for n in range(2, 61):
        url = 'https://minimalistbaker.com/recipes/page/{}/'.format(i)
        df = get_bodies_on_page(url)
        data = pd.concat([data, df], axis=0)
    return data

if __name__ == '__main__':
    # get url for recipe index
    url = argv[1]
    # get the data
    df = scrape_mb(url)
    # write to a csv
    df.to_csv('data/minimal_bake.csv')