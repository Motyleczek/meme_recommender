import imghdr
import struct

from flask import Blueprint, render_template, request, flash, jsonify
from .config import config
from ..reddit_api_functions import *
from ..reddit_api_functions.post import post
from . import Website
import os
print(os.getcwd())
from ..etl_module.app import meme_prediction
import keras
import random
import psycopg2
import datetime
import pytz
import string


views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'png'}

@views.route('/', methods=["GET", "POST"])
def index():
    # website = Website()
    # if request.method == "POST":
    conn = None
    data = None
    try:
        params = config()
        n = random.randint(1, 3226)
        conn = psycopg2.connect(**params)

        print('Connected succesfully')

        cur = conn.cursor()

        cur.execute('SELECT * FROM public."MemeTable" WHERE key = %s', (n,))

        data = cur.fetchall()

    except(Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()

    return render_template('index.html', data=data)
    # else:
    #     return render_template('index.html')

@views.route('/MemeAnalyzer', methods=['GET', 'POST'])
def meme_analyzer():
    print(os.getcwd())
    if request.method == "POST":
        file = request.files['file']

        if file and allowed_file(file.filename):
            title = request.form['title']
            author = request.form['author']
            # request.files["datafile"] --> this is as a FileStorage obj
            img_path = "meme_recommender/website/static/input_img.jpg"
            request.files["file"].save(img_path)

            post_url = post(img_path, request.form["title"])

            # model_A = keras.models.load_model("meme_recommender/model_A.keras")
            # model_C = keras.models.load_model("meme_recommender/model_C.keras")
            # prediction = meme_prediction(model_A, model_C, img_path)
            # with open("meme_recommender/website/static/wynik.txt", "wt") as file:
            #     file.write(str(prediction))

            save_meme_in_database(file, title, author, post_url, img_path)

    return render_template('meme_analyzer.html')

@views.route('/MemeExplorer', methods=["GET", "POST"])
def meme_explorer():

    if request.method == "POST": 
        conn = None
        data = None
        try:
            params = config()
            conn = psycopg2.connect(**params)

            print('Connected succesfully')

            cur = conn.cursor()

            humour = request.form.get('humour')
            sarcasm = request.form.get('sarcasm')
            offence = request.form.get('offence')
            motivation = request.form.get('motivation')
            sentiment = request.form.get('sentiment')

            query = f'SELECT * FROM public."MemeTable" WHERE humour = \'{humour}\' \
            AND sarcasm = \'{sarcasm}\' \
            AND offensive = \'{offence}\' \
            AND motivational = \'{motivation}\' \
            AND sentiment = \'{sentiment}\''

            cur.execute(query)

            meme_data = cur.fetchall()

            if meme_data == None:
                meme_data = 'No files found'

        except(Exception, psycopg2.Error) as error:
            print(error)

        finally:
            if conn is not None:
                cur.close()
                conn.close()

        return render_template('meme_explorer.html', data=meme_data)
    
    return render_template('meme_explorer.html')


def save_meme_in_database(file, title, author, post_url, img_path):
    image_width, image_height = get_image_dimensions(file)
    time = datetime.datetime.now(pytz.UTC)
    generated_id = generate_id()
    ups = random.randint(0,10000)
    downs = random.randint(0,10000)

    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()

        cur.execute(
            'INSERT INTO public."MemeTable" (title, thumbnail, height, width, time, author, id, ups, downs, media) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (title, img_path, image_height, image_width, time, author, generated_id, ups, downs, post_url)
        )

        conn.commit()
        flash('New Meme successfully saved', 'success')
    except Exception as error:
        flash(f'Error occurred: {error}', 'error')
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_dimensions(file):
    image_data = file.read()
    image_format = imghdr.what(None, h=image_data)

    if image_format == 'jpeg' or image_format == 'jpg':
        return struct.unpack('>HH', image_data[162:166])
    elif image_format == 'png':
        return struct.unpack('>LL', image_data[16:24])


def generate_id():
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(6))
    return random_id
