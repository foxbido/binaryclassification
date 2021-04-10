#!/usr/bin/env python

"""
input:  author, line
output: ((word, author), 1)
"""

import sys
import json

for line in sys.stdin:
    verse = json.loads(line)
    words = verse["line"].strip().split()
    for word in words:
        print(f'{word}:{verse["author"]}\t{1}')
"""
for line in sys.stdin:
    author, verse = line.split('\t')
    words = verse.strip().split()
    for word in words:
        print(f'{word}:{author}\t{1}')
"""
