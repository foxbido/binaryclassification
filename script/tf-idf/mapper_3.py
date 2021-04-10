#!/usr/bin/env python
# <word, <author, word_count, number_of_words_in_document, 1>>
import sys

for line in sys.stdin:
    line = line.rstrip()
    (key, value) = line.split('\t', 1)
    (word, doc_name) = key.split(':', 1)
    (word_count, num_words_in_doc) = value.split(':', 1)
    print(f'{word}\t{doc_name}:{word_count}:{num_words_in_doc}:{1}')
