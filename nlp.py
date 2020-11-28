import re
import nltk.tokenize.punkt
import nltk
import spacy; spacy.load('en')
import statistics
import math
from lexical_diversity import lex_div as ld

nltk.download('punkt')


def tokens_no_nums(txt):
    txt = re.sub('\d', '', txt)
    tokens = nltk.word_tokenize(txt)
    words = [word for word in tokens if word.isalpha()]
    return words


def token_count(txt):
    return len(tokens_no_nums(txt))


def verse_count(txt):
    return len([a for a in txt.split('\n') if a != ''])


def mtld(txt):
    nlp = spacy.load('en')
    doc = nlp(u""+txt)
    txt = ""
    for token in doc:
        txt += (" " + token.lemma_)
    txt = tokens_no_nums(txt)
    return ld.mtld_ma_wrap(txt)


def hdd(txt):
    nlp = spacy.load('en')
    doc = nlp(u""+txt)
    txt = ""
    for token in doc:
        txt += (" " + token.lemma_)
    txt = tokens_no_nums(txt)
    return ld.hdd(txt)*100


def letter_count(txt):
    num_words = 0
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    new_txt = ""

    for char in txt:
        if char not in punctuations:
            new_txt = new_txt + char

    for char in new_txt:
        if char == " ":
            pass
        else:
            num_words += 1
    return num_words


def data_clean(txt):
  clean = re.sub('(\[.*\])|(\(.*\))', '', txt)
  lines = [line for line in clean.split('\n')]
  resp = ""
  for i in range(0, len(lines)-2):
    if not (lines[i] == '' and lines[i+1] == ''):
      resp += (lines[i] + '\n')
  return resp


def coleman_liau_index(txt):
    s = (0.5*verse_count(txt) * (100 / token_count(txt)))
    l = (letter_count(txt) * (100 / token_count(txt)))
    return ((0.0588 * l) - (0.296 * s) - 15.8)


def coleman_liau_index_vote(txt):
    txt = data_clean(txt)
    resp = coleman_liau_index(txt)
    if resp <= 5.0:
        return 0
    elif resp > 5.0 and resp <= 6.0:
        return 1
    elif resp > 6.0 and resp <= 7.0:
        return 2
    elif resp > 7.0 and resp <= 10.0:
        return 3
    elif resp > 10.0 and resp <= 12.0:
        return 4
    elif resp > 12.0 and resp <= 16.0:
        return 5
    else:
        return 6


def mtld_vote(txt):
    txt = data_clean(txt)
    resp = mtld(txt)
    if resp <= 15.0:
        return 0
    elif resp > 15.0 and resp <= 25.0:
        return 1
    elif resp > 25.0 and resp <= 35.0:
        return 2
    elif resp > 35.0 and resp <= 45.0:
        return 3
    elif resp > 45.0 and resp <= 65.0:
        return 4
    elif resp > 65.0 and resp <= 90.0:
        return 5
    else:
        return 6


def hdd_vote(txt):
    txt = data_clean(txt)
    resp = hdd(txt)
    if resp <= 30.0:
        return 0
    elif resp > 30.0 and resp <= 60.0:
        return 1
    elif resp > 60.0 and resp <= 70.0:
        return 2
    elif resp > 70.0 and resp <= 85.0:
        return 3
    elif resp > 75.0 and resp <= 80.0:
        return 4
    elif resp > 80.0 and resp <= 85.0:
        return 5
    else:
        return 6


def vote_mean(txt):
    results = [mtld_vote(txt), hdd_vote(txt), coleman_liau_index_vote(txt)]
    return math.ceil(statistics.mean(results))


def vote_decode(n):
    if n <= 0:
        return "A1"
    elif n == 1:
        return "A2"
    elif n == 2:
        return "B1"
    elif n == 3:
        return "B2"
    elif n == 4:
        return "C1"
    elif n == 5:
        return "C2"
    else:
        return "C2"


def difficulty(song):
    return vote_decode(vote_mean(song["lyrics"]))
