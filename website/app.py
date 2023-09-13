from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import imghdr
from PIL import Image
import io
import base64
from .config import config
import random
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/MemeAnalyzer')
def meme_analyzer():
    return render_template('meme_analyzer.html')

@app.route('/MemeExplorer')
def meme_explorer():
    return render_template('meme_explorer.html')

if __name__ == '__main__':
    app.run(debug=True)
