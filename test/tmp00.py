#!/usr/bin/env python

# generate author list

def test():
    import json
    dante = []
    milton = []
    yeats = []
    whitman = []
    shakespeare = []
    eliot = []
    pound = []
    with open('../data/corpus_07c/part-r-00000', 'r') as f:
        for line in f:
            line = json.loads(line)
            author = line["author"]
            line = line["line"]
            if author == 'Dante Alighieri':
                dante.append(line)
            elif author == 'John Milton':
                milton.append(line)
            elif author == 'William Butler Yeats':
                yeats.append(line)
            elif author == 'William Shakespeare':
                shakespeare.append(line)
            elif author == 'Walt Whitman':
                whitman.append(line)
            elif author == 'T. S. Eliot':
                eliot.append(line)
            elif author == 'Ezra Pound':
                pound.append(line)
            else:
                continue
        # print'', len())
        print('dante:', len(dante))
        print('milton:', len(milton))
        print('yeats:', len(yeats))
        print('whitman:', len(whitman))
        print('shakespeare:', len(shakespeare))
        print('eliot', len(eliot))
        print('pound', len(pound))

    with open('dante_milton', 'w') as dm:
        for i in range(len(dante)):
            dm.write(f'dante\t{dante[i]}\n')
        for i in range(len(milton)):
            dm.write(f'milton\t{milton[i]}\n')
    with open('milton_yeats', 'w') as my:
        for i in range(len(milton)):
            my.write(f'1\t{milton[i]}\n')
        for i in range(len(yeats)):
            my.write(f'0\t{yeats[i]}\n')
    with open('whitman_shakespeare', 'w') as ws:
        for i in range(len(whitman)):
            ws.write(f'1\t{whitman[i]}\n')
        for i in range(len(shakespeare)):
            ws.write(f'0\t{shakespeare[i]}\n')

    with open('eliot_pound', 'w') as ep:
        for i in range(len(eliot)):
            ep.write(f'1\t{eliot[i]}\n')
        for i in range(len(pound)):
            ep.write(f'0\t{pound[i]}\n')


"""
- 
"""

test()

"""
dante: 109443
milton: 37284
yeats: 14097
shakespeare: 7885
whitman: 9334


dante_milton 146727

"""

