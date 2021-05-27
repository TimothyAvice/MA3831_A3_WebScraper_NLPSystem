# Packages
import re

import en_core_web_sm
import nltk
import pandas as pd
from nltk import word_tokenize
from pprint import pprint
# Perform parts of speech tagging on the review titles
from nltk.corpus import stopwords


def preprocess(sentence):
    sent = nltk.word_tokenize(sentence)
    sent = nltk.pos_tag(sent)
    return sent


def segmenter(sentence):
    sentence_segments = []
    segment1 = ""
    segment2 = ""

    index = sentence.find(": ")
    if index == -1:
        index = sentence.find("- ")
        if index == -1:
            return [sentence, ' ']

    for i in range(index):
        segment1 += sentence[i]

    for i in range(len(sentence) - (index+1)):
        segment2 += sentence[i + index+1]

    sentence_segments.append(segment1)
    sentence_segments.append(segment2)

    return sentence_segments


# Extract the laptop names and the brands
def tokenizeTitles(data):
    NNP_titles = []
    review_titles = data['Title']
    for title in review_titles:
        NNP_words = []
        sentence_segments = segmenter(title)
        brand_section = 0

        if sentence_segments[1] != ' ':
            if "review" not in sentence_segments[0].lower():
                brand_section = 1

        text = preprocess(sentence_segments[brand_section])
        for item in text:
            if item[1] == "NNP" or item[1] == "JJ":
                NNP_words.append(item[0])

        NNP_titles.append(NNP_words[0])

    print(NNP_titles)

    return NNP_titles


def namedEntityRecognition(data):
    nlp = en_core_web_sm.load()
    for title in data['Title']:
        text = nlp(title)
        pprint([(X.text, X.label_) for X in text.ents])


def main():
    data = pd.read_csv('output.csv')

    namedEntityRecognition(data)
    # brands = tokenizeTitles(data)
    # data['Brand'] = brands
    # # data['Laptop_name'] = laptop_name
    #
    # data.to_csv('outputBrand.csv', index=False)


main()
