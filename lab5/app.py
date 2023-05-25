import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask('qqq')
conn = psycopg2.connect(database="service_db", user="postgres", password="mvpe86qw", host="localhost", port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            login = request.form.get('username')
            password = request.form.get('password')
            if login == '' or password == '':
                return render_template('accounter2.html')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(login), str(password)))
            records = list(cursor.fetchall())

            if records == []:
                return render_template('accounter1.html')

            return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        if request.form.get("login"):
            full_name = request.form.get('full_name')
            login = request.form.get("login")
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s", str(login))
            records = list(cursor.fetchall())
            if request.form.get("back"):
                return redirect("/login/")
            if records:
                if request.form.get("back"):
                    return redirect("/registration/")
                return render_template('username_exist.html')
            else:
                if(login and password and full_name) and ((login.count(' ')==0) and (password.count(' ')==0) and (full_name.count(' ')==1) and (full_name.find(' ')!=0) and (full_name.find(' ')!=(len(full_name)-1))):
                    cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(full_name), str(login), str(password)))
                else:
                    if request.form.get("back"):
                        return redirect("/registration/")
                    return render_template('incorrect_reg_date.html')
                conn.commit()

            return redirect('/login/')

    return render_template('registration.html')

