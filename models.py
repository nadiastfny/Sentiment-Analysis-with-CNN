import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import text, sequence
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Reshape, Flatten, concatenate, Input, Conv1D, GlobalMaxPooling1D, Embedding
from tensorflow.keras.layers import Conv1D, MaxPooling1D, GlobalMaxPooling1D
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing import text, sequence
from sklearn.feature_extraction.text import CountVectorizer
from nltk.probability import FreqDist
import re, os, pickle, gensim, string, csv, nltk
from sklearn.metrics import accuracy_score, plot_confusion_matrix, classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
# %matplotlib inline
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from keras.models import Model
from gensim import models
from keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix
from keras.callbacks import ModelCheckpoint
import keras.models
from keras.models import model_from_json
import mysql.connector
import MySQLdb.cursors
from flask import session
from datetime import datetime
from app import ekstrak 
acc=[]
presisi=[]
recal=[]

#PARAMETER
FILTERS_SIZE = 128
KERNEL_SIZE = 3

# Define embeddings dimensions (columns in matrix fed into CNN and nodes in hidden layer of built-in keras function)
EMBEDDING_DIM = 300
MAX_SEQUENCE_LENGTH =100
MAX_FEATURE = 5000
# Hyperparameters for model tuning
LEARNING_RATE = 0.001
BATCH_SIZE = 32
EPOCHS = 7

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='sentimen'
)
cur = conn.cursor()


ekstrak()
data = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data_from_db.csv')

pos = []
neg = []
for l in data.label:
  if l == 1:
    pos.append(1)
    neg.append(0)
  elif l == 0:
    pos.append(0)
    neg.append(1)

data['Pos']= pos
data['Neg']= neg

def case_folding(tokens): 
    return tokens.lower()  

def cleansing(review):
    review = re.sub(r'[^\x00-\x7f]', r'', review)
    review = re.sub(r'(\\u[0-9A-Fa-f]+)', r'', review)
    review = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", review)
    review = re.sub(r'\\u\w\w\w\w', '', review)
    # Remove simbol, angka dan karakter aneh
    review = re.sub(r"[.,:;+!\-_<^/=?\"'\(\)\d\*]", " ", review)
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
    token = nltk.tokenize.word_tokenize(str(tokens))
    return token

data['Text_casefolding'] = data['review'].apply(lambda x: case_folding(x))

data['Text_cleansing'] = data['Text_casefolding'].apply(lambda x: cleansing(x))

data['Text_slang'] = data['Text_cleansing'].apply(lambda x: formalize_slang_word(x))
 
data['Text_char'] = data['Text_slang'].apply(lambda x: remove_unused_character(x))

data['Text_stopword'] = data['Text_char'].apply(lambda x: removeStopword(x))

data['negasi'] = data['Text_stopword'].apply(lambda x: ganti_negasi(x))

data['stemming'] = data['negasi'].apply(lambda x: stemming(x))

data['token'] = data['stemming'].apply(lambda x: tokenize(x))

result = [' '.join(sen) for sen in data['token']]
data['Text_Final'] = result
data['tokens'] = data['token']

data = data[['Text_Final', 'tokens', 'label', 'Pos', 'Neg']]

data.to_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data hasil preprocessing.csv')

# x = data['Text_Final']
# y = data['label']


data_train, data_test = train_test_split(data, test_size=0.2, random_state=42)

jmlh_latih = len(data_train)
jmlh_uji = len(data_test)
total = len(data)



modelWV = Word2Vec(data['tokens'], vector_size=EMBEDDING_DIM, window=5, min_count=5, sg=1)
modelWV.wv.save_word2vec_format('D:\BAHAN SKRIPSI\program_skripsi\models\saved_word2vec_v1.txt',binary=False)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(data_train["Text_Final"].tolist())
train_word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(data_train["Text_Final"].tolist())
train_cnn_data = pad_sequences(training_sequences, maxlen=MAX_SEQUENCE_LENGTH)

