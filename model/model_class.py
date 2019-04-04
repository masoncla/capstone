import pandas as pd
import numpy as np

class Preprocess():
    def __init__(self, body_vectors, instruction_vectors):

        self.bodies = body_vectors
        self.instructions = instruction_vectors
        self.result=None

    def transform_(self):
        '''
        takes dataframes containing sentences and vectors for both body and instructions
        and returns a dataframe with just the body sentences, vectors, and instruction similarity
        '''
        final = pd.DataFrame(columns=['sentence', 'correlation'])
        for i in self.bodies['post'].unique():
            # grab an array of the vector representations for body and instructions
            body = self.bodies[self.bodies['post']==i].iloc[:,2:].values
            instruct = self.instructions[self.instructions['post']==i].iloc[:,2:].values
            
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
    
    def label():
        self.result = self.transform_()
        self.result['relevance']=0
        self.result['relevance'][self.result['correlation']>=0.75]=1
        return self.result

class Model():
    def __init__(self, )