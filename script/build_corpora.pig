-- build_corpora.pig


--------------------------------------------------------------------------------
-------------------------- prepare structured raw data -------------------------
--------------------------------------------------------------------------------


gutindex = load '/tmp/eliot/data/gutindex_01' using JsonLoader('book_id:chararray, author:chararray, title:chararray');
gutpoetry = load '/tmp/eliot/data/raw/aparrish.json' using JsonLoader('line:chararray, book_id:chararray');
-- gutpoetry = sample gutpoetry 0.001;
-- this sample kept for debugging usage.
/*
    store gutindex into '/tmp/eliot/data/gutindex' using JsonStorage();
    store gutpoetry into '/tmp/eliot/data/gutpoetry' using JsonStorage();
    gutindex = load '/tmp/eliot/data/gutindex' using JsonLoader();
    gutpoetry = load '/tmp/eliot/data/gutpoetry' using JsonLoader();
*/
-- the above STORE operations are for debugging convinience.

-- gutindex: {book_id: chararray,author: chararray,title: chararray}
-- gutpoetry: {line: chararray,book_id: chararray}

-- poetry: {group: chararray,gutpoetry: {(line: chararray,book_id: chararray)}}
poetry = group gutpoetry by book_id;
-- poetry: {book_id: chararray,num_lines: long,lines: {(line: chararray)}}
poetry = foreach poetry generate group as book_id, COUNT(gutpoetry) as num_lines, gutpoetry.line as lines;
-- index: {book_id: chararray,author: chararray}
index = foreach gutindex generate book_id, author;


--------------------------------------------------------------------------------
------------------------------- building corpora -------------------------------
--------------------------------------------------------------------------------


-- corpus_00: {poetry::book_id: chararray,poetry::num_lines: long,poetry::lines: {(line: chararray)},index::book_id: chararray,index::author: chararray}
corpus_00 = join poetry by book_id, index by book_id using 'replicated';
-- corpus_01: {author: chararray,num_lines: long,lines: {(line: chararray)}}
corpus_01 = foreach corpus_00 generate index::author as author, poetry::num_lines as num_lines, poetry::lines as lines;
-- corpus_02: {group: chararray,corpus_01: {(author: chararray,num_lines: long,lines: {(line: chararray)})}}
corpus_02 = group corpus_01 by author;
-- corpus_03: {author: chararray,num_lines: long,lines: {(line: chararray)}}
corpus_03 = foreach corpus_02 generate group as author, SUM(corpus_01.num_lines) as num_lines, flatten(corpus_01.lines) as lines;
-- corpus_04: {author: chararray,num_lines: long,lines: {(line: chararray)}}
corpus_040 = filter corpus_03 by num_lines > (long)1000;
corpus_041 = filter corpus_040 by author != 'Various';
corpus_042 = filter corpus_041 by author != 'n/a';
corpus_04 = filter corpus_042 by author != 'Unknown';
-- TODO corpus_05 is for debugging usage, may remove in executing script.
-- corpus_05: {author: chararray,num_lines: long,lines: {(line: chararray)}}
corpus_05 = order corpus_04 by num_lines desc;
-- corpus_060: {author: chararray,line: chararray}
corpus_06 = foreach corpus_05 generate author, flatten(lines) as line;
/*
    store corpus_06 into '/tmp/eliot/data/corpus_06' using JsonStorage();
*/


--------------------------------------------------------------------------------
-------------------------- generate cleaned corpora ----------------------------
--------------------------------------------------------------------------------


register 'pig_udf.py' using streaming_python as step2;

-- cleaned lines for model training.
-- corpus_07c: {author: chararray,line: chararray}
corpus_07c = foreach corpus_06 generate author, step2.clean(line) as line;
-- group for selecting testing set with python
corpus_07c0 = group corpus_07c by author;
-- dump unecessary columns for optimization
corpus_07c1 = foreach corpus_07c0 generate group as author, corpus_07c.line as lines;
-- cleaned lines for model testing, 30% of training dataset.
-- corpus_08c: {author: chararray,line: chararray}
corpus_08c = foreach corpus_07c1 generate author, flatten(step2.select(lines, 0.3)) as line;
-- corpus_08c = foreach corpus_07c generate author, step2.select(lines, 0.3) as lines;

store corpus_07c into '/tmp/eliot/data/corpus_07c' using JsonStorage();
store corpus_08c into '/tmp/eliot/data/corpus_08c' using JsonStorage();
-- log00: Job failed, hadoop does not return any error message


--------------------------------------------------------------------------------
-------------------------- generate stemmed corpora ----------------------------
--------------------------------------------------------------------------------


-- stemmed lines for model training.
-- corpus_07s: {author: chararray,line: chararray)}}
corpus_07s = foreach corpus_07c generate author, step2.stem(line) as line;
-- group for selecting testing set with python
corpus_07s0 = group corpus_07s by author;
-- dump unecessary columns for optimization
corpus_07s1 = foreach corpus_07s0 generate group as author, corpus_07s.line as lines;
-- stemmed lines for model testing, 30% of training dataset.
-- corpus_08s: {author: chararray,line: chararray}
corpus_08s = foreach corpus_07s1 generate author, flatten(step2.select(lines, 0.3)) as line;
-- corpus_08s = foreach corpus_07s generate author, step2.select(lines, 0.3) as lines;


store corpus_07s into '/tmp/eliot/data/corpus_07s' using JsonStorage();
store corpus_08s into '/tmp/eliot/data/corpus_08s' using JsonStorage();
-- log00: main.sh  56.29s user 3.56s system 6% cpu 15:18.92 total


--------------------------------------------------------------------------------
-------------------------------- some reminers ---------------------------------
--------------------------------------------------------------------------------

/*
note that although `cleaned` and `stemmed` follow the same practice, they do
get different testing dataset. because the `select()` function uses Python's
random.sample() function.
*/

-- log00: Job failed, hadoop does not return any error message
-- log01: main.sh  61.13s user 4.28s system 5% cpu 19:09.68 total
