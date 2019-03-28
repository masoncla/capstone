import pandas as pd 
import numpy as np 
from scrape_mb import make_soup
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
    new = [line for line in new.split('\n') if line and ' ' in line] 
    # create one long list of sentence strings       
    sents += new
    return sents









if __name__ == '__main__':
    df = pd.read_csv(argv[1])
    # break body of each post into sentences and store in a series
    sents_series = pd.Series([split_sentences(df.body.iloc[i]) for i in range(len(df))])