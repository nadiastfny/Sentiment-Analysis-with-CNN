from flask import Flask, Markup, render_template, sessions, url_for, request, redirect, flash, jsonify, session
from flask.json import JSONEncoder
from keras_preprocessing.text import Tokenizer
from nltk import jsontags, text
from werkzeug.utils import redirect, secure_filename 
import pandas as pd
import pymysql, os, csv, pickle, re, nltk, mysql.connector, MySQLdb.cursors, json
from datetime import datetime
from flask_mysqldb import MySQL
import numpy as np
from bs4 import BeautifulSoup
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing import text, sequence
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from preprocessing import preprocessing_text, case_folding, cleansing,formalize_slang_word, removeStopword, ganti_negasi, remove_unused_character, stemming, tokenize
from model_v2 import model_v2
from model_v3 import model_v3
from keras.models import model_from_json
from ekstrak import split
from model_db import execute_query

app = Flask(__name__)
 
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'anything'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sentimen'
mysql = MySQL(app)

#uploud dataset
ALLOWED_EXTENSION = set(['csv', 'xls', 'xlsx', 'txt'])
app.config['UPLOAD_FOLDER'] = 'data'

with open('D:\BAHAN SKRIPSI\program_skripsi\models\Saved_Tokenize_tri.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

json_file = open('D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_tri.json', 'r')
model_json = json_file.read()
model = model_from_json(model_json)
model.load_weights("D:\BAHAN SKRIPSI\program_skripsi\models\saved_model_sentimen_tri.h5")

MAX_SEQUENCE_LENGTH = 50
EMBEDDING_DIM = 100

ROWS_PER_PAGE = 10

@app.route("/", methods=['GET', 'POST'])
def index():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('pageLogin'))

@app.route("/page_login")
def pageLogin():
    return render_template('login.html')

@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # cur = mysql.connection.cursor()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cur.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id_admin'] = account['id_admin']
            session['username'] = account['username']
 
            flash("Login Success!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password!", "warning")
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id_admin', None)
   session.pop('username', None)
   flash('You were logged out')
   # Redirect to login page
   return redirect(url_for('login'))

@app.route("/page_data_latih")
def pageLatih():
    return render_template('page_data_latih.php')

@app.route("/page_data_uji")
def pageUji():
    return render_template('page_data_uji.php')

@app.route("/page_klasifikasi")
def pageKlasifikasi():
    return render_template('page_klasifikasi.php')

@app.route("/website")
def pageUser():
    # return redirect(url_for('cekReview'))
    return render_template('website_fd.php')

@app.route("/ujitext", methods=['GET','POST'])
def ujiText():
    if request.method=='POST':
        text = request.form['text']
        review = request.form.get('text')   
        try:           
            rvw = [review]
            rvw = np.array(rvw)
            texts = [] 
            text = re.sub(r"'", r"\' ", text)
           
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

            cfolding = case_folding(text)
            clean = cleansing(cfolding)
            normalisasi= formalize_slang_word(clean)
            stem = stemming(normalisasi)
            unused_char = remove_unused_character(stem)
            stopword = removeStopword(unused_char)
            negasi = ganti_negasi(stopword)
            tokenisasi = tokenize(negasi)
            
            for i in range(rvw.shape[0]):
                teks = BeautifulSoup(rvw[i])
                texts.append(preprocessing_text(str(teks.get_text().encode())))
            
            sequences = tokenizer.texts_to_sequences(texts)
            word_index = tokenizer.word_index
      
            test_cnn_data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
            x_test = test_cnn_data
            print('x_test :', x_test)

            prediksi_sentimen = model.predict(x_test, batch_size=1, verbose=2)

            class_sentimen = ['POSITIF', 'NEGATIF']
            threshold=0.5
            
            if prediksi_sentimen > threshold:
                sentiment_str = "{0:.2%}".format(float(prediksi_sentimen))
                hasil_sentimen = class_sentimen[0]
            else:
                sentiment_str = "{0:.2%}".format(float(prediksi_sentimen))
                hasil_sentimen = class_sentimen[1]

            cur = mysql.connection.cursor()
            unused_chars = ' '.join(map(str, unused_char))
            # tokenisasis = ' '.join(map(str, tokenisasi))
            cur.execute("INSERT INTO cek_ulasan (id_cek, date, ulasan, casefolding, cleansing, normalisasi, remove_char, stopwords, negation_handling, stemming, probabilitas, sentimen) VALUES ('','"+formatted_date+"','"+text+"', '"+cfolding+"', '"+clean+"', '"+normalisasi+"', '"+unused_chars+"', '"+stopword+"', '"+negasi+"', '"+stem+"', '"+sentiment_str+"', '"+hasil_sentimen+"')")
            
            mysql.connection.commit()
            print("BERHASIL INSERT TO DATABASE")

            return render_template('page_hasil_klasifikasi.php',text=text, cfolding=cfolding, 
                                    clean=clean, normalisasi=normalisasi, stopword=stopword, negasi=negasi, 
                                    unused_char=unused_char, stem=stem, tokenisasi=tokenisasi, 
                                    hasil_sentimen=hasil_sentimen, sentiment_str=sentiment_str) 
        except ValueError:
            return "LOGIC ADA YANG SALAH !!! "
    pass

