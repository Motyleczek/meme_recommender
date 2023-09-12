from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import imghdr
from PIL import Image
import io
import base64
from .config import config
import random
import psycopg2

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'png'}

@app.route('/')
def index():
    # conn = None
    # data = None
    # try:
    #     params = config()
    #     n = random.randint(1, 3000)
    #     conn = psycopg2.connect(**params)

    #     cur = conn.cursor()

    #     cur.execute('SELECT * FROM public."MemeTable" WHERE key = %s', (n,))

    #     data = cur.fetchall()
    #     print(data)

    # except(Exception, psycopg2.Error) as error:
    #     print(error)

    # finally:
    #     if conn is not None:
    #         cur.close()
            # conn.close()

    return render_template('index.html')

@app.route('/MemeAnalyzer', methods=['GET', 'POST'])
def meme_analyzer():

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file and allowed_file(file.filename):
            title = request.form['title']
            author = request.form['author']

            image_data = file.read()
            image_width, image_height = get_image_dimensions(image_data)

            image_url = url_for('uploaded_file', filename=file.filename)

            return render_template('meme_send_confirmation.html', image_data_url=image_url, title=title, author=author,
                                   width=image_width, height=image_height)

    return render_template('meme_analyzer.html')

@app.route('/MemeExplorer')
def meme_explorer():
    return render_template('meme_explorer.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_dimensions(image_data):
    image = Image.open(io.BytesIO(image_data))
    width, height = image.size
    return width, height

def get_data_url(image_data):
    image_format = imghdr.what(None, image_data)
    if image_format:
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        data_uri = f'data:image/{image_format};base64,{encoded_image}'
        return data_uri
    return None

if __name__ == '__main__':
    app.run(debug=True)
