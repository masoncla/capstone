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

