#!/usr/bin/env python

# noinspection PyUnresolvedReferences
from pig_util import outputSchema
import re


# noinspection SpellCheckingInspection
class PorterStemmer:

    def __init__(self):
        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0  # j is a general offset into the string

    def cons(self, i):
        # cons(i) is TRUE <=> b[i] is a consonant.
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return not self.cons(i - 1)
        return 1

    def m(self):
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        # vowelinstem() is TRUE <=> k0,...j contains a vowel
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        # doublec(j) is TRUE <=> j,(j-1) contain a double consonant.
        if j < (self.k0 + 1):
            return 0
        if self.b[j] != self.b[j - 1]:
            return 0
        return self.cons(j)

    def cvc(self, i):
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i - 1) or not self.cons(i - 2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        # ends(s) is TRUE <=> k0,...k ends with the string s.
        length = len(s)
        if s[length - 1] != self.b[self.k]:  # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k - length + 1:self.k + 1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
        # setto(s) sets (j+1),...k to the characters in the string s, readjusting k.
        length = len(s)
        self.b = self.b[:self.j + 1] + s + self.b[self.j + length + 1:]
        self.k = self.j + length

    def r(self, s):
        # r(s) is used further down.
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):
                self.setto("ate")
            elif self.ends("bl"):
                self.setto("ble")
            elif self.ends("iz"):
                self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif self.m() == 1 and self.cvc(self.k):
                self.setto("e")

    def step1c(self):
        # step1c() turns terminal y to i when there is another vowel in the stem.
        if self.ends("y") and self.vowelinstem():
            self.b = self.b[:self.k] + 'i' + self.b[self.k + 1:]

    def step2(self):
        """
        step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):
                self.r("ate")
            elif self.ends("tional"):
                self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):
                self.r("ence")
            elif self.ends("anci"):
                self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):
                self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):
                self.r("ble")
            elif self.ends("alli"):
                self.r("al")
            elif self.ends("entli"):
                self.r("ent")
            elif self.ends("eli"):
                self.r("e")
            elif self.ends("ousli"):
                self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):
                self.r("ize")
            elif self.ends("ation"):
                self.r("ate")
            elif self.ends("ator"):
                self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):
                self.r("al")
            elif self.ends("iveness"):
                self.r("ive")
            elif self.ends("fulness"):
                self.r("ful")
            elif self.ends("ousness"):
                self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):
                self.r("al")
            elif self.ends("iviti"):
                self.r("ive")
            elif self.ends("biliti"):
                self.r("ble")
        elif self.b[self.k - 1] == 'g':
            if self.ends("logi"):
                self.r("log")
        # To match the published algorithm, delete this phrase

    def step3(self):
        # step3() dels with -ic-, -full, -ness etc. similar strategy to step2.
        if self.b[self.k] == 'e':
            if self.ends("icate"):
                self.r("ic")
            elif self.ends("ative"):
                self.r("")
            elif self.ends("alize"):
                self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):
                self.r("ic")
            elif self.ends("ful"):
                self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        # step4() takes off -ant, -ence etc., in context <c>vcvc<v>.
        if self.b[self.k - 1] == 'a':
            if self.ends("al"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"):
                pass
            elif self.ends("ence"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"):
                pass
            elif self.ends("ible"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"):
                pass
            elif self.ends("ement"):
                pass
            elif self.ends("ment"):
                pass
            elif self.ends("ent"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'):
                pass
            elif self.ends("ou"):
                pass
            # takes care of -ous
            else:
                return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"):
                pass
            elif self.ends("iti"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"):
                pass
            else:
                return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"):
                pass
            else:
                return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """
        step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k - 1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k - 1

    def stem(self, p, i, j):
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k + 1]


# this will be used just for cleaning, same removal with the stemming one.

@outputSchema("line: chararray")
def clean(line):
    line = re.sub(r'(\W)|(_)|(\d)', ' ', line)
    # won't delete single character, they might be useful.
    # line = re.sub(r"\b\w\b", " ", line)
    line = re.sub(r'\s+', ' ', line)
    line = line.lower()
    return line


# stemming use the PorterStemmer(), and other than stem, it applies cleaning as well.

@outputSchema("line: chararray")
def stem(line):
    p = PorterStemmer()
    while True:
        output = ''
        word = ''
        # return _compile(pattern, 0).sub(repl, string, count)
        # line = re.sub(r'(\W)|(_)|(\d)', ' ', line)
        # line = re.sub(r'\s+', ' ', line)
        if line == '':
            break
        for c in line:
            if c.isalpha():
                # word += c.lower()
                word += c
            else:
                if word:
                    output += p.stem(word, 0, len(word) - 1)
                    word = ''
                # output += c.lower()
                output += c
        return output


'''
+ main reason of selecting testing datasets fromc Python UDF instead of Pig SAMPLE:

1. dataset selected for testing use should evenly distributed by author.
2. SAMPLE cannot be used with lines:bag: { (line: chararray) }, only aliases acceppted.

>  because of that, there definately have to have some redundant steps, either re-clean 
   and re-stem the testing datasets, or re-GROUP and re-FLATTEN the training datasets.
   haven't tried both, but I choose the latter procedure. to try to minimize extra cost,
   I split stemming from cleaning, and have stem function based on the result of clean.
'''


# returns `percentage` of lines by one author. since it generate testing dataset using `random.sample()` function,
# basically, you cannot get the same set in any two executions.
@outputSchema("lines: {(line:chararray)}")
def select(lines, percentage):
    import random
    return random.sample(lines, int(percentage * len(lines)))


# noinspection PyShadowingBuiltins
@outputSchema("log: {(date:chararray, time:chararray, classname:chararray, level:chararray, detail:chararray)}")
def create_structure(input):
    if input.startswith('java.lang.Exception'):
        input = input[21:len(input)] + ' - java.lang.Exception'
    date, time, classname, level, detail = input.split(' ', 4)
    return date, time, classname, level, detail
