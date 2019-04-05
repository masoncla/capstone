import pandas as pd 
import numpy as np 
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from sys import argv
import pickle


def summarize_useful(df):
    '''
    INPUT: df of sentence strings and sentence vectors
    OUTPUT: paragraph of sentences
    '''
    arr = df.drop(['sentence'], axis=1)
    sentences = list(df.sentence.values)
    
    # Determine length of summary
    if len(df) <= 5:
        n_sents = len(df)
    else:
        n_sents = int(np.ceil(np.sqrt(len(df))))
    
    
    # Create a similarity martix with the sentence vectors
    similarity_mat = cosine_similarity(arr, arr)
    ranks = nx.pagerank(nx.from_numpy_array(similarity_mat))
    
    # Sort by rank and pick top sentences
    ranked = sorted(((ranks[i], s) for i,s in enumerate(sentences)), reverse=True)
    
    summarize = []
    for i in range(n_sents):
        summarize.append(ranked[i][1])
        
    # Return Summary    
    summary = ''.join(summarize)
    
    return summary
    
def get_relevant(df, model):
    # get predicted relevance for input dataframe
    pred_labels = model.predict(df.drop(['sentence'], axis=1))
    return df[pred_labels==1]

if __name__=='__main__':
    input_file = argv[1]
    model_file = argv[2]

    text_to_sum_relevance = pd.read_csv(input_file)
    model = pickle.load(open(model_file, 'rb') )
    
    rele_data = get_relevant(text_to_sum_relevance, model)
    summary = summarize_useful(rele_data)
    print(summary)