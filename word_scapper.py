import urllib
from bs4 import BeautifulSoup
import re

def scrap_top_words(url):
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r).find('div', {'id': 'bodyContent'})

    # removes style tags and inner content, others tag only
    tags = '(<style.*?>.*?<.*?>)|(<.*?>)'
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
    freq_list = [(k, v) for k, v in sorted(
        freq.items(), key=lambda x:x[1], reverse=True)]
    return freq_list[:10]
