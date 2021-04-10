#!/usr/bin/env python

# noinspection PyPep8Naming
# import os
from time import time
import re
import json


class tests:
    def test3(self):
        p_s_book_id = re.compile(r'[A-Z].*\s+[0-9]+\n$')
        with open('data/reuse/index.all', 'r') as f:
            for line in f:
                if p_s_book_id.match(line) and len(line) != 79:
                    print(line)

    def test2(self):
        filename = 'data/reuse/index.all'
        index_all = file_to_list(filename)
        # print_list(index_all)
        # print_list(combine_separated_lines(index_all))
        index_all = combine_separated_lines(index_all)
        # book_id_list = []
        # author_list = []
        # title_list = []
        # for record in index_all:
        # book_id_list.append(get_book_id(record))
        # author_list.append(get_author(record))
        # title_list.append(get_title(record, author_list[-1]))
        # print(len(book_id_list))
        # print(len(author_list))
        # print(len(title_list))
        # print_list(book_id_list)
        for record in index_all:
            # record = re.sub('\n', '', record)
            author = get_author(record)
            title = get_title(record, author)
            if author == 'n/a':
                # print('n/a', end='\t\t\t\t')
                # print(record, end='')
                continue
            # print(get_book_id(record), end='\n')
            else:
                # record = re.sub('\n', '', record)
                print(record, end='')
                print(f'{title}, by {author}')

    def test1(self):
        f_index = open('data/reuse/index.all', 'r')
        list_index = f_index.readlines()
        for item in list_index:
            print(str(len(item)) + '\t---- ' + str(item))
        print(len(list_index))
        print(list_index)
        f_index.close()


# Prints all elements in a list, separated with the given string.
def print_list(list_name, separator='\n'):
    # >>>1<<<
    # print('[%s]' % separator.join(map(str, list_name)))
    # >>>2<<<
    # for item in list_name:
    #     print(item)
    print(*list_name, sep=separator, end='')


# DONE
def is_book_id_line(line):
    # This pattern is very finely tuned.
    p_book_id = re.compile(r'.*\s?[^,]\s+[0-9]+\n')
    # not really useful actually, just as a memo, may be used in simpler situations.
    # return line.split()[-1].isdigit()
    return p_book_id.match(line)


# DONE
# assume that `line` contains book id
def get_book_id(line):
    return re.sub(r'\n', '', line.split()[-1])


# DONE
# this fun extract everything between r',? by ' and r'\s\s+[0-9]+'
def get_author(line):
    """
    return re.sub(r'(.*,? by )|(\s\s+[0-9]+)', '', line)
    1. the property `author` is not available in some of the records, assign 'n/a'.
    Remove in title note.
    """
    p_author = re.compile(r'.*,? [bB]y [A-Za-z].*[0-9]+\n')
    if not p_author.match(line):
        return 'n/a'
    p_note = re.compile(r'\(Note:[^)].*\)')
    line = re.sub(p_note, '', line)
    author = re.sub(r'.*,? [bB]y ', '', line)
    author = re.sub(r'\s?\s+[0-9]+\n', '', author)
    if len(author) < 3:
        author = r'n/a'
    # NOTE: if author is not available and title contains the by-pattern, this could generate an invalid author.
    return author


# DONE
def get_title(line, author):
    # NOTE: same issue as the `get_author()` func.
    if author == 'n/a':
        book_id = get_book_id(line)
        title = re.sub(r'\s+' + re.escape(book_id) + r'\n', '', line)
    else:
        p_except_title = re.compile(r",? [bB]y " + re.escape(author) + r"\s+[0-9]+\n")
        title = re.sub(p_except_title, '', line)
    return title


# DONE
# Reads lines from file, with removal of blank lines, and returns a list.
# Plus: also removes quoted lines and non-text noted lines.
def file_to_list(filename):
    lines = []
    with open(filename) as f_in:
        # [Note: ..., [Subtitle: ..., [Language: ..., [Illustrator: ..., [Editor: ...
        # p_square_brackets = re.compile(r'(\s?\[Note:.*)|(.*]\s?)|(\s?\[Subtitle:.*)')
        p_square_brackets = re.compile(r'(\s*\[[A-Z][a-z]+.*)|(.*]\s?)')
        p_audio_book_id = re.compile(r'[A-Z].*\s\s+[0-9]+[A-Z]\n')
        p_format_unrelated = re.compile(r'(.*EBOOK.*)|'
                                        r'(GUTENBERG COLLECTION.*)|'
                                        r'(========+)|'
                                        r'(.*GUTINDEX.*)', re.IGNORECASE)
        just_done_audio = False
        just_done_brackets = False

        for line in f_in:
            # remove blank lines of the file upon appending
            if len(line) != 1:
                # remove line that is quoted within square brackets '[]'
                if just_done_brackets:
                    if is_book_id_line(line):
                        just_done_brackets = False
                        lines.append(line)
                        continue
                    else:
                        continue
                if p_square_brackets.match(line):
                    just_done_brackets = True
                    continue
                # remove line ends with audio book's id
                if just_done_audio:
                    # if line.split()[-1].isdigit():
                    if is_book_id_line(line):
                        just_done_audio = False
                        lines.append(line)
                        continue
                    else:
                        continue
                if p_audio_book_id.match(line):
                    just_done_audio = True
                    continue
                # remove gutenberg's note lines
                if p_format_unrelated.match(line):
                    continue
                if line[0] == ' ' or line[0].islower():
                    continue
                else:
                    lines.append(line)
    return lines


