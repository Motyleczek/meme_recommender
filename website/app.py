# used only for experimentation, the final versions should be implemented
# in views.py in order to be present on the website

from flask import Flask, render_template, url_for
# from . import Website
import random
import psycopg2
import os
from config import config

app = Flask(__name__)   # means when this file is run

@app.route('/', methods = ["GET", "POST"])
def index():
    conn = None
    data = None
    try:
        params = config()
        n = random.randint(1, 3000)
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        cur.execute('SELECT * FROM public."MemeTable" WHERE key = %s', (n,))

        data = cur.fetchall()
        print(data)

    except(Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()

    return render_template('index.html', data=data)

@app.route('/MemeAnalyzer')
def meme_analyzer():
    return render_template('meme_analyzer.html')

@app.route('/MemeExplorer')
def meme_explorer():
    return render_template('meme_explorer.html')



if __name__ == "__main__":
    app.run(debug=True)