test_sequences = tokenizer.texts_to_sequences(data_test["Text_Final"].tolist())
test_cnn_data = pad_sequences(test_sequences, maxlen=MAX_SEQUENCE_LENGTH)

embeddings_index = dict()
f = open('D:\BAHAN SKRIPSI\program_skripsi\models\saved_word2vec_v1.txt')
for line in f:
	values = line.split()
	word = values[0]
	coefs = np.asarray(values[1:], dtype='float32')
	embeddings_index[word] = coefs
f.close()

embedding_matrix = np.zeros((len(train_word_index)+1,EMBEDDING_DIM))

for word, index in train_word_index.items():
  embedding_vector = embeddings_index.get(word)
  if embedding_vector is not None:
    embedding_matrix[index] = embedding_vector

label_names = ['Pos', 'Neg']

y_train = data_train[label_names].values
x_train = train_cnn_data

model = Sequential()
model.add(Embedding(input_dim=len(train_word_index)+1, output_dim=EMBEDDING_DIM, weights=[embedding_matrix], input_length=MAX_SEQUENCE_LENGTH,  trainable=True))
model.add(Conv1D(FILTERS_SIZE, KERNEL_SIZE, strides="1", padding="same ", activation='relu'))
model.add(MaxPooling1D(2))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(10, activation='relu'))
model.add(Dense(len(list(label_names)), activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])

num_epochs = 100
batch_size = 32

es_callback =EarlyStopping(monitor='val_loss', patience=10, verbose=1)

hist = model.fit(x_train, y_train, epochs=num_epochs, validation_split=0.1, shuffle=True , batch_size=batch_size,callbacks=[es_callback])

predictions = model.predict(test_cnn_data, batch_size=1, verbose=1)
labels = [1,0]
class_sentimen = ['Positif', 'Negatif']

prediction_labels=[]
for p in predictions:
    prediction_labels.append(labels[np.argmax(p)])
print("akurasi = " + str(sum(data_test.label==prediction_labels)/len(prediction_labels)))

analisis=pd.DataFrame()
analisis['Uji']=data_test['Text_Final']
analisis['Prediksi']=prediction_labels

predikPos=[]
for i in range(0,465):
  predikPos.append(predictions[i][0])

predikNeg=[]
for i in range(0,465):
  predikNeg.append(predictions[i][1])

analisis['Proba Positif']=predikPos
analisis['Proba Negatif']=predikNeg
analisis['label_actual']=data_test.label

data = pd.DataFrame({
    'text_uji':analisis['Uji'],
    'label_aktual': analisis['label_actual'],
    'prediksi':analisis['Prediksi'],
    'prob_pos' : analisis['Proba Positif'],
    'prob_neg' : analisis['Proba Negatif']
})
data.to_csv('D:\BAHAN SKRIPSI\program_skripsi\data\hasil_prediksi_v1.csv', index=False, header=False, sep="\t")

# =====INSERT HASIL UJI KE DATABASE=====
def insert_db():
  col_names = ['text_uji','label_aktual', 'prediksi', 'prob_pos', 'prob_neg']
  csvData = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\hasil_prediksi_v1.csv',  names=col_names, header=None,sep="\t")
  for i,row in csvData.iterrows():
    sql = "INSERT INTO hasil_uji (id_tesmodel, text_uji,label_aktual,prediksi,prob_pos,prob_neg) VALUES (%s, %s, %s, %s, %s, %s) "
    value = ('', row['text_uji'],row['label_aktual'],row['prediksi'],row['prob_pos'],row['prob_neg'])
    cur.execute(sql, value)
    conn.commit()

insert_db()
print("BERHASIL INSERT HASIL PREDIKSI KE DATABASE!!!")

xx=sum(data_test.label==prediction_labels)/len(prediction_labels)

y_test= data_test['label'].values

y_tes=[]
for i in range(0, len(y_test)):
  y_tes.append(y_test[i])

