from flask import Blueprint, render_template, request, flash, jsonify
from .config import config
from . import Website
import random
import psycopg2

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def index():
    conn = None
    data = None
    try:
        params = config()
        n = random.randint(1, 3000)
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        cur.execute('''SELECT * FROM public."MemeTable" ORDER BY key ASC''')

        data = cur.fetchall()
        print(data)

    except(Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()

    return render_template('index.html', data=data)

@views.route('/MemeAnalyzer')
def meme_analyzer():
    return render_template('meme_analyzer.html')

@views.route('/MemeExplorer')
def meme_explorer():
    return render_template('meme_explorer.html')

