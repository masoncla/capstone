import pandas as pd 
import numpy as np 
from sklearn.linear_model import LogisticRegression
import yaml
import pickle
from label_engineer import get_corr_df

# Create Training Data
# import data
df_bodies = pd.read_csv(train_body_file)
df_instructions = pd.read_csv(train_instruction_file)

# create correlation column for body sentences
data = get_corr_df(df_bodies, df_instructions)

#create labels
data['relevance']=0
data['relevance'][data['correlation']>=0.75]=1


with open('model_param.yaml', 'r') as f:
    params = yaml.load(f)

model = LogisticRegression(**params)

