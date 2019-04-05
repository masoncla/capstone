import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
from sys import argv, exit



if __name__=='__main__':
    input_file = argv[1]
    export_file = argv[2]


    data = pd.read_csv(input_file)
    sent_batch = data.sentence.values

    module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" 
    # Import the Universal Sentence Encoder's TF Hub module
    embed = hub.Module(module_url)
    
    # create GUSE placeholder
    sentences = tf.placeholder(dtype=tf.string, shape=[None])
    embedding = embed(sentences)

    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        embed_body = session.run(embedding, feed_dict={sentences: sent_batch})

    

    # put sentences and correlations into dataframe
    array_df = pd.DataFrame(embed_body)
    final = pd.concat([data, array_df], axis=1)
    final.to_csv(export_file, index=False)