# DONE
# blank lines should be removed before this function
def combine_separated_lines(lines):
    complete = []
    total_lines = len(lines)
    for i in range(total_lines):
        if not is_book_id_line(lines[i]):
            # book_id = get_book_id(lines[i - 1])
            book_id = get_book_id(complete[-1])
            """
            if i < total_lines - 1:
                if not is_book_id_line(lines[i + 1]):
                    l_third = re.sub(r'\n', f'    {book_id}', lines[i + 1])
                    l_second = re.sub(r'\n', l_third, lines[i])
                    combined = re.sub(r'\s\s+.*', l_second, lines[i - 1])
                    complete.append(combined)
                    i += 1
                    continue
            """
            l_second = re.sub(r'\n', f'    {book_id}', lines[i])
            # combined = re.sub(r'\s\s+.*', l_second, lines[i - 1])
            combined = re.sub(r'\s\s+.*', l_second, complete[-1])
            complete.pop()
            complete.append(combined)
        else:
            complete.append(lines[i])
    return complete


# Some remaining problems (might not affect the processing, though).
def problems():
    """
    1. Some of the titles contain notes formatted within brackets like: (Note: ***.)
    2. Authors' names may not be denoted with "by", but also "By", not only r", by "
       or r", By ", but also r" by " or r" By", so the pattern should be this:
       r",? [bB]y ". I am not sure it won't match any other string other than author.
    !. Solution is, exclude 'by'.
    """
    return 0


def build_index():
    raw_index = combine_separated_lines(file_to_list('../data/raw/gutindex.all'))
    # if not os.path.exists('../data/step1/'):
    #     os.makedirs('../data/step1/')
    with open('../data/gutindex_00', 'w') as f_gutindex:
        index_dict = dict()
        p_test = re.compile(r'John Greenleaf Whittier, Vol.*')
        # count = 0
        for record in raw_index:
            # This is an indicator of process.
            # if count % 12742 == 0:
            #     print(f"{(int(count / 12742) + 1) * 2}0%... ", end='')
            # count += 1
            book_id = get_book_id(record)
            author = get_author(record)
            title = get_title(record, author)
            # f_gutindex.write(f'{book_id}\t{author}\t{title}\n')
            # print("{:<7}{:<30}{:<60}".format(book_id, author, title))
            if p_test.match(author):
                author = 'John Greenleaf Whittier'
                # print(author)
            index_dict["book_id"] = book_id
            index_dict["author"] = author
            index_dict["title"] = title
            f_gutindex.write(json.dumps(index_dict) + '\n')
            # f_gutindex.write(f'{book_id}\t{author}\t{title}\n')
        print()


"""
This function modifies some records in `index.all` generated from step 1,
some of them the `author` column is 'n/a', here will manually change the
available ones with a proper author.
Since it relies on the joined corpus of `aparrish.step1` and `index.all`,
so hereby I seperate the procedure from the index sorting functions.
"""


