from bs4 import BeautifulSoup
import requests
import urllib
import os
import re
import pandas as pd
from sys import argv, exit

def make_soup(url):
    '''
    INPUT: url string
    OUTPUT: BeautifulSoup object
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def next_link(url):
    soup_ = make_soup(url)
    link = soup_.find('a', rel='next')
    if link:
        return link.get('href')
    else:
        return False

def grab_body(url):
    '''
    INPUT: blog post url
    OUTPUT: list of sentence strings
    '''
    soup = make_soup(url)
    art = soup.article
    recipe = art.find('div', class_="wprm-recipe-container")
    recipe_start = str(recipe)[:30]
    if recipe_start != 'None':
        idx = str(art).index(recipe_start)
        data = str(art)[:idx]
        data = re.sub(r'<.*?>', '', data)
        data = re.sub('\xa0', '', data)
        return data, soup.title.text
    else:
        return (False, False)

if __name__ == '__main__':
    # create empty dataframe to hold scraped data
    df = pd.DataFrame(columns=['title', 'body', 'url'])
    i = 0
    # get url input from user
    url = argv[1]

    #scrape blog posts in one category
    for i in range(50):
        body, title = grab_body(url)
        if body == False:
            continue

        A = pd.DataFrame([[title, body, url]], columns=['title', 'body', 'url'])
        df = pd.concat([df,A], axis=0)
        url = next_link(url)
        
    
    # write data to a csv
    df.to_csv('/Users/clairemason/Galvanize/Capstone/capstone/data.csv', index=False)

        