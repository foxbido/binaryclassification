#!usr/bin/env python

import json


def author_list():
    authors = dict()
    with open('../data/corpus_07c/part-r-00000', 'r') as f:
        for line in f:
            line = json.loads(line)
            author = line["author"]
            if exit(authors[author]):
                authors[author] += 1
            else:
                authors[author] = 1
    print(authors)
    return authors


author_list()
