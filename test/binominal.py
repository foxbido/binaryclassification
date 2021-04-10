# /usr/bin/env python
# other libraries
import numpy as np
import pandas as pd
import json

# sklearn
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer

"""
labels = {"dante": 1, "milton": 0}
with open('dante_milton', 'r') as f:
    import re

    with open('dante_milton.csv', 'w') as labeled:
        for line in f:
            line = re.sub(r'^dante\t', '1\t', line)
            line = re.sub(r'^milton\t', '0\t', line)
            line = re.sub(r' d ', 'ed ', line)
            labeled.writelines(line)
        # author = labels[(line.split('\t')[0])]
        # tranformed = f'{author}\t{line}'

df = pd.read_csv('dante_milton.csv', '\t')
"""

# df = pd.read_csv('milton_yeats', '\t')
# df = pd.read_csv('whitman_shakespeare', '\t')
df =pd.read_csv('eliot_pound', '\t')
df.columns = ["author", "line"]

# shuffle index and store corpus as csv for testing usage
np.random.seed(0)
df = df.reindex(np.random.permutation(df.index))
df.to_csv('./ep.csv', index=False)
df = pd.read_csv('./ep.csv')
df.head(3)
# dm
# 146727 * 0.3 = 44018
# 109443
# 37284
# my
# 51381 * 0.3 = 15414 : 35966
# 37284
# 14097
# ws
# 17219 * 0.3 = 5166 : 12054
# 9334
# 7885
# ep
# 3564 * 0.3 = 1069 : 2495
# 1710
# 1854
x_train = df.loc[:2495, 'line'].values
y_train = df.loc[:2495, 'author'].values
x_test = df.loc[2495:, 'line'].values
y_test = df.loc[2495:, 'author'].values

tfidf = TfidfVectorizer(strip_accents=None, lowercase=False, preprocessor=None)
param_grid = [{'vect__ngram_range': [(1, 1)],
               'clf__penalty': ['l2'],
               'clf__C': [1.0, 10.0, 100.0]},
              {'vect__ngram_range': [(1, 1)],
               'vect__use_idf': [False],
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

"""
my:
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1), 'vect__norm': None, 'vect__use_idf': False}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.91076840552501
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.916572077185017

dm:
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 100.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1), 'vect__norm': None, 'vect__use_idf': False}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.9303872508374968
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.9610022965639308

ws: 7=3
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1)}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.8956449605972626
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.8921378776142526

ws: 3=7
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1)}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.8534942637638772
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.8641719216727514

ws: 9=1
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1)}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.9005031800060372
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.9012202208018594

ws: 1=9
>>> print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
Best parameter set:
{'clf__C': 100.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1)}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.7974300640377486
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.8178884873515746

ep: 3=7
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1)}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.7682242990654207
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.7822774659182037

ep: 7=3
Best parameter set:
{'clf__C': 10.0, 'clf__penalty': 'l2', 'vect__ngram_range': (1, 1)}
>>> print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
CV Accuracy: 0.8229130260521043
>>> print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
Test Accuracy: 0.849250936329588
"""