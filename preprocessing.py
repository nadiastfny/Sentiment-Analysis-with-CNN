import os
import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import tensorflow as tf
import re
import numpy as np
import pandas as pd
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from tensorflow.keras.preprocessing.text import Tokenizer

def case_folding(tokens): 
    return tokens.lower()  

def cleansing(review):
    review = re.sub(r'[^\x00-\x7f]', r'', review)
    review = re.sub(r'(\\u[0-912345678A-Fa-f]+)', r'', review)
    review = re.sub(r"[^A-Za-z0123456789^,!.\/'+-=]", " ", review)
    review = re.sub(r'[=\+/&!<>;\'\"\?%#$@\,\. \t\r\n]', r' ', review)
    review = re.sub(r'\\u\w\w\w\w', '', review)
    # Remove simbol, angka dan karakter aneh
    review = re.sub(r'(.)\1{1,}', r'\1', review)
    
    return review
    
def formalize_slang_word(review):
    text_list = review.split(' ')
    slang_words_raw = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\kamus\kamus_normalisasi_baru.csv', sep=',', header=None)
    slang_word_dict = {}
    
    for item in slang_words_raw.values:
        slang_word_dict[item[0]] = item[1]
        
        for index in range(len(text_list)):
            if text_list[index] in slang_word_dict.keys():
                text_list[index] = slang_word_dict[text_list[index]]
                
    return ' '.join(map(str, text_list))

def remove_unused_character(review):
#     text_list = review
    text_list = review.split(' ')
    text_list_temp = []

    for index in range(len(text_list)):
        if len(text_list[index]) >= 3:
            text_list[index] = ' '.join(text_list[index].split())
            text_list_temp.append(text_list[index])
    return text_list_temp 

def removeStopword(review):
    stopwords = open('D:\BAHAN SKRIPSI\program_skripsi\data\kamus\kamus_stopword_baru.csv', 'r').read().split()
    review_stop = []
    filteredtext = [word for word in review if word not in stopwords]
    review_stop.append(" ".join(filteredtext))
    return ' '.join(review_stop)

def open_kamus_prepro(x):
  kamus={}
  with open(x,'r') as file :
    for line in file :
      slang=line.replace("'","").split(':')
      kamus[slang[0].strip()]=slang[1].rstrip('\n').lstrip()
  return kamus

kamus_negasi = open_kamus_prepro('D:\BAHAN SKRIPSI\program_skripsi\data\kamus\kamus negasi.txt')
def ganti_negasi(w):
  w_splited = w.split(' ')
  if 'tidak' in w_splited:
     index_negasi = w_splited.index('tidak')
     for i,k in enumerate(w_splited):
       if k in kamus_negasi and w_splited[i-1] == 'tidak':
         w_splited[i] = kamus_negasi[k]

  return ' '.join(w_splited)

factory = StemmerFactory()
stemmer = factory.create_stemmer()
def stemming(tokens):
    tokens = tokens.lower()
    tokens = stemmer.stem(tokens)
    return tokens

def tokenize(tokens):
    # nltk.download('punkt')
    token = nltk.tokenize.word_tokenize(str(tokens))
    return token

def preprocessing_text(text):
    text = case_folding(text)
    text = cleansing(text)
    text = formalize_slang_word(text)
    text = stemming(text)
    text = remove_unused_character(text)
    text = removeStopword(text)
    text = ganti_negasi(text)
    text = tokenize(text)
    return text
    
# def join_negation(review):
#     text_list = review
#     for index in range(len(text_list)):
#         if (text_list[index] == 'tidak' or text_list[index] == 'kurang' or text_list[index] == 'jangan' or text_list[index] == 'bukan'):
#             if index < len(text_list) - 1:
#                 text_list[index] = text_list[index] + "_" + text_list[index + 1]
#                 text_list[index + 1] = ''
#             else: 
#                 text_list[index] = ''  
#     return ' '.join(' '.join(text_list).split())

 
# def split_konjungsi(review):
#     review = review.split(' ')
#     rsl = []
    
#     for val in review:
#         for kal in val.split():
#             if (kal == "tapi" or kal == "tetapi" or kal == "walaupun" or kal == "meskipun" or kal == "padahal" or kal == "namun"):
#                 if kal == "tapi":
    #                 tmp = val.split("tapi")
    #             elif kal == "tetapi":
    #                 tmp = val.split("tetapi")
    #             elif kal == "walaupun":
    #                 tmp = val.split("walaupun")
    #             elif kal == "meskipun":
    #                 tmp = val.split("meskipun")
    #             elif kal == "padahal":
    #                 tmp = val.split("padahal")
    #             elif kal == "namun":
    #                 tmp = val.split("namun")
    #             break
    #         else : 
    #              tmp = [val]
    #     for vall in tmp:
    #         vall = ' '.join(vall.split())
    #         rsl.append(vall)
    # return rsl
