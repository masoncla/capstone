import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

class Preprocess():
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.body = None
        self.instruct = None
    
    def split_sentences_(self, body):
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

    def sent_engineer_(self, df):
        df.dropna(inplace=True)
        body_sents_series = pd.Series([self.split_sentences_(df.body.iloc[i]) for i in range(len(df))])
        body_sents_df = pd.DataFrame(body_sents_series, columns=['body_sents'])
        inst_sents_series = pd.Series([self.split_sentences_(df.instructions.iloc[i]) for i in range(len(df))])
        inst_sents_df = pd.DataFrame(inst_sents_series, columns = ['inst_sents'])
        data = pd.concat([df, body_sents_df, inst_sents_df], axis=1)
        return data

    def split_into_dfs(self):
        D = self.sent_engineer_(self.raw_data)
        D.dropna(inplace=True)
        self.body = pd.DataFrame(columns=['sentence', 'post'])
        self.instruct = pd.DataFrame(columns=['sentence', 'post'])

        for i in range(len(D)):
            sent_df = pd.DataFrame([sent for sent in D.body_sents.iloc[i]], columns=['sentence'])
            sent_df['post'] = i
            inst_df = pd.DataFrame([sent for sent in D.inst_sents.iloc[i]], columns=['sentence'])
            inst_df['post'] = i
            self.body = pd.concat([self.body, sent_df], ignore_index=True)
            self.instruct = pd.concat([self.instruct, inst_df], ignore_index=True)

        return self.body, self.instruct



class Labeler():
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
            corr = cosine_similarity(body, instruct)
            max_corr = np.array([(i, row.max()) for i, row in enumerate(corr)])
            
            # put into df
            rel_df = pd.DataFrame(max_corr[:,1], columns=['correlation'])
            sents_df = pd.DataFrame(self.bodies.sentence[self.bodies.post==i].values, columns=['sentence'])
            array_df = pd.DataFrame(body)
            labelled = pd.concat([sents_df, rel_df, array_df], axis=1, sort=False)
            final = pd.concat([final, labelled], axis=0, ignore_index=True)
            
        return final
    
    def label(self):
        self.result = self.transform_()
        self.result['relevance']=0
        self.result['relevance'][self.result['correlation']>=0.75]=1
        return self.result

class Model():
    def __init__(self, data, model=LogisticRegression()):
        self.data = data
        self.model = model

