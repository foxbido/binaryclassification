from nltk.stem.porter import PorterStemmer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
import pyprind
import numpy as np
import pandas as pd
import os


def tokenizer(text):
    return text.split()


def tokenizer_porter(text):
    porter = PorterStemmer()
    return [porter.stem(word) for word in text.split()]


pbar = pyprind.ProgBar(50000)
labels = {'pos': 1, 'neg': 0}
df = pd.DataFrame()
for s in ('test', 'train'):
    for l in ('pos', 'neg'):
        path = f'../data/aclImdb/{s}/{l}'
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r') as infile:
                txt = infile.read()
                df = df.append([[txt, labels[l]]], ignore_index=True)
                pbar.update()
df.columns = ['review', 'sentiment']

# shuffle index and store corpus as csv for testing usage
np.random.seed(0)
df = df.reindex(np.random.permutation(df.index))
df.to_csv('./aclidb.csv', index=False)
df = pd.read_csv('./aclidb.csv')
df.head(3)

# selecting testing and training datasets
x_train = df.loc[:25000, 'review'].values
y_train = df.loc[:25000, 'sentiment'].values
x_test = df.loc[25000:, 'review'].values
y_test = df.loc[25000:, 'sentiment'].values

# initialize the model parameters
tfidf = TfidfVectorizer(strip_accents=None, lowercase=False, preprocessor=None)
param_grid = [{'vect__ngram_range': [(1, 1)],
               'vect__tokenizer': [tokenizer, tokenizer_porter],
               'clf__penalty': ['l2'],
               'clf__C': [1.0, 10.0, 100.0]},
              {'vect__ngram_range': [(1, 1)],
               'vect__use_idf': [False],
               'vect__norm': [None],
               'clf__penalty': ['l2'],
               'clf__C': [1.0, 10.0, 100.0]}]

lr_tfidf = Pipeline([('vect', tfidf), ('clf', LogisticRegression(random_state=0, max_iter=400))])
gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid, scoring='accuracy', cv=5, verbose=1, n_jobs=-1)
gs_lr_tfidf.fit(x_train, y_train)

# check the result
print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
