import nltk
import pandas as pd

# Tokenizes and normalises the data
import tqdm
from nltk import word_tokenize
from nltk.corpus import stopwords
import re


def noiseRemoval(data):

    stop_words = set(stopwords.words('english'))
    for i in tqdm.tqdm(range(data.shape[0])):
        for j in range(data.iloc[0].shape[0] - 1):
            tokens = word_tokenize(data.iloc[i,j + 1])
            data.iloc[i, j + 1] = " ".join([word for word in tokens if not word in stop_words])

    data['Intro'] = [re.sub(r'\W', ' ', i) for i in data['Intro']]
    data['Specifications'] = [re.sub(r'\W', ' ', i) for i in data['Specifications']]
    data['Case'] = [re.sub(r'\W', ' ', i) for i in data['Case']]
    data['Connectivity'] = [re.sub(r'\W', ' ', i) for i in data['Connectivity']]
    data['Input devices'] = [re.sub(r'\W', ' ', i) for i in data['Input devices']]
    data['Display'] = [re.sub(r'\W', ' ', i) for i in data['Display']]
    data['Performance'] = [re.sub(r'\W', ' ', i) for i in data['Performance']]
    data['Emissions'] = [re.sub(r'\W', ' ', i) for i in data['Emissions']]
    data['Energy management'] = [re.sub(r'\W', ' ', i) for i in data['Energy management']]
    data['Verdict'] = [re.sub(r'\W', ' ', i) for i in data['Verdict']]

    normalization(data)


def normalization(data):

    lemmatizer = nltk.stem.WordNetLemmatizer()
    for i in tqdm.tqdm(range(data.shape[0])):
        for j in range(data.iloc[0].shape[0] - 1):
            word_list = word_tokenize(data.iloc[i, j + 1])
            data.iloc[i, j + 1] = ' '.join([lemmatizer.lemmatize(w) for w in word_list])

    sentimentAnalysis(data)


def sentimentAnalysis(data):

    for index, row in tqdm.tqdm(data.iterrows()):
        tokenizedList = nltk.word_tokenize(row)


def main():
    data = pd.read_csv('outputBrand.csv')
    noiseRemoval(data)

main()