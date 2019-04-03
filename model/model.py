import pandas as pd 
import numpy as np 
from sklearn.linear_model import LogisticRegression
import yaml

# get ya data
df = pd.read_csv('data/train.csv')

#create labels
df['relevance']=0
df['relevance'][df['correlation']>=0.75]=1




with open('/Users/clairemason/Galvanize/Capstone/capstone/model_param.yaml', 'r') as params:
    params = yaml.load(params)

model = LogisticRegression(**params)
model.fit()
