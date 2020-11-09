import re
from flask.helpers import flash
import nltk.tokenize.punkt
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
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


def coleman_liau_index(txt):
    s = (0.5*verse_count(txt) * (100 / token_count(txt)))
    l = (letter_count(txt) * (100 / token_count(txt)))
    return ((0.0588 * l) - (0.296 * s) - 15.8)


def coleman_liau_index_vote(txt):
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
        return "Fluent"


app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route("/", methods=['POST'])
@cross_origin()
def post():
    song = request.get_json()

    response = jsonify(
        difficulty=vote_decode(
            coleman_liau_index_vote(song['lyrics'])))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')

    return response


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()
