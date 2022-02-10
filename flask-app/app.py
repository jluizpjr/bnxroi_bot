import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('../ama-1001577316753.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM ama').fetchall()
    conn.close()
    return render_template('index.html', questions=questions)