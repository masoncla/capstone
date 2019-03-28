from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
from nltk import sent_tokenize 
from sys import argv, exit

def make_soup(url):
    '''
    INPUT: url string
    OUTPUT: BeautifulSoup object
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

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

def get_categories(url):
    soup = make_soup(url)
    cats = soup.find_all('option', class_='level-0')
    cat_names = [cat.text.lower() for cat in cats]
    # remove duplicates
    return [word for word in cat_names[25:] if ' ' not in word and '/' not in word]

def get_recipe_links(url):
    soup = make_soup(url)
    links = [link.get("href") for link in soup.find_all('a', class_='more-link')]
    return links

def get_recipe_instructions(url):
    soup = make_soup(url)
    recipe = soup.find_all('div', class_="wprm-recipe-instruction-text")

    instructions = [instruct.text for instruct in recipe]
    ins_str = []
    for instruct in instructions:
        for sent in sent_tokenize(instruct):
            ins_str.append(sent)

    return instructions

def get_bodies_on_page(url):
    df = pd.DataFrame(columns=['title', 'body', 'instructions'])
    links = get_recipe_links(url)
    for link in links:
        try:
            body, title = grab_body(link)
            instruct = get_recipe_instructions(link)
            A = pd.DataFrame([[title, body, instruct]], columns=['title', 'body', 'instructions'])
            df = pd.concat([df,A], axis=0, ignore_index=True)
        except:
            continue
    return df

def get_next_page(url):
    soup = make_soup(url)
    next_ = soup.find('li', class_="pagination-next").find("a").get("href")
    return next_    

def scrape_sm():    
    cats = get_categories('https://thesaltymarshmallow.com/recipes/')
    data = pd.DataFrame(columns = ['title','body','instructions'])
    for cat in cats:
        i = 0
        url = 'https://thesaltymarshmallow.com/category/{}/'.format(cat)
        data = pd.concat([data, get_bodies_on_page(url)], axis=0, ignore_index=True)
        while i <= 37:
            try:
                url = get_next_page(url)
                data = pd.concat([data, get_bodies_on_page(url)], axis=0, ignore_index=True)
                i+=1
            except:
                i+=1
                continue
    return data



if __name__ == '__main__':
    data = scrape_sm()

    data.to_csv('data/salty_mallow.csv')