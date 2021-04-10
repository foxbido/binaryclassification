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
# extremely time-consuming ~40min
df = pd.DataFrame()
data = []
with open('../data/corpus_08c/part-r-00000', 'r') as f:
    for line in f:
        line = json.loads(line)
        data.append(line)


df = df.append({"line": line["line"], "author": line["author"]}, ignore_index=True)
df.columns = ["line", "author"]
