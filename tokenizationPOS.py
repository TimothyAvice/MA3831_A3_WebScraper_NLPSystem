# Packages
import pandas as pd
import nltk


# Perform parts of speech tagging on the review titles
def preprocess(sentence):
    sent = nltk.word_tokenize(sentence)
    sent = nltk.pos_tag(sent)
    return sent


# Extract the laptop names and the brands
def extractTitleInfo(data):
    NNP_titles = []
    review_titles = data['Title']
    for title in review_titles:
        NNP_words = []
        text = preprocess(title)
        for word in text:
            if word[1] == 'NNP':
                NNP_words.append(word[0])
        NNP_titles.append(NNP_words)

    brands = []
    laptop_name = []
    for title in NNP_titles:
        brands.append(title[0])
        laptop_name.append(title[1])

    return brands, laptop_name


def main():
    data = pd.read_csv('output.csv')
    brands, laptop_name = extractTitleInfo(data)
    data['Brand'] = brands
    data['Laptop_name'] = laptop_name

    data.to_csv('outputBrand.csv', index=False)


main()
