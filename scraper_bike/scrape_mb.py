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
    #data = re.sub('\n', ' ', data)
    return data, soup.title.text

def get_recipe_instructions(url):
    '''
    returns the a list of the instruction sentence strings from the recipe post at the inputted url
    '''
    soup = make_soup(url)
    # get recipe instruction conatiners
    recipe = soup.find_all('div', class_="wprm-recipe-instruction-text")
    # isolate just the text
    instructions = [instruct.text for instruct in recipe]
    return ''.join(instructions)


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

def scrape_mb(url):
    data = pd.DataFrame(columns=['title','body', 'instructions'])
    data = pd.concat([data, get_bodies_on_page(url)], axis=0)
    for n in range(2, 61):
        url = 'https://minimalistbaker.com/recipes/page/{}/'.format(n)
        df = get_bodies_on_page(url)
        data = pd.concat([data, df], axis=0, ignore_index=True)
    return data

if __name__ == '__main__':
    # get url for recipe index
    url = argv[1]

    # get the data
    df = scrape_mb(url)

    # write to a csv
    df.to_csv(argv[2])