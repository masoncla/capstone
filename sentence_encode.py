import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import pandas as pd
import requests

from collections import defaultdict
from nltk import sent_tokenize


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
    body_sents_series = pd.Series([split_sentences(df.body.iloc[i].decode('utf-8')) for i in range(len(df))])
    body_sents_df = pd.DataFrame(body_sents_series, columns=['body_sents'])
    inst_sents_series = pd.Series([split_sentences(df.instructions.iloc[i].decode('utf-8')) for i in range(len(df))])
    inst_sents_df = pd.DataFrame(inst_sents_series, columns = ['inst_sents'])
    data = pd.concat([df, body_sents_df, inst_sents_df], axis=1)
    return data

def get_corr(embeded_inst):
    final = pd.DataFrame(columns=['sentence', 'correlation'])
    for i in embeded_inst.keys():
        corr = np.inner(embeded_inst[i][0], embeded_inst[i][1])
        max_corr = np.array([(i, row.max()) for i, row in enumerate(corr)])
        sent_df = pd.DataFrame([sent.encode('utf-8') for sent in data.body_sents.iloc[i]], columns=['sentence'])
        #array_df = pd.DataFrame([row for row in embeded_inst[i][0]])
        rel_df = pd.DataFrame(max_corr[:,1], columns=['correlation'])
        labelled = pd.concat([sent_df, array_df, rel_df], axis=1)
        final = pd.concat([final, labelled], ignore_index=True)
    return final




if __name__=='__main__':
    data = pd.read_csv('minimal_bake.csv')
    data = sent_engineer(data)


    module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" 
    # Import the Universal Sentence Encoder's TF Hub module
    embed = hub.Module(module_url)

    # Reduce logging output
    tf.logging.set_verbosity(tf.logging.ERROR)

    embeded = defaultdict()

    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        for i in range(10):
            embed_body = session.run(embed(data.body_sents.iloc[i]))
            embed_inst = session.run(embed(data.inst_sents.iloc[i]))
            embeded[i] = (embed_body, embed_inst)

    final = get_corr(embeded)
    final.to_csv('vec_data.csv')