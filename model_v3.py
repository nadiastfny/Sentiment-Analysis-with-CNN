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
from sklearn.metrics import precision_score, recall_score, f1_score
import re, os, pickle, gensim, string, csv, nltk
from sklearn.metrics import accuracy_score, plot_confusion_matrix, classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")
from gensim.models.word2vec import Word2Vec

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
import keras.regularizers 

conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='sentimen'
)
cur = conn.cursor()

def ekstrak_train():
    cur = conn.cursor()
    cur.execute("SELECT id_train,review,label FROM tbl_train")
    with open("D:\BAHAN SKRIPSI\program_skripsi\data\data_train.csv", "w", encoding='utf-8', newline='') as csv_file:  # Python 3 version    
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cur.description]) # write headers
        csv_writer.writerows(cur)
    print('Done berhasil ekstrak data train')
    cur.close()

def ekstrak_test():
    cur = conn.cursor()
    cur.execute("SELECT id_tes,review,label FROM tbl_tes")
    with open("D:\BAHAN SKRIPSI\program_skripsi\data\data_test.csv", "w", encoding='utf-8', newline='') as csv_file:  # Python 3 version    
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cur.description]) # write headers
        csv_writer.writerows(cur)
    print('Done berhasil ekstrak data test')
    cur.close()

