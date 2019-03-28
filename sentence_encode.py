import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import pandas as pd
import requests
import re
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
    body_sents_series = pd.Series([split_sentences(df.body.iloc[i]) for i in range(len(df))])
    body_sents_df = pd.DataFrame(body_sents_series, columns=['body_sents'])
    inst_sents_series = pd.Series([split_sentences(df.instructions.iloc[i]) for i in range(len(df))])
    inst_sents_df = pd.DataFrame(inst_sents_series, columns = ['inst_sents'])
    data = pd.concat([df, body_sents_df, inst_sents_df], axis=1)
    return data



module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" 
# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)

# Reduce logging output
tf.logging.set_verbosity(tf.logging.ERROR)

embeded_inst = defaultdict()

with tf.Session() as session:
  session.run([tf.global_variables_initializer(), tf.tables_initializer()])
  for i in range(80):
    if i%5 == 0:
      print(i)
    #embed_body = session.run(embed(data.body_sents.iloc[i]))
    embed2 = session.run(embed(data.inst_sents.iloc[i]))
    embeded_inst[i] = embed2