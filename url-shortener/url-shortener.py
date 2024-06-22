from flask import Flask, request, redirect, render_template, url_for
import sqlite3
import string
import random

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                (id INTEGER PRIMARY KEY, original_url TEXT, short_id TEXT)''')
    conn.commit()
    conn.close()


def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(characters) for _ in range(length))
    return short_id


def get_original_url(short_id):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('SELECT original_url FROM urls WHERE short_id=?', (short_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None


def store_url(original_url, short_id):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('INSERT INTO urls (original_url, short_id) VALUES (?, ?)', (original_url, short_id))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_id = generate_short_id()
        store_url(original_url, short_id)
        return render_template('index.html', short_url=request.host_url + short_id)
    return render_template('index.html')

@app.route('/<short_id>')
def redirect_to_url(short_id):
    original_url = get_original_url(short_id)
    if original_url:
        return redirect(original_url)
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
