import nltk
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tqdm
from nltk import word_tokenize
from nltk.corpus import stopwords
import re


def noiseRemoval(data):
    stop_words = set(stopwords.words('english'))
    for i in tqdm.tqdm(range(data.shape[0])):
        for j in range(data.iloc[0].shape[0] - 1):
            tokens = word_tokenize(data.iloc[i, j + 1].lower())
            if j != data.iloc[0].shape[0] - 1:
                data.iloc[i, j + 1] = " ".join([word for word in tokens if not word in stop_words])

    data['Intro'] = [re.sub(r'\W', ' ', i) for i in data['Intro']]
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


# Return sentiment of sentence. Returning 0.0 in all fields if it is none
def vader(sentence):
    analyser = SentimentIntensityAnalyzer()
    if sentence == "none":
        return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
    else:
        return analyser.polarity_scores(sentence)


def sentimentAnalysis(data):
    segments = [[], [], [], [], [], [], [], [], []]
    for index, row in tqdm.tqdm(data.iterrows()):
        segments[0].append(vader(row['Intro']))
        segments[1].append(vader(row['Case']))
        segments[2].append(vader(row['Connectivity']))
        segments[3].append(vader(row['Input devices']))
        segments[4].append(vader(row['Display']))
        segments[5].append(vader(row['Performance']))
        segments[6].append(vader(row['Emissions']))
        segments[7].append(vader(row['Energy management']))
        segments[8].append(vader(row['Verdict']))

    data['Intro sentiment'] = segments[0]
    data['Case sentiment'] = segments[1]
    data['Connectivity sentiment'] = segments[2]
    data['Input devices sentiment'] = segments[3]
    data['Display sentiment'] = segments[4]
    data['Performance sentiment'] = segments[5]
    data['Emissions sentiment'] = segments[6]
    data['Energy management sentiment'] = segments[7]
    data['Verdict sentiment'] = segments[8]

    data.to_csv('outputBrandSentiment.csv', index=False)


def main():
    data = pd.read_csv('outputBrand.csv')
    noiseRemoval(data)


main()