@app.route("/cekreview", methods=['GET','POST'])
def cekReview():
    if request.method=='POST':
        text = request.form['text']
        review = request.form.get('text')   
        try:
            rvw = [review]
            rvw = np.array(rvw)
            texts = [] 
            text = re.sub(r"'", r"\' ", text)
           
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            
            cfolding = case_folding(text)
            clean = cleansing(cfolding)
            normalisasi= formalize_slang_word(clean)
            stem = stemming(normalisasi)
            unused_char = remove_unused_character(stem)
            stopword = removeStopword(unused_char)
            negasi = ganti_negasi(stopword)
            tokenisasi = tokenize(negasi)

            for i in range(rvw.shape[0]):
                teks = BeautifulSoup(rvw[i])
                texts.append(preprocessing_text(str(teks.get_text().encode())))
            
            sequences = tokenizer.texts_to_sequences(texts)
            word_index = tokenizer.word_index
      
            test_cnn_data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
            x_test = test_cnn_data
            print('x_test :', x_test)

            prediksi_sentimen = model.predict(x_test, batch_size=1, verbose=2)

            threshold=0.5
            class_sentimen = ['POSITIF', 'NEGATIF']
 
            if prediksi_sentimen > threshold:
                hasil_sentimen = class_sentimen[0]
                sentiment_str = "{0:.2%}".format(float(prediksi_sentimen))
                teks="POSITIVE😊😊"
            else:
                hasil_sentimen = class_sentimen[1]
                sentiment_str = "{0:.2%}".format(float(prediksi_sentimen))
                teks="NEGATIVE☹️☹️"

            cur = mysql.connection.cursor()
            unused_chars = ' '.join(map(str, unused_char))
            
            cur.execute("INSERT INTO cek_ulasan (id_cek, date, ulasan,  casefolding, cleansing, normalisasi, remove_char, stopwords, negation_handling, stemming, probabilitas, sentimen) VALUES ('','"+formatted_date+"','"+text+"', '"+cfolding+"', '"+clean+"', '"+normalisasi+"', '"+unused_chars+"', '"+stopword+"', '"+negasi+"', '"+stem+"', '"+sentiment_str+"', '"+hasil_sentimen+"')")          
            mysql.connection.commit()
            print("BERHASIL INSERT TO DATABASE")

            return render_template('website_fd.php', hasil_sentimen=teks) 
          
        except ValueError:
            return "cek lagi!"
    # pass
    else:
         return render_template('website_fd.php')
        
@app.route('/add_admin', methods=['GET', 'POST'])
def insertAdmin():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO admin (username, password) VALUES (%s,%s)",(username,password,))
    mysql.connection.commit()
    flash("Add data admin success!", "success")
    return redirect(url_for('dataAdmin'))

@app.route('/data_admin', methods=['GET', 'POST'])
def dataAdmin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin")
    rv = cur.fetchall()
    cur.close()
    return render_template('page_data_admin.php', data=rv)

@app.route('/updateAdmin', methods=['POST'])
def updateAdmin():
    id = request.form['id_admin']
    user = request.form['username']
    pwd = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE admin SET username=%s, password=%s WHERE id_admin=%s ", (user,pwd,id,) )
    mysql.connection.commit()
    flash("Update data admin success!", "success")
    return redirect(url_for('dataAdmin')) 

