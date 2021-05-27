# Packages
import os

import nltk
import pandas as pd
import tqdm
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

java_path = r"C:\Program Files\Java\jre1.8.0_291\bin\java.exe"
os.environ['JAVAHOME'] = java_path


# def preprocess(sentence):
#     sent = nltk.word_tokenize(sentence)
#     sent = nltk.pos_tag(sent)
#     return sent
#
#
# def segmenter(sentence):
#     sentence_segments = []
#     segment1 = ""
#     segment2 = ""
#
#     index = sentence.find(": ")
#     if index == -1:
#         index = sentence.find("- ")
#         if index == -1:
#             return [sentence, ' ']
#
#     for i in range(index):
#         segment1 += sentence[i]
#
#     for i in range(len(sentence) - (index + 1)):
#         segment2 += sentence[i + index + 1]
#
#     sentence_segments.append(segment1)
#     sentence_segments.append(segment2)
#
#     return sentence_segments
#
#
# Extract the laptop names and the brands
# def tokenizeTitles(data):
#     NNP_titles = []
#     review_titles = data['Title']
#     for title in review_titles:
#         NNP_words = []
#         sentence_segments = segmenter(title)
#         brand_section = 0
#
#         if sentence_segments[1] != ' ':
#             if "review" not in sentence_segments[0].lower():
#                 brand_section = 1
#
#         text = preprocess(sentence_segments[brand_section])
#         for item in text:
#             if item[1] == "NNP" or item[1] == "JJ":
#                 NNP_words.append(item[0])
#
#         NNP_titles.append(NNP_words[0])
#
#     print(NNP_titles)
#
#     return NNP_titles


def namedEntityRecognition(data):
    brandNames = []
    model_filename = './stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz'
    path_to_jar = './stanford-ner-2020-11-17/stanford-ner.jar'
    st = StanfordNERTagger(model_filename=model_filename, path_to_jar=path_to_jar, encoding='utf-8')
    for i in tqdm.tqdm(range(len(data['Title']))):
        organizations = []
        tokens = word_tokenize(data.loc[i, 'Title'])
        classified_text = st.tag(tokens)
        for item in classified_text:
            if item[1] == 'ORGANIZATION':
                organizations.append(item[0])
        if len(organizations) == 0:
            brandNames.append("No brand found")
        else:
            brandNames.append(organizations[0])

    counter = 0
    for brand in brandNames:
        if brand == "No brand found":
            counter += 1

    print("Number of non branded entries: " + str(counter))
    print("Percentage detection: " + str((counter - len(brandNames)/(len(brandNames) + 0.0))*100))

    return brandNames


def main():
    data = pd.read_csv('output.csv')

    brands = namedEntityRecognition(data)
    # brands = tokenizeTitles(data)
    data['Brand'] = brands
    # # data['Laptop_name'] = laptop_name
    #
    data.to_csv('outputBrand.csv', index=False)


main()
