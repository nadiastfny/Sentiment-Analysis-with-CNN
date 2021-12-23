from numpy.lib.arraysetops import setxor1d
import pandas as pd
from flask_mysqldb import MySQL
from flask import Flask, render_template, sessions, url_for, request, redirect, flash, jsonify
import mysql.connector
import MySQLdb.cursors
from flask import session
from model_v2 import ekstrak
from sklearn.model_selection import train_test_split
import re, os, pickle, gensim, string, csv, nltk

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sentimen"
)

cur = mydb.cursor()

def split():
  ekstrak() 
  data = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data_from_db.csv')
  
  data_train, data_test = train_test_split(data, test_size=0.1, random_state=42)

  text_train = str(data_train['review'])
  text_train = re.sub(r"'", r"\' ", text_train)
  text_train = data_train['review']

  text_tes = str(data_test['review'])
  text_tes = re.sub(r"'", r"\' ", text_tes)
  text_tes = data_test['review']

  print(type(text_train))
  
  data_latih = pd.DataFrame({
        'id' : data_train['id'],
        'review':data_train['review'],
        # 'review':text_train,
        'label': data_train['label']
    })

  data_uji = pd.DataFrame({
        'id' : data_test['id'],
        'review':data_test['review'],
        # 'review':text_tes,
        'label': data_test['label']
    })

  data_latih.to_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data_train.csv', index=False, sep=',')
  data_uji.to_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data_test.csv', index=False, sep=',')
  print("Start proses insert data train .....")
  insert_train()
  print("BERHASIL SAVE DATA TRAIN")
  print("Start proses insert data test .....")
  insert_test()
  print("BERHASIL SAVE DATA TEST")


# =====INSERT DATA TRAIN KE DATABASE=====
def insert_train():
  col_names = ['id','review','label']
  csvData = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data_train.csv',  names=col_names, header=None,sep=",")
  for i,row in csvData.iterrows():
    id = row["id"]
    review = row["review"]
    label = row["label"]
    sql = "INSERT INTO tbl_train (id,review, label) SELECT id,review,label FROM tbl_master WHERE id='"+id+"'"
    cur.execute(sql)
    mydb.commit()
  

# =====INSERT DATA TEST KE DATABASE=====
def insert_test():
  col_names = ['id','review','label']
  csvData = pd.read_csv('D:\BAHAN SKRIPSI\program_skripsi\data\data_test.csv',  names=col_names, header=None,sep=",")
  for i,row in csvData.iterrows():
    id = row["id"]
    review = row["review"]
    label = row["label"]
    sql = "INSERT INTO tbl_tes (id,review, label) SELECT id,review,label FROM tbl_master WHERE id='"+id+"'"
    cur.execute(sql)
    mydb.commit()