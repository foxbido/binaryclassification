#!/usr/bin/env python
# this program is designed only for bi-author classification
import time
import json
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer


# for use of parameter selecting
def tokenizer(text):
    return text.split()


# for use of parameter selecting
def token_porter(text):
    ps = PorterStemmer()
    return [ps.stem(word) for word in text.split()]


# returns combined DataFrame of given two authors extracted from corpus
def extract_author(author1, author2):
    import json
    data = []
    with open('../data/corpus_07c/part-r-00000', 'r') as f:
        for line in f:
            line = json.loads(line)
            if line["author"] == author1:
                line["author"] = 1
                data.append(line)
            elif line["author"] == author2:
                line["author"] = 0
                data.append(line)
    df = pd.DataFrame(data)
    return df


# LogisticRegression model of two authors and given ratio of splitting train-test datasets
def train(author1, author2, ratio):
    df = extract_author(author1, author2)
    np.random.seed(0)
    df = df.reindex(np.random.permutation(df.index))

    pos_of_split = int((len(author1) + len(author2)) * ratio)
    x_train = df.loc[:pos_of_split, 'line'].values
    y_train = df.loc[:pos_of_split, 'author'].values
    x_test = df.loc[pos_of_split:, 'line'].values
    y_test = df.loc[pos_of_split:, 'author'].values
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
    # `max_iter` is set to 5000, because number of regressions can increase to this many when number of training
    # lines are half 10k, Python will stop at some point.
    lr_tfidf = Pipeline([('vect', tfidf), ('clf', LogisticRegression(random_state=0, max_iter=5000))])
    # here the `n_jobs` parameter you may want to adjust it to be a proper one, -1 means using all cores
    # on your machine, which may jam your current issues.
    gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid, scoring='accuracy', cv=5, verbose=1, n_jobs=-1)
    gs_lr_tfidf.fit(x_train, y_train)

    """
    print(f'Best parameter set:\n{gs_lr_tfidf.best_params_}')
    print(f'CV Accuracy: {gs_lr_tfidf.best_score_}')
    print(f'Test Accuracy: {gs_lr_tfidf.best_estimator_.score(x_test, y_test)}')
    """

    # cv_accuracy = gs_lr_tfidf.best_score_
    test_accuracy = gs_lr_tfidf.best_estimator_.score(x_test, y_test)

    return test_accuracy
    # the cv_accuracy is only for use of optimizing model parameters
    # return [cv_accuracy, test_accuracy]


# set up a set of authors, and train them with given train-test splitting ratio.
# the default ratio is 0.7
# [Notice] this will generate the complete iteration of cross-product of the
# author set, when it contains more than 10 authors, total time consumed can
# increase tremendously, that's also why I split the ratio separately.
def train_set(ratio=0.7):
    author = ["Dante Alighieri",
              "John Milton",
              "William Butler Yeats",
              "Walt Whitman",
              "William Shakespeare",
              "Ezra Pound",
              "T. S. Eliot"]
    # result_dante_milton_7 = train(author[0], author[1], 0.7)
    # print(result_dante_milton_7)
    # result_pound_eliot_5 = train(author[5], author[6], 0.9)
    # print(result_pound_eliot_5)
    begin = time.time()
    result = dict()
    for i in range(len(author)):
        author1 = author[i]
        for author2 in author[i + 1:len(author) + 1]:
            print(f'\nRunning jobs on {author1}-{author2}...\n')
            result[f'{author1}-{author2}'] = train(author1, author2, ratio)
    duration = time.time() - begin
    result["duration"] = duration
    result["ratio"] = ratio
    return result


def main():
    # this is merely a test running of 3=7 ratio
    result = train_set(0.9)
    print(result)
    print(json.dumps(result, indent=4))
    """
    result = []
    # this is the complete version of all ratios mentioned in my final presentation
    ratios = [0.9, 0.7, 0.5, 0.3, 0.1]
    for ratio in ratios:
        result.append(train_set(ratio))
    with open('complete_result', 'w') as f:
        for line in result:
            f.writelines(line)
    """


if __name__ == '__main__':
    main()
