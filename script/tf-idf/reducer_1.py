#!/usr/bin/env python
# <<word, author>, n>
import sys

count = 0
current_word = None
current_author = None

for line in sys.stdin:
    (key, val) = line.split('\t', 1)
    (word, author) = key.split(':', 1)

    if current_word != word or current_author != author:
        if current_word and current_author:
            print('{}:{}\t{}'.format(current_word, current_author, count))
            count = 0
        current_word = word
        current_author = author
    try:
        count += int(val)
    except ValueError:
        continue
print('{}:{}\t{}'.format(word, author, count))
