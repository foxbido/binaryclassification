#!/usr/bin/env python
# <<word, author>, <count, count_author>>

import sys

author_word_count_0 = 0
current_author = None
author_words = {}
author_word_count_1 = {}
val = []

for line in sys.stdin:
    line = line.rstrip()
    (author, val) = line.split('\t', 1)
    (word, word_count) = val.split(':', 1)

    if current_author != author:
        if current_author:
            author_word_count_1[current_author] = author_word_count_0
            author_word_count_0 = 0
        current_author = author
    try:
        author_word_count_0 += int(word_count)
        if author in author_words.keys():
            tmp_list = author_words[author]
            tmp_list.append(word + "\t" + word_count)
            author_words[author] = tmp_list
        else:
            tmp_list = [word + "\t" + word_count]
            author_words[author] = tmp_list
    except ValueError:
        continue
author_word_count_1[current_author] = author_word_count_0

# Generating key-value pairs
for key in author_words.keys():
    contents = author_words[key]
    for item in contents:
        item = item.rstrip()
        (word, word_count) = item.split("\t", 1)
        print(f'{word}:{key}\t{word_count}:{str(author_word_count_1[key])}')