"""
0 Dante Alighieri
1 Homer
2 Burton Egbert Stevenson
3 Henry Wadsworth Longfellow
4 Anonymous
5 Elias Lönnrot
6 Sir Thomas Moore
7 Lodovico Ariosto
8 John Milton
9 Virgil
10 John Gower
11 Philip Freneau
12 Madison J. Cawein
13 Ella Wheeler Wilcox
14 George Gordon Byron
15 Robert Louis Stevenson
16 Alfred Noyes
17 Rudyard Kipling
18 James Whitcomb Riley
19 Algernon Charles Swinburne
20 Robert Burns and Allan Cunningham
21 Alexander Pope
22 James Parton
23 George Meredith
24 Robert Burns
25 William Morris
26 Robert Herrick
27 Edgar Lee Masters
28 Thomas Hardy
29 John Greenleaf Whittier
30 James Russell Lowell
31 Alfred Lord Tennyson
32 Elizabeth Barrett Browning
33 Richard Crashaw
34 Torquato Tasso
35 Ovid
36 William Butler Yeats
37 Robert Browning
38 Robert Bridges
39 John Masefield
40 William Wordsworth
41 Andrew Lang
42 Emma Lazarus
43 Johann Wolfgang con Goethe
44 Edgar A. Guest
45 Thomas Cowherd
46 William Cullen Bryant
47 Emily Dickinson
48 Francis Thompson
49 Lu?de Cam?
50 Lucan
51 Francis Turner Palgrave
52 Frederich Schiller
53 Eugene Field
54 Geoffrey Chaucer
55 Smyrnaeus Quintus
56 Robert W. Service
57 Edward Young
58 Lucretius
59 Oscar Wilde
60 Walt Whitman
61 Harry Graham
62 Amy Lowell
63 Edmund Spenser
64 William Lisle Bowles
65 Edwin Arlington Robinson
66 Father Ryan
67 Willam Combe
68 Adelaide Anne Procter
69 George Borrow
70 Omar Khayyam
71 James Beattie
72 John Keats
73 Coventry Patmore
74 William Shakespeare
75 Sidney Lanier
76 Owen Meredith
77 Margeret Sprague Carhart
78 Gilbert Parker
79 Sebastian Brandt
80 Raymond MacDonald Alden, Ph.D
81 Joseph Victor von Scheffel
82 Cale Young Rice
83 John Wilson
84 Erasmus Darwin
85 Bret Harte
86 Richard Lovelace
87 William Wright
88 John Keble
89 John Dryden
90 Robert Southey
91 Henry Vaughan
92 Charles Rogers
93 Oliver Goldsmith
94 Walter Scott
95 C. J. Dennis
96 Vachel Lindsay
97 Maurice Hewlett
98 Katherine H. Shute
99 W. Y. Sellar
100 James Baldwin
101 Oliver Wendell Holmes
102 Heinrich Heine
103 Dunstan Gale et al.
104 Bertram Stevens
105 Bjornstjerne Bjornson
106 William Cowper
107 Rossiter Johnson
108 William Makepeace Thackeray
109 John Clare
110 Henry W. Longfellow
111 Edward Lear
112 Winston Stokes
113 Sara Teasdale
114 Joaquin Miller
115 Samuel Taylor Coleridge
116 Eric Mackay
117 Sir Walter Scott
118 Johann W. Von Goethe
119 George P. Morris
120 Currer, Ellis, and Acton Bell
121 John Castillo
122 Johann Wolfgang Von Goethe
123 James McIntyre
124 Edward Ziegler Davis
125 Lewis Morris
126 Goethe
127 Rabindranath Tagore
128 Frank Sidgwick
129 Laura E. Richards
130 A. Novice
131 A. B. Paterson
132 Samuel Johnson
133 Hiram Hoyt Richmond
134 Archibald Lampman
135 John Oxenham
136 Bliss Carman
137 Walter R. Cassels
138 Robert Frost
139 Austin Dobson
140 J. D. Cossar
141 Arthur Conan Doyle
142 Henry Timrod
143 F. W. Moorman
144 Edgar Allan Poe
145 Jean Blewett
146 Charles G. Leland
147 Alexander Smith
148 Henry Van Dyke
149 John Gay
150 Madison Julius Cawein
151 Aurelius Clemens Prudentius
152 Leon Gautier
153 Edwin Arnold
154 Harrison S. Morris
155 W. M. MacKeracher
156 James Parkerson
157 Henry Newbolt
158 Ezra Pound and Ernest Fenollosa
159 J. C. Squire
160 Will Carleton
161 E. Nesbit
162 William Ernest Henley
163 Orson F. Whitney
164 Thomas W. Talley
165 Esaias Tegne'r
166 Publius Ovidius Naso
167 Rebekah Smith
168 Robert Malise Bowyer Nichols
169 John Bowring
170 Fannie Isabelle Sherrick
171 Rupert Brooke
172 Bliss Carman and Richard Hovey
173 Henry David Thoreau
174 Robert Haven Schauffler
175 Alfred Castner King
176 Wilfrid Wilson Gibson
177 George W. Sands
178 David Lester Richardson
179 Carolyn Wells
180 Kostes Palamas
181 Susanna Moodie
182 Walter de la Mare
183 Edna St. Vincent Millay and Robert Frost
184 Lola Ridge
185 G. K. Chesterton
186 Adam Lindsay Gordon
187 William D. Howells
188 W. S. Gilbert
189 Frederick Locker
190 Christopher Morley
191 Margaret E. Sangster
192 Michael Drayton
193 Joseph Horatio Chant
194 Walter Crane
195 Eugenia Dunlap Potts
196 Lewis Carroll
197 Toru Dutt
198 John Gould Fletcher
199 Lennox Amott
200 Laurence Hope
201 Susan Coolidge
202 Helene A. Guerber
203 Don Marquis
204 Angus MacKay
205 Helen Hay Whitney
206 John Dos Passos
207 Henry Kendall
208 Conrad Aiken
209 Mathilde Blind
210 Elizabeth Atkins
211 Edwin Alfred Watrous
212 Henry Abbey
213 Margaret Fuller
214 Eliza Lee Follen
215 John Presland
216 E. Pauline Johnson
217 William Young Sellar
218 Mathias Casimire Sarbiewski
219 Edith Nesbit
220 Robert Graves
221 T. W. H. Crosland
222 David Roberts
223 Francis Adams
224 Edna St. Vincent Millay
225 Charles Baudelaire
226 Francis Sherman
227 Edward Dyson
228 Henry Lawson
229 Palmer Cox
230 William Collins
231 Clara Doty Bates
232 Thomas Oldham
233 Edward Moore
234 Sarah S. Mower
235 Cotton Noe
236 Th?hile Gautier
237 Mary C. Sturgeon
238 Andrew Barton 'Banjo' Paterson
239 Percy Bysshe Shelley
240 Thomas Davis
241 C. S. Calverley
242 M.E.S. Wright
243 Lewis Sprague Mills
244 Rio Grande
245 Oscar Kuhns
246 Oliver Wendell Holmes, Sr.
247 Kalidasa
248 Hilda Doolittle
249 Ada Langworthy Collier
250 Edith M. Thomas
251 Thomas Bailey Aldrich
252 Julius Madison Cawein
253 Adam Mickiewicz
254 Charles Sangster
255 Robert Norwood
256 Frances Anne Butler
257 A. E. Housman
258 Joseph C. Lincoln
259 Juliana Horatia Ewing
260 Siegfried Sassoon
261 Alice Meynell
262 Thomas Stanley
263 Marion Forster Gilmore
264 Gerard Manley Hopkins
265 Aubrey De Vere
266 Anne Killigrew
267 Thomas Cooper
268 William Vaughn Moody
269 Alan Seeger
270 Joseph Victor Scheffel
271 R. C. Lehmann
272 Olive T. Dargan
273 Vidyapati Thakura
274 Fitz-Greene Halleck
275 Bert Leston Taylor
276 Willis Boyd Allen
277 Isabel Ecclestone Mackay
278 Mary Gardiner Horsford
279 Josephine Preston Peabody
280 Walter De La Mare
281 Evan Evans
282 William Blake
283 Erwin Clarkson Garrett
284 George A. Baker, Jr.
285 Clark Ashton Smith
286 Frances E. W. Harper
287 Ezra Pound
288 Jean Louis de Esque
289 Nathaniel Parker Willis
290 Phillis Wheatley
291 Thomas Gray
292 Elizabeth Stuart Phelps
293 Charles G. D. Roberts
294 John Niendorff
295 Thomas Nelson Page
296 Kate Greenaway
297 Walter Savage Landor
298 Curtis C. Bushnell
299 Stephen Vincent Benet
300 Louis Untermeyer
301 Edmund Vance Cooke
302 Gene Stratton-Porter
303 T. S. Eliot
304 Lafcadio Hearn
305 Marian Longfellow
306 Frank Justus Miller
307 Irving Sidney Dix
308 Marjorie Allen Seiffert
309 G. S. Cautley
310 L. Cranmer-Byng
311 Hannah Lavinia Baily
312 Henry More
313 Norah M. Holland
314 William Carlos Williams
315 George W. Doneghy
316 Margaret A. Richard
317 Émile Verhaeren
318 Joseph Rodman Drake
319 Myrtle Reed
320 Chauncey Brewster Tinker
321 Dora Sigerson Shorter
322 Philip Sidney
323 Robert Bloomfield
324 Everard Jack Appleton
325 E. Estlin Cummings, S. Foster Damon,
326 Francis Brett Young
327 Henry Hart Milman
328 David Rorie
329 George Colman, the Younger
330 John Collings Squire and Charles Baudelaire
331 Arthur Macy
332 Seosamh MacCathmhaoil
333 Elizabeth Turner
334 Elva S. Smith
335 Henry A. Beers
336 Charles Hamilton Musgrove
337 Edith Wharton
338 Fay Inchfawn
339 Morris Rosenfeld
340 Horatio Alger, Jr
341 Esther Nelson Karn
342 Dante Gabriel Rossetti
343 Kabir
344 Hilda Conkling
345 Frank Oliver Call
346 Leigh Gordon Giltner
347 Sappho
348 Helen Leah Reed
349 John Lydgate
350 William Dean Howells
351 Violet Jacob
352 Henry van Dyke
353 Charlton Miner Lewis
354 G.K. Chesterton
355 Stephen Crane
356 David Morton
357 Edinburgh Burgess Golfing Society
358 George W. Caldwell
359 James Henry Cousins
360 Annie Fellows Johnston and Albion Fellows Bacon
361 Theodore H. Rand
362 John Charles McNeill
363 The Men of the 1st. and 2nd.
364 James Bramston
365 Evaleen Stein
366 Evelyn Scott
367 Robert W. Norwood
368 Sibyl Bristowe
369 Bernard Gilbert
370 James Stephens
371 Muriel Stuart
372 Edward Smyth Jones
373 Barbara Hofland
374 Casper Almore
375 James Elroy Flecker
376 Alfred Lichtenstein
377 Dhan Gopal Mukerji
378 Frank R. Heine
379 Dorothy Una Ratcliffe
380 Virna Sheard
381 Alfred Austin
382 Robert J. C. Stead
383 Owen Seaman
384 Aldous Huxley
385 Joseph R. Wilson
386 Rennell Rodd
387 Richard Aldington,
388 Sallie Southall Cotten
389 Clive Hamilton
390 A.H. Laidlaw
391 Christin?e Pisan
392 Thomas Orchard
393 Laurence Alma-Tadema
394 Gilbert Keith Chesterton
395 Hilaire Belloc
396 Nancy Byrd Turner
397 Emile Verhaeren
398 William Young
399 W. E. Henley
400 Andrew Cecil Bradley
401 Odell Shepard
402 Mary Baker Eddy
403 William Hodgson Ellis
404 John Graham Bower and Klaxon
405 James Thomson
406 Wilfred Scawen Blunt
407 Frederick Locker-Lampson
408 Arthur Stringer
409 Thomas Moore
410 Edwin C. Ranck
411 Ezra Pound and T.E. Hulme
412 Aldington et al.
413 Arthur Symons
414 Lydia Howard Sigourney
415 John William Draper
416 James E. Pickering
417 C. Harrison
418 Anne Collins
419 Charles Dickens
420 Max Eastman
421 Badger Clark
422 Edmund Goldsmid
423 James Williams
424 A. D. Godley
425 Louisa May Alcott
426 W.H.G. Kingston
427 Miss Mulock
428 Wilhelm Busch

"""