y_pred=[]
for p in predictions:
  y_pred.append(labels[np.argmax(p)])

cf_sentimen = pd.DataFrame(data=confusion_matrix(y_tes, y_pred, labels=labels), columns=labels, index=labels)
print(cf_sentimen)

tps_sentimen = {}
fps_sentimen  = {}
fns_sentimen  = {}
tns_sentimen  = {}
for label in labels:
  tps_sentimen[label] = cf_sentimen.loc[label, label]
  fps_sentimen[label] = cf_sentimen[label].sum() - tps_sentimen[label]
  fns_sentimen[label] = cf_sentimen.loc[label].sum() - tps_sentimen[label]

for label in set(y_tes):
  tns_sentimen[label] = len(y_tes) - (tps_sentimen[label] + fps_sentimen[label] + fns_sentimen[label])

accuracy_global_new_sentimen=sum(tps_sentimen.values())/len(y_tes)
acc.append(accuracy_global_new_sentimen)


tpfp_sentimen = [ai + bi for ai, bi in zip(list(tps_sentimen.values()), list(fps_sentimen.values()))]
precision=[ai / bi if bi>0 else 0 for ai , bi in zip(list(tps_sentimen.values()), tpfp_sentimen)]
precisionSentimen=sum(precision)/2
presisi.append(precisionSentimen)

tpfn_sentimen = [ai + bi for ai, bi in zip(list(tps_sentimen.values()), list(fns_sentimen.values()))]
recall=[ai / bi if bi>0 else 0 for ai, bi in zip(list(tps_sentimen.values()), tpfn_sentimen)]
recallSentimen=sum(recall)/2
recal.append(recallSentimen)

acc = str((sum(acc)/len(acc)))
presisi = str((sum(presisi)/len(presisi)))
recall = str((sum(recal)/len(recal)))

with open('D:\BAHAN SKRIPSI\program_skripsi\models\Saved_Tokenize_v1.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

model_json = model.to_json()
with open('D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_v1.json','w') as json_file:
  json_file.write(model_json)

model.save_weights("D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_v1.h5")
print("Model saved to disk")


def insert_database(total, jmlh_latih, jmlh_uji, size, filter, kernel, akurasi, recall, presisi):
  now = datetime.now()
  formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
  cur.execute("INSERT INTO pengujian (id_uji, date, total_dataset, data_latih, data_tes, size_embedding, filter, kernel, akurasi, recall, presisi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",('', formatted_date, total, jmlh_latih, jmlh_uji, size, filter, kernel, akurasi, recall, presisi))
  conn.commit()


insert_database(total, jmlh_latih, jmlh_uji, EMBEDDING_DIM, FILTERS_SIZE, KERNEL_SIZE, acc, recall, presisi)

print("BERHASIL SAVE HASIL PENGUJIAN KE DATABASE!!!")



# fig2 = plt.figure()
# plt.plot(hist.history['acc'],'r',linewidth=1.0)
# plt.plot(hist.history['val_acc'],'b',linewidth=1.0)
# plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=10)
# plt.xlabel('Epochs ',fontsize=10)
# plt.ylabel('Accuracy',fontsize=10)
# plt.title('Accuracy Model Sentimen',fontsize=13)
# fig2.savefig('D:\BAHAN SKRIPSI\program_skripsi\Plot\acc_sentimen_1.png')
# # plt.show()

# fig1 = plt.figure()
# plt.plot(hist.history['loss'],'r',linewidth=1.0)
# plt.plot(hist.history['val_loss'],'b',linewidth=1.0)
# plt.legend(['Training loss','Validation Loss'],fontsize=10)
# plt.xlabel('Epochs ',fontsize=10)
# plt.ylabel('Loss',fontsize=10)
# plt.title('Loss Model Sentimen',fontsize=13)
# fig1.savefig('D:\BAHAN SKRIPSI\program_skripsi\Plot\loss_sentimen_v1.png')
# # plt.show()