# string:id_admin
@app.route('/hapus_admin/<id_admin>', methods=['GET'])
def hapusAdmin(id_admin):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM admin WHERE id_admin=%s", [id_admin])
    mysql.connection.commit()
    flash("Delete data admin success!", "danger")
    return redirect(url_for('dataAdmin'))

@app.route('/data_cek', methods=['GET', 'POST'])
def dataCek():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cek_ulasan ORDER BY id_cek DESC")
    rv = cur.fetchall()
    cur.close()
    return render_template('page_data_cek.php', data=rv)

@app.route('/cek', methods=['GET', 'POST'])
def detailCek():
    id = request.form['id_cek']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cek_ulasan WHERE id_cek='"+id+"' ")
    rv = cur.fetchall()
    cur.close()
    return redirect(url_for('dataCek'))

@app.route('/hapus_cek/<id_cek>', methods=['GET'])
def hapusCek(id_cek):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cek_ulasan WHERE id_cek=%s", [id_cek])
    mysql.connection.commit()
    return redirect(url_for('dataCek'))

@app.route('/data_pengujian', methods=['GET', 'POST'])
def dataPengujian():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pengujian ORDER BY id_uji DESC")
    rv = cur.fetchall()
    cur.close()
    return render_template('page_data_pengujian.php', data=rv)

