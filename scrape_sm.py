from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
from scrape_mb import make_soup
from sys import argv, exit

def get_categories(url):
    soup = make_soup(url)
    cats = soup.find_all('option', class_='level-0')
    cat_names = [cat.text for cat in cats]
    # remove duplicates
    return cat_names[25:]

def get_recipe_links(url):
    soup = make_soup(url)
    links = [link.get("href") for link in soup.find_all('a', class_='more-link')]
    return links

def get_bodies_on_page(url):
    df = pd.DataFrame(columns=['title', 'body', 'url'])
    links = get_recipe_links(url)
    for link in links:
        try:
            body, title = grab_body(link)
            A = pd.DataFrame([[title, body, link]], columns=['title', 'body', 'url'])
            df = pd.concat([df,A], axis=0, ignore_index=True)
        except:
            continue
    return df

def get_next_page(url):
    soup = make_soup(url)
    next_ = soup.find('li', class_="pagination-next").find("a").get("href")
    return next_    

def scrape_sm(url):
    cats = ['pasta', 'breakfast']
    final = pd.DataFrame(columns = ['title','body','url'])
    for cat in cats:
        url = 'https://thesaltymarshmallow.com/category/{}/'.format(cat)
        i = 0
        
        data = pd.DataFrame(columns=['title','body','url'])
        data = pd.concat([data, get_bodies_on_page(url)], axis=0, ignore_index=True)
        
        
        while i < 37:
            try:
                url = get_next_page(url)
                data = pd.concat([data, get_bodies_on_page(url)], axis=0, ignore_index=True)
                i += 1
            except:
                i+=1
                continue
        final = pd.concat([final, data], axis=0, ignore_index=True)
    return final 



if __name__ == '__main__':
    data = scrape_sm(argv[1])

    data.to_csv('data/salty_mallow.csv')