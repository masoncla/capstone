import pandas as pd 
import numpy as np 
from sklearn.linear_model import LogisticRegressionCV
import yaml
import pickle
from sys import argv

if __name__=='__main__':
    # import training data
    df_train = pd.read_csv(argv[1])
    df_train.dropna(inplace=True)
    # split into features and target
    X_train = df_train.drop(['sentence', 'correlation', 'relevance'], axis=1).values
    y_train = df_train.relevance.values

    # get model parameters
    with open('model_param.yaml', 'r') as f:
        params = yaml.load(f)

    # Initialize and train model
    model = LogisticRegressionCV(**params)
    model.fit(X_train, y_train)

    # Save trained model
    pickle.dump(model, open('path_to_pickle_file', 'wb'))



