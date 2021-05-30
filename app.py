import re
from flask import Flask, request, Response
import urllib
from bs4 import BeautifulSoup
import re
from flask.json import jsonify
from flask_cors import CORS
from werkzeug.datastructures import MIMEAccept

app = Flask(__name__, '/static/')
cors = CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/find', methods=["POST"])
def find():
    data = request.json
    res = scrap_word_counts(data.get('url'))
    return jsonify(data=res)


def scrap_word_counts(url):
    try:
        r = urllib.request.urlopen(url)
        soup = BeautifulSoup(r).find(
            'div', {'id': 'bodyContent'})
        # removes style tags and inner content, others tag only
        tags = '(<.*?>)'
        # remove tags
        for child in soup(['style', 'script']):
            child.decompose()
        words = re.sub(tags, ',', soup.prettify())
        words = re.split('\n|,| ', words)
        freq = dict()
        for word in words:
            w = word.strip()
            w = re.sub('[^\w+]', '', w)
            if w != '':
                try:
                    freq[w] += 1
                except KeyError:
                    freq[w] = 1
        freq_dict = sorted(
            freq.items(), key=lambda x: x[1], reverse=True)[:10]
        return freq_dict
    except:
        return 'Incorrect Url or Internal error'
