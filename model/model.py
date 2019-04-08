import pandas as pd 
import numpy as np 
from sklearn.linear_model import LogisticRegression
import yaml
import pickle


# import training data
df_train = pd.read_csv('train_data_filepath')
# split into features and target
X_train = df_train.drop(['sentence', 'correlation', 'relevance'], axis=1).values
y_train = df_train.relevance.values

# get model parameters
with open('model_param.yaml', 'r') as f:
    params = yaml.load(f)

model = LogisticRegression(**params)
model.fit(X_train, y_train)

pickle.dump(model, open('path_to_pickle_file', 'wb'))



