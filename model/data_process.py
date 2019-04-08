import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from nltk import sent_tokenize
import tensorflow as tf
import tensorflow_hub as hub
from sys import argv

# takes raw scraped data and transforms it into individual sentences with corresponding post numbers
class Preprocess():
    def __init__(self):
        self.body_vecs = None
        self.inst_vecs = None
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
        body_sents_series = pd.Series([self.split_sentences_(df.body.iloc[i].decode('utf-8')) for i in range(len(df))])
        body_sents_df = pd.DataFrame(body_sents_series, columns=['body_sents'])
        inst_sents_series = pd.Series([self.split_sentences_(df.instructions.iloc[i].decode('utf-8')) for i in range(len(df))])
        inst_sents_df = pd.DataFrame(inst_sents_series, columns = ['inst_sents'])
        data = pd.concat([df, body_sents_df, inst_sents_df], axis=1)
        return data

    def split_into_dfs_(self, data):
        D = self.sent_engineer_(data)
        D.dropna(inplace=True)
        self.body = pd.DataFrame(columns=['sentence', 'post'])
        self.instruct = pd.DataFrame(columns=['sentence', 'post'])

        for i in range(len(D)):
            sent_df = pd.DataFrame([sent.encode('utf-8') for sent in D.body_sents.iloc[i]], columns=['sentence'])
            sent_df['post'] = i
            inst_df = pd.DataFrame([sent.encode('utf-8') for sent in D.inst_sents.iloc[i]], columns=['sentence'])
            inst_df['post'] = i
            self.body = pd.concat([self.body, sent_df], ignore_index=True)
            self.instruct = pd.concat([self.instruct, inst_df], ignore_index=True)

        


    def vectorize_(self, data):
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

        array_df = pd.DataFrame(embed_body)
        final = pd.concat([data, array_df], axis=1)
        return final

    def fit(self, raw_data):
        self.split_into_dfs_(raw_data)
        self.body_vecs = self.vectorize_(self.body)
        self.inst_vecs = self.vectorize_(self.instruct)
        return self.body_vecs, self.inst_vecs

# engineer labels for vectorized sentences
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
            self.nearby_sim_(labelled)
            final = pd.concat([final, labelled], axis=0, ignore_index=True, sort=True)

            
        return final


    def label(self):
        self.result = self.transform_()
        # define labels
        self.result['relevance']=0
        self.result['relevance'][(self.result['correlation']>=0.75) & (self.result['correlation']<1.0)]=1
        return self.result



if __name__=='__main__':
    input_file_path = argv[1]
    export_file_path = argv[2]

    raw_data = pd.read_csv(input_file_path)

    clean_and_vectorize = Preprocess()
    body_vecs, instruction_vecs = clean_and_vectorize.fit(raw_data)

    labels = Labeler(body_vecs, instruction_vecs)
    final = labels.label()

    final.to_csv(export_file_path, index=False)
    