def model_v3(kernel):
    print('Proses model')
    acc=[]
    prec=[]
    rec=[]

    #PARAMETER
    FILTERS_SIZE = 50
    ker = int(kernel)
    KERNEL_SIZE = int(ker)

    # Define embeddings dimensions (columns in matrix fed into CNN and nodes in hidden layer of built-in keras function)
    EMBEDDING_DIM = 100
    MAX_SEQUENCE_LENGTH = 50
    # Hyperparameters for model tuning
    LEARNING_RATE = 0.0001
    BATCH_SIZE = 128
    EPOCHS = 50  
    
    ekstrak_train()
    data = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data_train.csv')
    data.info()
    
    ekstrak_test()
    data_tes = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data_test.csv')
    data_tes.info()
    
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

    #PROSES PREPROCESSING UNTUK DATA TRAINING
    print('Start Preprocessing train ........')
    data['Text_casefolding'] = data['review'].apply(lambda x: case_folding(x))
    print('Finish case folding.........')
    data['Text_cleansing'] = data['Text_casefolding'].apply(lambda x: cleansing(x))
    print('Finish cleansing.........')
    data['Text_slang'] = data['Text_cleansing'].apply(lambda x: formalize_slang_word(x))
    print('Finish slang.........')
    data['stemming'] = data['Text_slang'].apply(lambda x: stemming(x))
    print('Finish stemming.........')
    data['Text_char'] = data['stemming'].apply(lambda x: remove_unused_character(x))
    print('Finish text char.........')
    data['Text_stopword'] = data['Text_char'].apply(lambda x: removeStopword(x))
    print('Finish text stopword.........')
    data['negasi'] = data['Text_stopword'].apply(lambda x: ganti_negasi(x))
    print('Finish negasi.........')
    data['token'] = data['negasi'].apply(lambda x: tokenize(x))
    print('Finish token train.........')

    result = [' '.join(sen) for sen in data['token']]
    data['Text_Final'] = result
    data['tokens'] = data['token']
    data = data[['Text_Final', 'tokens', 'label']]
    data.to_csv('D:\BAHAN SKRIPSI\program_skripsi\data\hasil preprocessing data train.csv')
    print('Finish Preprocessing Train ........')

    data.dropna(inplace=True)
    data.info()
    print(data['label'].value_counts() )
    #PROSES PREPROCESSING UNTUK DATA TESTING

    print('Start preprocessing test.........')
    data_tes['Text_casefolding'] = data_tes['review'].apply(lambda x: case_folding(x))
    print('Finish case folding.........')
    data_tes['Text_cleansing'] = data_tes['Text_casefolding'].apply(lambda x: cleansing(x))
    print('Finish cleansing.........')
    data_tes['Text_slang'] = data_tes['Text_cleansing'].apply(lambda x: formalize_slang_word(x))
    print('Finish slang.........')
    data_tes['stemming'] = data_tes['Text_slang'].apply(lambda x: stemming(x))
    print('Finish stemming.........')
    data_tes['Text_char'] = data_tes['stemming'].apply(lambda x: remove_unused_character(x))
    print('Finish text char.........')
    data_tes['Text_stopword'] = data_tes['Text_char'].apply(lambda x: removeStopword(x))
    print('Finish text stopword.........')
    data_tes['negasi'] = data_tes['Text_stopword'].apply(lambda x: ganti_negasi(x))
    print('Finish negasi.........')
    data_tes['token'] = data_tes['negasi'].apply(lambda x: tokenize(x))
    print('Finish token test.........')

    result_tes = [' '.join(sen) for sen in data_tes['token']]
    data_tes['Text_Final'] = result_tes
    data_tes['tokens'] = data_tes['token']

    data_tes = data_tes[['Text_Final', 'tokens', 'label']]

    data_tes.to_csv('D:\BAHAN SKRIPSI\program_skripsi\data\hasil preprocessing data test.csv')
    print('Finish preprocessing test.........')
    
    data_tes.info()
    print(data_tes['label'].value_counts() )
    
    jmlh_latih = len(data)
    jmlh_uji = len(data_tes)
    total = (jmlh_latih+jmlh_uji)

    print('Start word2vec.........')
    modelWV = Word2Vec(data['tokens'], vector_size=EMBEDDING_DIM, window=3, min_count=0, sg=1, seed=2)
    modelWV.wv.save_word2vec_format('D:\BAHAN SKRIPSI\program_skripsi\models\saved_word2vec_uni.txt',binary=False)
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(data['Text_Final'].tolist())
    train_word_index = tokenizer.word_index

    training_sequences = tokenizer.texts_to_sequences(data["Text_Final"].tolist())
    train_cnn_data = pad_sequences(training_sequences, maxlen=MAX_SEQUENCE_LENGTH)

    test_sequences = tokenizer.texts_to_sequences(data_tes["Text_Final"].tolist())
    test_cnn_data = pad_sequences(test_sequences, maxlen=MAX_SEQUENCE_LENGTH)

    embeddings_index = dict()
    f = open('D:\BAHAN SKRIPSI\program_skripsi\models\saved_word2vec_uni.txt')
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

    y_train = data.label
    x_train = train_cnn_data

    model = Sequential()
    model.add(Embedding(input_dim=len(train_word_index)+1, output_dim=EMBEDDING_DIM, weights=[embedding_matrix], input_length=MAX_SEQUENCE_LENGTH, trainable=True))
    model.add(Conv1D(FILTERS_SIZE, KERNEL_SIZE, strides=1, activation='relu', padding='same' , kernel_regularizer=keras.regularizers.l2(0.01)))
    model.add(MaxPooling1D(2))
    model.add(Flatten())
    model.add(Dense(8, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=Adam(LEARNING_RATE), metrics=['acc'])

    num_epochs = 50
    batch_size = 128

    es_callback =EarlyStopping(monitor='val_loss', patience=10, verbose=1)
    print('Start training model........')

    hist = model.fit(x_train, y_train, epochs=num_epochs, validation_split=0.1, shuffle=True , batch_size=batch_size, callbacks=[es_callback])
    
    x_test = test_cnn_data
    y_test = data_tes.label

    pred = model.evaluate(x_test, y_test, batch_size=8, verbose=1)
    pred    
    
    with open('D:\BAHAN SKRIPSI\program_skripsi\models\Saved_Tokenize_tri.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    model_json = model.to_json()
    with open('D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_tri.json','w') as json_file:
        json_file.write(model_json)

    model.save_weights("D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_tri.h5")
    print("Model saved to disk")
    
    # Load tokenizer for preprocessing
    with open('D:\BAHAN SKRIPSI\program_skripsi\models\Saved_Tokenize_tri.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # Load pre-trained model into memory
    json_file = open('D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_tri.json','r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # Load weights into new model
    loaded_model.load_weights("D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_tri.h5")

    predictions = loaded_model.predict(test_cnn_data, batch_size=8, verbose=1)
    # predictions

    labels = [1,0]
    threshold = 0.5

    prediction_labels=[]
    for p in predictions:
        prediction_labels.append(labels[np.argmax(p)])

    output = (predictions>0.5).astype(int)
    # print(output[2])

    conf = pd.DataFrame(data=confusion_matrix(y_test, output, labels=labels), columns=labels, index=labels)
    print(conf)
    
    accuracy = (conf[0][0]+conf[1][1]) / (conf[0][0]+conf[0][1]+conf[1][0]+conf[1][1])
    acc = int(accuracy)
    print ('Accuracy :', acc)

    prec = (precision_score(y_test, output), conf[0][0]/(conf[0][0] + conf[1][0]) )
    print('Precision :', prec)

    rec = (recall_score(y_test, output), conf[0][0]/(conf[0][0]+conf[0][1]) )
    print('Recall :', rec)

    spec = conf[1][1]/(conf[1][1]+conf[1][0])
    print('Specifity :', spec)

    error = (conf[0][1]+conf[1][0]) / (conf[0][0]+conf[0][1]+conf[1][0]+conf[1][1])
    print('Error :', error)

    analisis=pd.DataFrame()
    analisis['Kalimat Uji']=data_tes['Text_Final']
    analisis['Prediksi']= output

    predik=[]
    for i in range(0,jmlh_uji):
        predik.append(predictions[i])

    analisis['Nilai_Probabilitas']=predik
    analisis['label_actual']=data_tes.label

    data = pd.DataFrame({
        'text_uji':analisis['Kalimat Uji'],
        'label_aktual': analisis['label_actual'],
        'prediksi':analisis['Prediksi'],
        'probabilitas' : analisis['Nilai_Probabilitas']
    })
    data.to_csv('D:\BAHAN SKRIPSI\program_skripsi\data\hasil_prediksi_tri.csv', index=False, header=False, sep="\t")

    # =====INSERT HASIL UJI KE DATABASE=====
    # def insert_db():
    #   col_names = ['text_uji','label_aktual', 'prediksi', 'probabilitas']
    #   csvData = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\hasil_prediksi_tri.csv',  names=col_names, header=None,sep="\t")
    #   for i,row in csvData.iterrows():
    #     sql = "INSERT INTO hasil_uji (id_tesmodel, text_uji,label_aktual,prediksi,probabilitas) VALUES (%s, %s, %s, %s, %s) "
    #     value = ('', row['text_uji'],row['label_aktual'],row['prediksi'],row['probabilitas'])
    #     cur.execute(sql, value)
    #     conn.commit()

    # print("Start insert hasil prediksi sentimen model to database...")
    # insert_db()
    # print("BERHASIL INSERT HASIL PREDIKSI KE DATABASE!!!")

    
    def insert_database(total, jmlh_latih, jmlh_uji, size, filter, kernel, akurasi):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO pengujian (id_uji, date, total_dataset, data_latih, data_tes, size_embedding, filter, kernel, akurasi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",('', formatted_date, total, jmlh_latih, jmlh_uji, size, filter, kernel, acc))
        conn.commit()

    insert_database(total, jmlh_latih, jmlh_uji, EMBEDDING_DIM, FILTERS_SIZE, KERNEL_SIZE, acc)

    print("BERHASIL SAVE HASIL PENGUJIAN VERSI 3 KE DATABASE!!!")


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


