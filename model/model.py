import pandas as pd 
import numpy as np 
from sklearn.linear_model import LogisticRegression
import yaml
import pickle
from label_engineer import get_corr_df

# get ya data
df_bodies = pd.read_csv('data/train.csv')
df_instructions = 

#create labels
df['relevance']=0
df['relevance'][df['correlation']>=0.75]=1



model = pickle.load(open('model.p', 'rb'))