def author_mod():
    with open('../data/gutindex_00', 'r') as f0:
        with open('../data/gutindex_01', 'w') as f1:
            for line in f0:
                line_dict = json.loads(line)
                if line_dict['author'] == 'n/a':
                    if line_dict['book_id'] == '304':
                        line_dict['author'] = 'Rio Grande'
                    elif line_dict['book_id'] == '45470':
                        line_dict['author'] = 'Émile Verhaeren'
                    elif line_dict['book_id'] == '3021':
                        line_dict['author'] = 'Robert Frost'
                    elif line_dict['book_id'] == '17604':
                        line_dict['author'] = 'Anonymous'
                    elif line_dict['book_id'] == '3757':
                        line_dict['author'] = 'Henry Van Dyke'
                    elif line_dict['book_id'] == '2151':
                        line_dict['author'] = 'Edgar Allan Poe'
                    elif line_dict['book_id'] == '21765':
                        line_dict['author'] = 'Publius Ovidius Naso'
                    elif line_dict['book_id'] == '22374':
                        line_dict['author'] = 'RM'
                    elif line_dict['book_id'] == '9580':
                        line_dict['author'] = 'John Greenleaf Whittier'
                    elif line_dict['book_id'] == '1745':
                        line_dict['author'] = 'John Milton'
                    elif line_dict['book_id'] == '1365':
                        line_dict['author'] = 'Henry Wadsworth Longfellow'
                    elif line_dict['book_id'] == '10602':
                        line_dict['author'] = 'Edmund Spenser'
                    elif line_dict['book_id'] == '1287':
                        line_dict['author'] = 'Johann Wolfgang con Goethe'
                    elif line_dict['book_id'] == '1229':
                        line_dict['author'] = 'Sidney Lanier'
                    elif line_dict['book_id'] == '30568':
                        line_dict['author'] = 'Rudyard Kipling'
                    elif line_dict['book_id'] == '30659':
                        line_dict['author'] = 'Robert Louis Stevenson'
                    elif line_dict['book_id'] == '1141':
                        line_dict['author'] = 'Oscar Wilde'
                    elif line_dict['book_id'] == '8187':
                        line_dict['author'] = 'Sir Thomas Moore'
                    elif line_dict['book_id'] == '32459':
                        line_dict['author'] = 'William Wordsworth'
                    elif line_dict['book_id'] == '32986':
                        line_dict['author'] = 'Thomas Stanley'
                    elif line_dict['book_id'] == '4369':
                        line_dict['author'] = 'Alfred Lichtenstein'
                    elif line_dict['book_id'] == '6763':
                        line_dict['author'] = 'Aristotle'
                    elif line_dict['book_id'] == '579':
                        line_dict['author'] = 'Sidney Lanier'
                    elif line_dict['book_id'] == '574':
                        line_dict['author'] = 'William Blake'
                    elif line_dict['book_id'] == '3545':
                        line_dict['author'] = 'Oliver Goldsmith'
                    elif line_dict['book_id'] == '5198':
                        line_dict['author'] = 'George Crabbe'
                    elif line_dict['book_id'] == '38549':
                        line_dict['author'] = 'Richard Crashaw'
                    elif line_dict['book_id'] == '38550':
                        line_dict['author'] = 'Richard Crashaw'
                    elif line_dict['book_id'] == '4756':
                        line_dict['author'] = 'Wallace Irwin'
                    elif line_dict['book_id'] == '2679' \
                            or line_dict['book_id'] == '2678':
                        line_dict['author'] = 'Emily Dickinson'
                    elif line_dict['book_id'] == '22535' \
                            or line_dict['book_id'] == '34289':
                        line_dict['author'] = 'Various'
                    elif line_dict['book_id'] == '7394' \
                            or line_dict['book_id'] == '7391':
                        line_dict['author'] = 'Oliver Wendell Holmes'
                    elif line_dict['book_id'] == '3295' \
                            or line_dict['book_id'] == '3473':
                        line_dict['author'] = 'Emma Lazarus'
                    elif line_dict['book_id'] == '691' \
                            or line_dict['book_id'] == '692':
                        line_dict['author'] = 'James Whitcomb Riley'
                    elif line_dict['book_id'] == '31015' \
                            or line_dict['book_id'] == '33363' \
                            or line_dict['book_id'] == '37452':
                        line_dict['author'] = 'Elizabeth Barrett Browning'
                    elif line_dict['book_id'] == '9600' \
                            or line_dict['book_id'] == '9599' \
                            or line_dict['book_id'] == '9594' \
                            or line_dict['book_id'] == '9590' \
                            or line_dict['book_id'] == '9586' \
                            or line_dict['book_id'] == '9574' \
                            or line_dict['book_id'] == '9569' \
                            or line_dict['book_id'] == '9567' \
                            or line_dict['book_id'] == '9566' \
                            or line_dict['book_id'] == '9565':
                        line_dict['author'] = 'John Greenleaf Whittier'
                    # print(line_dict)
                elif line_dict['author'] == 'Alfred Tennyson' \
                        or line_dict['author'] == 'Lord Tennyson' \
                        or line_dict['author'] == 'Alfred, Lord Tennyson':
                    line_dict['author'] = 'Alfred Lord Tennyson'
                elif line_dict['author'] == 'W. B. Yeats':
                    line_dict['author'] = 'William Butler Yeats'
                elif line_dict['author'] == 'Lord Byron':
                    line_dict['author'] = 'George Gordon Byron'
                f1.write(json.dumps(line_dict) + '\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Run time will be recorded by `main.sh` script.
    # t_begin0 = time()
    # print("Processing raw index file:")
    build_index()
    # print("Time consumed: " + str(time() - t_begin0))
    # t_begin1 = time()
    # print("Some small modifications undergoing:")
    author_mod()
    # print("Time consumed: " + str(time() - t_begin1))
    # print("Finished.")
    # print("Totally consumed: " + str(time() - t_begin0))