@app.route('/hapus_pengujian/<id>', methods=['GET'])
def hapusPengujian(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pengujian WHERE id_uji=%s", [id])
    mysql.connection.commit()
    return redirect(url_for('dataPengujian'))

@app.route('/data_hasil_uji', methods=['GET', 'POST'])
def dataHasilUji():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hasil_uji ORDER BY id_tesmodel DESC")
    rv = cur.fetchall()
    cur.close()
    return render_template('page_data_hasil_prediksi.php', data=rv)

@app.route('/master_data', methods=['GET', 'POST'])
def dataMaster():
    cur = mysql.connection.cursor()
    try:
        if request.method == 'POST':
            draw = request.form['draw'] 
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print('draw:',draw)
            print('row:',row)
            print('row per page:',rowperpage)
            print('search:',searchValue)
            
            cur.execute("select count(review) from tbl_master")
            sql=cur.fetchone()
            print(sql)

            totalRecords = sql
            print('c')
            print('records:', totalRecords) 
            cur.execute("select * from tbl_master limit %s, %s", (row, rowperpage))
            employeelist = cur.fetchall()
            data = []
            
            for row in employeelist:
                data.append({
                    'id' : row[0],
                    # 'id' : row[1],
                    'review' : row[1],
                    'label' : row[2]
                })
 
            response = {
                "draw" : draw,
                "iTotalRecords" : totalRecords,
                # "iTotalDisplayRecords" : totalRecordwithFilter,
                "aaData" : data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cur.close() 
    return render_template('page_data_master.php')

@app.route('/add_data', methods=['GET', 'POST'])
def addMaster():
    text = request.form['review']
    label = request.form['label']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tbl_master (review, label) VALUES (%s,%s)",(text,label,))
    mysql.connection.commit()
    return redirect(url_for('dataMaster'))

@app.route('/datalatih', methods=['GET', 'POST'])
def dataLatih():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_train ORDER BY id_train DESC")
    rv = cur.fetchall()
    cur.close()

    return render_template('page_data_latih.php', data=rv)

@app.route('/editlatih', methods=['POST'])
def editLatih():
    id_train = request.form['id_train']
    id = request.form['id']
    review = request.form['review']
    label = request.form['label']
    cur = mysql.connection.cursor()
    cur.execute( "UPDATE tbl_train SET review=%s, label=%s WHERE id_train=%s ", (review,label,id_train,))
    cur.execute("UPDATE tbl_master SET review=%s, label=%s WHERE id=%s ", (review,label,id,))
    mysql.connection.commit()
    flash("Update data training success!", "success")
    return redirect(url_for('dataLatih')) 

@app.route('/hapuslatih/<id_tr>,<id>', methods=['GET'])
def hapusLatih(id_tr,id):
    # id = request.args.get("id")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbl_train WHERE id_train=%s", [id_tr])
    cur.execute("DELETE FROM tbl_master WHERE id=%s", [id])
    mysql.connection.commit()
    flash("Delete data training success!", "danger")
    return redirect(url_for('dataLatih'))

@app.route('/add_latih', methods=['GET', 'POST'])
def addLatih():
    text = request.form['review']
    label = request.form['label']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tbl_master (review,label) VALUES (%s,%s)",(text,label,))  #insert ke db master dulu
    get_id = cur.lastrowid
    id = str(get_id)
    print(id) 
    cur.execute("INSERT INTO tbl_train (id,review,label) SELECT id,review,label FROM tbl_master WHERE id='"+id+"' ")   #insert ke db train
    mysql.connection.commit()
    flash("Add data training success!", "success")
    return redirect(url_for('dataLatih'))

@app.route('/datauji', methods=['GET', 'POST'])
def dataUji():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_tes ORDER BY id_tes DESC")
    rv = cur.fetchall()
    cur.close()
    return render_template('page_data_uji.php', data=rv)

@app.route('/edituji', methods=['POST'])
def editUji():
    id_tes = request.form['id_tes']
    id = request.form['id']
    review = request.form['review']
    label = request.form['label']
    cur = mysql.connection.cursor()
    cur.execute( "UPDATE tbl_tes SET review=%s, label=%s WHERE id_tes=%s ", (review,label,id_tes,))
    cur.execute("UPDATE tbl_master SET review=%s, label=%s WHERE id=%s ", (review,label,id,))
    mysql.connection.commit()
    flash("Update data testing success!", "success")
    return redirect(url_for('dataUji')) 

@app.route('/hapusuji/<id_ts>,<id>', methods=['GET'])
def hapusUji(id_ts,id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbl_tes WHERE id_tes=%s", [id_ts])
    cur.execute("DELETE FROM tbl_master WHERE id=%s", [id])
    mysql.connection.commit()
    flash("Delete data testing success!", "danger")
    return redirect(url_for('dataUji'))

@app.route('/add_uji', methods=['GET', 'POST'])
def addUji():
    text = request.form['review']
    label = request.form['label']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tbl_master (review,label) VALUES (%s,%s)",(text,label,))  #insert ke db master dulu
    get_id = cur.lastrowid
    id = str(get_id)
    print(id) 
    cur.execute("INSERT INTO tbl_tes (id,review,label) SELECT id,review,label FROM tbl_master WHERE id='"+id+"' ")   #insert ke db train
    mysql.connection.commit()
    flash("Add data testing success!", "success")
    return redirect(url_for('dataUji'))

@app.route('/model_versi_2', methods=['GET','POST'])
def modelV2():
    kernel = request.form['kernel']
    print("model proses")
    model_v2(kernel)
    return redirect(url_for('dataPengujian'))

@app.route('/model_versi_3', methods=['GET','POST'])
def modelV3():
    kernel = request.form['kernel']
    print("model proses")
    model_v3(kernel)
    return redirect(url_for('dataPengujian'))

@app.route('/ekstrak_data', methods=['GET', 'POST'])
def ekstrak():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_master")
    with open("D:\BAHAN SKRIPSI\program_skripsi\data\data_from_db.csv", "w", encoding='utf-8', newline='') as csv_file:  # Python 3 version    
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cur.description]) # write headers
        csv_writer.writerows(cur)
    print('Done')
    cur.close()
    return redirect(url_for('dataMaster'))

@app.route('/splitdata')
def splitData():
    split()
    return redirect(url_for('dataLatih'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/import_data', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        file = request.files['file']

        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)

        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            parseCSV(file_path)   #ini kalau mau dimasukin ke database aja
            print("save data to db")
            # file.save(file_path)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))            
            return redirect(url_for('dataMaster'))
            
    return redirect(url_for('dataMaster'))

#import tabel tes
def parseCSV(filePath):
      # CVS Column Names
      col_names = ['review', 'label']
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvData.iterrows():
            cur = mysql.connection.cursor()
            sql = "INSERT INTO tbl_master (review, label) VALUES (%s, %s)"
            value = (row['review'], row['label'])
            cur.execute(sql, value)
            mysql.connection.commit()

if __name__ == "__main__":
    app.run(debug=True)
