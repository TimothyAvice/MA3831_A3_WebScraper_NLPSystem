# Packages
import os

import en_core_web_sm
import nltk
import pandas as pd
import tqdm
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

java_path = r"C:\Program Files\Java\jre1.8.0_291\bin\java.exe"
os.environ['JAVAHOME'] = java_path


def spacy(data):
    brandNames = []
    nlp = en_core_web_sm.load()
    for i in tqdm.tqdm(range(len(data['Title']))):
        organizations = []
        classified_text = nlp(data.loc[i, 'Title'])
        for item in classified_text.ents:
            if item.label_ == 'ORG':
                organizations.append(item.text)
        if len(organizations) == 0:
            brandNames.append("No brand found")
        else:
            brandNames.append(organizations[0])

    counter = 0
    for brand in brandNames:
        if brand == "No brand found":
            counter += 1

    print("Number of non branded entries: " + str(counter))
    print("Percentage detection: " + str(((len(brandNames) - counter)/(len(brandNames) + 0.0))*100))

    return brandNames


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
    print("Percentage detection: " + str(((len(brandNames) - counter)/(len(brandNames) + 0.0))*100))

    return brandNames


def main():
    data = pd.read_csv('output.csv')

    brands = namedEntityRecognition(data)
    brands2 = spacy(data)

    print(brands)
    print(brands2)
    # brands = tokenizeTitles(data)
    # data['Brand'] = brands
    # # data['Laptop_name'] = laptop_name
    #
    # data.to_csv('outputBrand.csv', index=False)


main()
