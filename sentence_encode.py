import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import pandas as pd
import requests
import time
from sys import argv, exit




def get_corr(embeded_inst, data):
    final = pd.DataFrame(columns=['sentence', 'correlation'])
    for i in embeded_inst.keys():
        corr = np.inner(embeded_inst[i][0], embeded_inst[i][1])
        max_corr = np.array([(i, row.max()) for i, row in enumerate(corr)])
        sent_df = pd.DataFrame([sent.encode('utf-8') for sent in data.body_sents.iloc[i]], columns=['sentence'])
        rel_df = pd.DataFrame(max_corr[:,1], columns=['correlation'])
        labelled = pd.concat([sent_df, rel_df], axis=1)
        final = pd.concat([final, labelled], ignore_index=True)
    return final





if __name__=='__main__':
    data = pd.read_csv(argv[1])
    sent_batch = data.sentence.values

    t2 = time.time()
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" 
    # Import the Universal Sentence Encoder's TF Hub module
    embed = hub.Module(module_url)
    

    

    # create GUSE placeholder
    sentences = tf.placeholder(dtype=tf.string, shape=[None])
    embedding = embed(sentences)

    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        embed_body = session.run(embedding, feed_dict={sentences: sent_batch})

    print('Total time: {}'.format(time.time()-t2))
    

    # put sentences and correlations into dataframe
    array_df = pd.DataFrame(embed_body)
    final = pd.concat([data, array_df], axis=1)
    final.to_csv(argv[2])