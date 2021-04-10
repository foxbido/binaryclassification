#!/usr/bin/env python
# <author, <word, count>>
import sys

for line in sys.stdin:
    line = line.strip('\n')
    (key, word_count) = line.split('\t', 1)
    (word, author) = key.split(':', 1)
    print(f'{author}\t{word}:{word_count}')
