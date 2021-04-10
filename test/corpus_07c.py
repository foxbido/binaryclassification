# other libraries
import numpy as np
import pandas as pd
import json

# sklearn
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer

# translate corpus_07c from json into DataFrame
# pbar = pyprind.ProgBar(2471573)
data = []
with open('../data/corpus_08c/part-r-00000', 'r') as f:
    for line in f:
        line = json.loads(line)
        data.append(line)

df = pd.DataFrame(data)

# shuffle index and store corpus as csv for testing usage
np.random.seed(0)
df = df.reindex(np.random.permutation(df.index))
df.to_csv('./corpus_07c.csv', index=False)
df = pd.read_csv('corpus_07c.csv')
df.head(3)

# all * 0.3 == test : 2471573 * 0.3 == 1730101
x_train = df.loc[:1730101, 'line'].values
y_train = df.loc[:1730101, 'author'].values
x_test = df.loc[1730101:, 'line'].values
y_test = df.loc[1730101:, 'author'].values

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