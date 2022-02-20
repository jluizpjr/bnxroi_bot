import sqlite3
from flask import Flask, render_template, request
import traceback
import sys

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('../ama-1001577316753.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_db_connection_vote():
    conn = sqlite3.connect('vote.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM ama').fetchall()
    conn.close()
    return render_template('index.html', questions=questions)


@app.route('/bsc/')
def bsc():
    return render_template('bsc.html')


# VOTE FOR VOLUNTEER

@app.route('/vote_main')
def vote_main():
    conn = get_db_connection_vote()
    volunteers = conn.execute('SELECT * FROM volunteers').fetchall()
    conn.close()
    return render_template('vote_main.html', volunteers=volunteers)

@app.route('/vote_adm', methods=['GET'])
def vote_adm():
    conn = get_db_connection_vote()
    volunteers = conn.execute('SELECT * FROM volunteers').fetchall()
    conn.close()
    print(volunteers)
    return render_template('vote_adm.html', volunteers=volunteers)


@app.route('/vote_adm', methods=['POST'])
def vote_adm_insert():

    if request.method == 'POST':
        if request.form['submit'] == "submit":
            try:
                name = request.form['name']
                walletAddress = request.form['wallet_Address']
                print(name + " " + walletAddress)
                with sqlite3.connect("vote.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO volunteers (name) VALUES (?)", (name,))
                    con.commit()
                    msg = "Record successfully added"
                    con.row_factory = sqlite3.Row
                    volunteers = con.execute('SELECT * FROM volunteers').fetchall()
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))
                con.rollback()
                msg = "error in insert operation"
            finally:
                con.close()
                return render_template("vote_adm.html", volunteers=volunteers)

        elif request.form['submit'] == "delete":
            print("Callind delete")
            print(request.form.getlist('checkbox'))
            try:
                names = request.form.getlist('checkbox')
                with sqlite3.connect("vote.db") as con:
                    cur = con.cursor()
                    for name in names:
                        cur.execute("DELETE FROM volunteers WHERE name=(?)", (name,))
                        con.commit()
                    msg = "Record successfully deleted"
                    con.row_factory = sqlite3.Row
                    volunteers = con.execute('SELECT * FROM volunteers').fetchall()

            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))
                con.rollback()
                msg = "error in delete operation"
            finally:
                con.close()
                print(volunteers)
                return render_template("vote_adm.html", volunteers=volunteers)
