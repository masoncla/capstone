import pandas as pd 
import numpy as np 

from nltk import sent_tokenize
from sys import argv, exit

def split_sentences(body):
    # tokenize into sentences
    sents = sent_tokenize(body)
    # break apart the sentences on the new lines \n
    new = ''
    for i, sent in enumerate(sents):
        if '\n' in sent:
            new += sents.pop(i)
    new = [line for line in new.split('\n') if line and len(line)>1] 
    # create one long list of sentence strings       
    sents += new
    return sents

def get_recipe_instructions(url)
    '''
    returns the a list of the instruction sentence strings from the recipe post at the inputted url
    '''
    soup = make_soup(url)
    # get recipe instruction conatiners
    recipe = soup.find_all('div', class_="wprm-recipe-instruction-text")
    # isolate just the text
    instructions = [instruct.text for instruct in recipe]
    # break into sentences
    ins_str = []
    for instruct in instructions:
        for sent in sent_tokenize(instruct):
            ins_str.append(sent)

    return ins_str







if __name__ == '__main__':
    df = pd.read_csv(argv[1])
    # break body of each post into sentences and store in a series
    sents_series = pd.Series([split_sentences(df.body.iloc[i]) for i in range(len(df))])