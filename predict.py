import numpy as np
import tensorflow as tf
import json
import re
import requests
from bs4 import BeautifulSoup
from keras.models import load_model
from preprocessing import preprocessing_text
from gensim.models.word2vec import Word2Vec
import os.path
import sys
import json
import base64
import string
#load model preprocessing
import numpy as np
import pandas as pd
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import keras.models
from keras.models import model_from_json
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Load Model
json_file = open('D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_v1.json', 'r')
model_json = json_file.read()
model = model_from_json(model_json)
model.load_weights("D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_v1.h5")

with open('D:\BAHAN SKRIPSI\program_skripsi\models\tokenizer.pickle', 'rb') as handle:
	tokenizer = pickle.load(handle)

cek = json.loads(base64.b64decode(sys.argv[1]))
data = cek['data']
data = [data]
data = np.array(data)



def case_folding(data): 
    data = data.lower()
    return data  

def cleansing(data):
    data = re.sub(r'[^\x00-\x7f]', r'', data)
    data = re.sub(r'(\\u[0-9A-Fa-f]+)', r'', data)
    data = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", data)
    data = re.sub(r'\\u\w\w\w\w', '', data)
    # Remove simbol, angka dan karakter aneh
    data = re.sub(r"[.,:;+!\-_<^/=?\"'\(\)\d\*]", " ", data)
    data = re.sub(r'(.)\1{1,}', r'\1', data)
    return data
    
def formalize_slang_word(data):
    text_list = data.split(' ')
    slang_words_raw = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\kamus\kamus_normalisasi_baru.csv', sep=',', header=None)
    slang_word_dict = {}
    
    for item in slang_words_raw.values:
        slang_word_dict[item[0]] = item[1]
        
        for index in range(len(text_list)):
            if text_list[index] in slang_word_dict.keys():
                text_list[index] = slang_word_dict[text_list[index]]
                
    return ' '.join(map(str, text_list))

def remove_unused_character(data):
#     text_list = review
    text_list = data.split(' ')
    text_list_temp = []

    for index in range(len(text_list)):
        if len(text_list[index]) >= 3:
            text_list[index] = ' '.join(text_list[index].split())
            text_list_temp.append(text_list[index])
    return text_list_temp 

def removeStopword(data):
    stopwords = open('D:\BAHAN SKRIPSI\program_skripsi\data\kamus\kamus_stopword_baru.csv', 'r').read().split()
    review_stop = []
    filteredtext = [word for word in data if word not in stopwords]
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
def ganti_negasi(data):
  w_splited = data.split(' ')
  if 'tidak' in w_splited:
     index_negasi = w_splited.index('tidak')
     for i,k in enumerate(w_splited):
       if k in kamus_negasi and w_splited[i-1] == 'tidak':
         w_splited[i] = kamus_negasi[k]

  return ' '.join(w_splited)

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def stemming(data):
    data = data.lower()
    data = stemmer.stem(data)
    return data

def tokenize(data):
    data = nltk.tokenize.word_tokenize(str(data))
    return data


hasil_case_folding = []
for i in range(len(data)):
  hasil_case_folding.append(case_folding(data[i]))


hasil_cleansing = []
for i in range(len(hasil_case_folding)):
  hasil_cleansing.append(hasil_case_folding(data[i]))
str_cleansing = str(hasil_cleansing)

hasil_normalisasi = []
for i in range(len(hasil_cleansing)):
  hasil_normalisasi.append(formalize_slang_word(hasil_cleansing[i]))
str_formalize_slang_word = str(hasil_normalisasi)

hasil_removed_char = []
for i in range(len(hasil_normalisasi)):
  hasil_removed_char.append(remove_unused_character(hasil_normalisasi[i]))
str_remove_unused_character = str(hasil_removed_char)


hasil_stopword = []
for i in range(len(hasil_removed_char)):
  hasil_stopword.append(removeStopword(hasil_removed_char[i]))
str_removeStopword = str(hasil_stopword)


hasil_negasi = []
for i in range(len(hasil_stopword)):
  hasil_negasi.append(ganti_negasi(hasil_stopword[i]))
str_ganti_negasi = str(hasil_negasi)


hasil_stemming = []
for i in range(len(hasil_negasi)):
  hasil_stemming.append(stemming(hasil_negasi[i]))
str_stemming = str(hasil_stemming)

hasil_tokenize = []
for i in range(len(hasil_stemming)):
  hasil_tokenize .append(tokenize (hasil_stemming[i]))
str_tokenize  = str(hasil_tokenize[0])

# preprocessing = [' '.join(sen) for sen in hasil_tokenize]
sequences = tokenizer.texts_to_sequences(str_tokenize)
word_index = tokenizer.word_index
str_sequences = str(sequences)

word_index = tokenizer.word_index

x_test = pad_sequences(sequences, maxlen=100)
print('x_test :', x_test)

prediksi = model.predict(x_test, batch_size=1, verbose=0)
probabilitas = "POSITIF : " + str(prediksi[0][0]) + "  |  NEGATIF : " + str(prediksi[0][1]) 
probabilitas_pembulatan = "POSITIF : " + str(round(prediksi[0][0])) + "  |  NEGATIF : " + str(round(prediksi[0][1]))

class_category = ['Positif', 'Negatif']
for i in range(prediksi.shape[0]):
 klasifikasi = class_category[prediksi[i].argmax()]


hasil = {
	'casefolding': hasil_case_folding,
	'cleansing': hasil_cleansing,
	'normalisasi': hasil_normalisasi,
    'remove_char': hasil_removed_char,
	'stopwords': hasil_stopword,
	'negation_handling': hasil_negasi,
    'stemming': hasil_stemming,
    'tokenisasi': str_tokenize,
    'prob_positif': probabilitas,
    'proba_negatif': probabilitas_pembulatan,
	'klasifikasi': klasifikasi,
    'vektor': str_sequences
}
hasil = json.dumps(hasil)
print(hasil)

































# def prepData(text):
    # Convert to array
# textDataArray = [text]
#     # Convert into list with word ids
# sequences = tokenizer.texts_to_sequences(textDataArray)
# str_sequences = str(sequences)
# word_index = tokenizer.word_index
# x_test = pad_sequences(sequences, maxlen=100, padding='pre')

# prediksi = model.predict(x_test, batch_size=1, verbose=0)
# probabilitas = "POSITIVE : " + str(prediksi[1][0]) + "  |  NEGATIVE : " + str(prediksi[0][1]) 
# probabilitas_pembulatan = "POSITIVE : " + str(round(prediksi[1][0])) + "  |  NEGATIVE : " + str(round(prediksi[0][1]))

# class_category = ['Positif', 'Negatif']
# for i in range(prediksi.shape[0]):
# klasifikasi = class_category[prediksi[i].argmax()]

    # return sequences


#TAHAP PREPROCESSING
# def prepData(text):
#     # Convert to array
#     textDataArray = [text]
#     # Convert into list with word ids
#     Features = tokenizer.texts_to_sequences(textDataArray)
#     Features = pad_sequences(Features, 100, padding='pre')
#     return Features

 
# def pred(text):
#   test = [text]
#   review_tokens = tokenizer.texts_to_sequences(test)
#   review_tokens_pad = pad_sequences(review_tokens, maxlen=100, padding="pre")
#   sentiment = model.predict(review_tokens_pad)
#   print(sentiment)
#   if sentiment[0] > 0.5:
#     sentiment_str = "Positif:" + "{0:.2%}".format(float(sentiment[0]))
#   else:
#     sentiment_str = "Negatif :" + "{0:.2%}".format(float(sentiment[0]))
#   return sentiment_str