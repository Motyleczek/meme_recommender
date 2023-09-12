from flask import Blueprint, render_template, request, flash, jsonify
from .config import config
from . import Website
import os
print(os.getcwd())
from ..etl_module.app import meme_prediction
import keras
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

    except(Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()

    return render_template('index.html', data=data)

@views.route('/MemeAnalyzer', methods=['GET', 'POST'])
def meme_analyzer():
    print(os.getcwd())
    if request.method == "POST":
        # request.files["datafile"] --> this is as a FileStorage obj
        img_path = "meme_recommender/website/static/input_img.jpg"
        request.files["file"].save(img_path)
        model_A = keras.models.load_model("meme_recommender/model_A.keras")
        model_C = keras.models.load_model("meme_recommender/model_C.keras")
        prediction = meme_prediction(model_A, model_C, img_path)
        with open("meme_recommender/website/static/wynik.txt", "wt") as file:
            file.write(str(prediction))
    return render_template('meme_analyzer.html')

@views.route('/MemeExplorer')
def meme_explorer():
    return render_template('meme_explorer.html')

