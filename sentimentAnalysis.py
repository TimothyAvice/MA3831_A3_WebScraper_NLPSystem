import nltk
import pandas as pd

# Tokenizes and normalises the data
def preprocessing(data):
    data[''] = nltk.word_tokenize(sentence)

def main():
    data = pd.read_csv('outputBrand.csv')



main()