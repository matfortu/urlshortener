from flask import Flask, redirect
import sqlite3
import random
import string

HOST = 'https://matfortu.it'

app = Flask(__name__)

def new(url):
    short = get_existing(url)
    if not short:
        short = get_random_string(4)
        db = sqlite3.connect('urls.db')
        c = db.cursor()
        c.execute('INSERT INTO urls (url, short) VALUES (?, ?)', (url, short))
        db.commit()
        c.close()
    return short

def search(short):
    db = sqlite3.connect('urls.db')
    c = db.cursor()
    c.execute("SELECT url FROM urls WHERE short = ?", [short])
    res = c.fetchone()
    db.close
    return res

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_existing(url):
    res = tuple()
    db = sqlite3.connect('urls.db')
    c = db.cursor()
    c.execute("SELECT short FROM urls WHERE url = ?", [url])
    res = c.fetchone()
    db.close
    return res[0]

@app.route('/<short>', methods=['GET'])
def handle_search(short=None):
    try:
        res = search(short)[0]
        if not res.startswith('http'):
            res = 'https://' + res
        return redirect(res, code=302)
    except:
        return "Shortlink not found"

@app.route('/add', methods=['GET'])
@app.route('/add/', methods=['GET'])
@app.route('/add/<url>', methods=['GET'])
@app.route('/add/<path:url>', methods=['GET'])
def add(url= None):
    if url and (url.startswith('http') or url.startswith('https')):
        short = new(url)
        return f'{url} -> <a href="{HOST}/{short}">{HOST}/{short}</a>'
    else:
        return "Invalid URL"