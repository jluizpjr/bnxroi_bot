import sqlite3
from flask import Flask, render_template, request

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


@app.route('/vote_adm', methods=['POST', 'GET'])
def vote_adm():
    conn = get_db_connection_vote()
    volunteers = conn.execute('SELECT * FROM volunteers').fetchall()
    conn.close()
    return render_template('vote_adm.html', volunteers=volunteers)


@app.route('/vote_adm_insert', methods=['POST', 'GET'])
def vote_adm_insert():
    if request.method == 'POST':
        try:
            name = request.form['name']

            with sqlite3.connect("vote.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO volunteers (name) VALUES (?)", (name))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            con.close()
            return render_template("result.html", msg=msg)
