from flask import Blueprint, render_template, request, flash, jsonify
 
views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/MemeAnalyzer')
def meme_analyzer():
    return render_template('meme_analyzer.html')

@views.route('/MemeExplorer')
def meme_explorer():
    return render_template('meme_explorer.html')

