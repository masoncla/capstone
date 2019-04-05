import pandas as pd
import numpy as np 
from nltk import sent_tokenize
from sys import argv




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

def sent_engineer(df):
    df.dropna(inplace=True)
    body_sents_series = pd.Series([split_sentences(df.body.iloc[i]) for i in range(len(df))])
    body_sents_df = pd.DataFrame(body_sents_series, columns=['body_sents'])
    inst_sents_series = pd.Series([split_sentences(df.instructions.iloc[i]) for i in range(len(df))])
    inst_sents_df = pd.DataFrame(inst_sents_series, columns = ['inst_sents'])
    data = pd.concat([df, body_sents_df, inst_sents_df], axis=1)
    return data

def split_into_dfs(D):
    D.dropna(inplace=True)
    body = pd.DataFrame(columns=['sentence', 'post'])
    instruct = pd.DataFrame(columns=['sentence', 'post'])
    
    for i in range(len(D)):
        sent_df = pd.DataFrame([sent for sent in D.body_sents.iloc[i]], columns=['sentence'])
        sent_df['post'] = i
        inst_df = pd.DataFrame([sent for sent in D.inst_sents.iloc[i]], columns=['sentence'])
        inst_df['post'] = i
        body = pd.concat([body, sent_df], ignore_index=True)
        instruct = pd.concat([instruct, inst_df], ignore_index=True)
        
    return body, instruct

if __name__=='__main__':
    input_file = argv[1]
    body_file = argv[2]
    instruct_file = argv[3]

    input_df = pd.read_csv(input_file)
    data = sent_engineer(input_df)

    body, instruct = split_into_dfs(data)

    body.to_csv(body_file, index=False)
    instruct.to_csv(instruct_file, index=False)

