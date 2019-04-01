from bs4 import BeautifulSoup
import requests
import urllib
import os
import re
from urllib.request import urlopen
from nltk import sent_tokenize
import pandas as pd
import numpy as np

main_url = 'https://www.yellowblissroad.com/category/recipes/main-course/'

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
    body = [line.text for line in soup.find("div", class_="entry-content").find_all("p") if line.text !='' and line.text!='     '  and line.text!='\xa0']
    return body

def get_recipe_links(url):
    soup = make_soup(url)
    links = [link.get("href") for link in soup.find_all('a', class_='entry-title-link')]
    return links

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
    df = pd.DataFrame(columns=['body', 'instructions'])
    links = get_recipe_links(url)
    for link in links:
        try:
            body = grab_body(link)
            instruct = get_recipe_instructions(link)
            A = pd.DataFrame([[body, instruct]], columns=['body', 'instructions'])
            df = pd.concat([df,A], axis=0, ignore_index=True)
        except:
            continue
    return df

def scrape_it_all(url):
    data = pd.DataFrame(columns=['body', 'instructions'])
    data = pd.concat([data, get_bodies_on_page(url)], axis=0, ignore_index=True)
    for n in range(2, 36):
        url = 'https://www.yellowblissroad.com/category/recipes/main-course/page/{}/'.format(n)
        df = get_bodies_on_page(url)
        data = pd.concat([data, df], axis=0, ignore_index=True)
    return data





if __name__=='__main__':
    df = scrape_it_all(main_url)
    df.to_csv('data/yellow.csv')