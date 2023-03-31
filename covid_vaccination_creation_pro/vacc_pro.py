
from flask import Flask, render_template, request

import sqlite3
app = Flask(__name__)


import datetime


connection_obj = sqlite3.connect('vaccination_pro.db')

cursor_obj = connection_obj.cursor()


connection_obj.execute('''CREATE TABLE IF NOT EXISTS AADHAAR_INFO(
    AADHAAR_NO INTEGER PRIMARY KEY,
    NAME TEXT NOT NULL,
    DATE_OF_BIRTH DATE NOT NULL,
    GENDER TEXT NOT NULL,
    ADDRESS TEXT  );''')


print("AADHAAR_INFO Table created successfully")

connection_obj.execute('''CREATE TABLE IF NOT EXISTS VACCINATION_INFO(
    AADHAAR_no INTEGER NOT NULL,
    VACCINATION_DATE DATE,
    DOSE_no INTEGER,
    AGE INTEGER,
    vaccination_site varchar(50),
    FOREIGN KEY (AADHAAR_no) references AADHAAR_INFO (AADHAAR_NO) );''')
 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enter_record', methods=['POST', 'GET'])
def enter_record():
    
        return render_template('new_record.html')
    
@app.route('/add_aadhar', methods=['POST', 'GET'])
def add_aadhar():
     
        return render_template('aadhar.html')
    
@app.route('/add_vaccination', methods=['POST','GET'])
def add_vaccination():
        return render_template('vaccination.html')
    

@app.route('/a_aadhar',methods=['POST', 'GET'])
def a_aadhar():
    
    if request.method == 'POST':
        try:
            aadhar_no = request.form['AADHAAR_NO']
            name = request.form['NAME']
            dob = request.form['DATE_OF_BIRTH']
            gender = request.form['GENDER']
            address = request.form['ADDRESS']
         
            connection_obj = sqlite3.connect('vaccination_pro.db')

            cursor_obj = connection_obj.cursor()
           
            cursor_obj.execute('''INSERT INTO AADHAAR_INFO 
                  (AADHAAR_NO,NAME,DATE_OF_BIRTH,GENDER,ADDRESS) VALUES (?,?,?,?,?)''',
                  (aadhar_no,name,dob,gender,address))
            
            connection_obj.commit()
            msg = "Record successfully added"
        except:
            connection_obj.rollback()
            msg = "error in insert operation"
         
        finally:
            return render_template("new_record.html",msg = msg)             
            connection_obj.close()
    
    

@app.route('/a_vaccine',methods=['POST', 'GET'])
def a_vaccine():
    if request.method == 'POST':
        try:
            aadhar_id = request.form['AADHAAR_no']
            vaccinedate = request.form['VACCINATION_DATE']
            dose = request.form['DOSE_no']
            age = request.form['AGE']
            vaccsite = request.form['vaccination_site']
                       
            connection_obj = sqlite3.connect('vaccination_pro.db')
            cursor_obj = connection_obj.cursor()

            cursor_obj.execute('''INSERT INTO VACCINATION_INFO 
                  (AADHAAR_no,VACCINATION_DATE,DOSE_no,AGE,vaccination_site) VALUES (?,?,?,?,?)''',
                  (aadhar_id,vaccinedate,dose,age,vaccsite) )
            
            connection_obj.commit()
            msg = "Record successfully added"
        except:
            connection_obj.rollback()
            msg = "error in insert operation"
      
        finally:
            return render_template("new_record.html",msg = msg)             
            connection_obj.close()
            
            
            

@app.route('/display_id_info',methods=['POST', 'GET'])
def display_id_info():
    if request.method == 'POST':
        
        connection_obj = sqlite3.connect('vaccination_pro.db')
        connection_obj.row_factory = sqlite3.Row
        cursor_obj = connection_obj.cursor()

        aadhar_idd = request.form['aadhar_idd']
        cursor_obj.execute('''CREATE TABLE IF NOT EXISTS query AS
                    SELECT AADHAAR_INFO.AADHAAR_NO, AADHAAR_INFO.NAME, 
                    VACCINATION_INFO.DOSE_no
                    FROM AADHAAR_INFO
                    INNER JOIN VACCINATION_INFO
                    ON AADHAAR_INFO.AADHAAR_NO = VACCINATION_INFO.AADHAAR_no 
                    ''') 

        qu="SELECT MAX(DOSE_no) as DOSE_no, AADHAAR_NO, NAME from query WHERE AADHAAR_NO = ?"
        
        cursor_obj.execute(qu, (aadhar_idd,))
        row = cursor_obj.fetchone()
        if row:    
            return render_template("display.html",row = row)
        else:
            return render_template("display.html",error='ID not available')
        connection_obj.close()
    else:
        return render_template("display.html")
                 
                 

@app.route('/vaccinated_record')
def vaccinated_record():

    con = sqlite3.connect("vaccination_pro.db")
    con.row_factory = sqlite3.Row
   
    cur = con.cursor()
    cur.execute('''SELECT AADHAAR_INFO.AADHAAR_NO, AADHAAR_INFO.NAME, AADHAAR_INFO.GENDER,                   
                    AADHAAR_INFO.ADDRESS,
                    VACCINATION_INFO.VACCINATION_DATE, VACCINATION_INFO.DOSE_no, VACCINATION_INFO.AGE,
                    VACCINATION_INFO.vaccination_site FROM AADHAAR_INFO
                    inner JOIN VACCINATION_INFO
                    ON AADHAAR_INFO.AADHAAR_NO = VACCINATION_INFO.AADHAAR_no
                   ''')
   
    rows = cur.fetchall()
    return render_template("records.html",rows = rows)
    con.close()

if __name__ == '__main__':
    app.run(debug = True)