# /usr/bin/env python
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer


def tokenizer(text):
    return text.split()


def token_porter(text):
    ps = PorterStemmer()
    return [ps.stem(word) for word in text.split()]


df = pd.read_csv('milton_yeats_whitman', '\t')
df.columns = ["author", "line"]

# shuffle index and store corpus as csv for testing usage
np.random.seed(0)
df = df.reindex(np.random.permutation(df.index))
df.to_csv('./myw.csv', index=False)
df = pd.read_csv('./myw.csv')
df.head(3)

# 60715 * 0.7 = 42500 : 18214
# 37284
# 14097
# 9334
x_train = df.loc[:42500, 'line'].values
y_train = df.loc[:42500, 'author'].values
x_test = df.loc[42500:, 'line'].values
y_test = df.loc[42500:, 'author'].values

tfidf = TfidfVectorizer(strip_accents=None, lowercase=False, preprocessor=None)
param_grid = [{'vect__ngram_range': [(1, 1)],
               'vect__tokenizer': [tokenizer, token_porter],
               'clf__penalty': ['l2'],
               'clf__C': [1.0, 10.0, 100.0]},
              {'vect__ngram_range': [(1, 1)],
               'vect__tokenizer': [tokenizer, token_porter],
               'vect__use_idf': [True],
               'vect__norm': [None],
               'clf__penalty': ['l2'],
               'clf__C': [1.0, 10.0, 100.0]}]
lr_tfidf = Pipeline([('vect', tfidf), ('clf', LogisticRegression(random_state=0, max_iter=400))])
gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid, scoring='accuracy', cv=5, verbose=1, n_jobs=7)
gs_lr_tfidf.fit(x_train, y_train)

# check the result
print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')

'''
7=3
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1)}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.7283663326653307
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.7142857142857143

9=1
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1), 'vect__norm': None, 'vect__use_idf': False}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.8601675921129152
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.8711909075934772

5=5
>>> # check the result
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1)}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.8260099255863151
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.8334815693250321
'''

"""
fully equipped parameter grid
7=3
[Parallel(n_jobs=7)]: Done  60 out of  60 | elapsed:  3.1min finished
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1), 'vect__norm': None, 'vect__tokenizer': <function token_porter at 0x7fd323727790>, 'vect__use_idf': False}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.8480271026938008
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.8541781047545843

7=3 : tfidf=True
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1), 'vect__tokenizer': <function tokenizer at 0x7fd323727820>}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.8470857989025513
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.8555506753047106
"""
