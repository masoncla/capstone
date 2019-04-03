import pandas as pd 
import numpy as np 

def get_corr_df(bodies, instructions):
    '''
    takes dataframes containing sentences and vectors for both body and instructions
    and returns a dataframe with just the body sentences, vectors, and instruction similarity
    '''
    final = pd.DataFrame(columns=['sentence', 'correlation'])
    for i in bodies['post'].unique():
        # grab an array of the vector representations for body and instructions
        body = bodies[bodies['post']==i].iloc[:,2:].values
        instruct = instructions[instructions['post']==i].iloc[:,2:].values
        
        # create correlations matrix
        corr = np.inner(body, instruct)
        max_corr = np.array([(i, row.max()) for i, row in enumerate(corr)])
        
        # put into df
        rel_df = pd.DataFrame(max_corr[:,1], columns=['correlation'])
        sents_df = pd.DataFrame(bodies.sentence[bodies.post==i].values, columns=['sentence'])
        array_df = pd.DataFrame(body)
        labelled = pd.concat([sents_df, rel_df, array_df], axis=1, sort=False)
        final = pd.concat([final, labelled], axis=0, ignore_index=True)
        
    return final

