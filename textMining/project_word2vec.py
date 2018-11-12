from pprint import pprint
import sys
import re
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=FutureWarning, module='gensim')
from gensim.models import Word2Vec
from soynlp.tokenizer import RegexTokenizer, LTokenizer, MaxScoreTokenizer



def word2vec(user_file = './review_01_0005_72378155.txt'):
    tokenizer = RegexTokenizer()
    sents = []

    file = open(user_file, 'r', encoding='UTF-8', newline='')

    while True:
        line = file.readline()
        line = re.sub('\s*\n', '', line)

        if "-----------------" not in line:
            sents.append(line)
        if len(sents) > 5000:
            break

    tokenized_contents = []

    for sent in sents:
        temp = tokenizer.tokenize(sent, flatten=True)
        tokenized_contents.append(temp)

    embedding_model = Word2Vec(tokenized_contents, size=100, window=5, min_count=2, workers=4, iter=100, sg=1)
    while True:
        print("User input : ")
        user_input = input()
        if user_input is "":
            break
        else:
            try:
                result = embedding_model.most_similar(positive=[user_input], topn=5)
                for elem in result:
                    print(elem)
            except Exception:
                print("ERROR : 결과가 없습니다.")


word2vec('./review_01_0001_6961757.txt')