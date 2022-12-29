from flask import Flask, render_template
from vocab import suggest_vocabulary_word, vocabulary_word_search, pronounciation, audio
import os
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    global text1
    global text2
    global text3
    global text4
    global text5
    global vocabulary_word
    folder = 'static'
    # Delete the folder and all of its contents
    os.makedirs(folder, exist_ok=True)
    shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)
    text1, text2, text3, text4, text5, vocabulary_word, pos, meaning, example_sentence, etymology = suggest_vocabulary_word()
    vocabulary_word_search(vocabulary_word)
    return render_template('index.html', 
                            vocabulary_word=vocabulary_word, 
                            pos=pos, 
                            meaning=meaning, 
                            example_sentence=example_sentence, 
                            etymology=etymology)


@app.route('/call_function', methods=['POST'])
def call_function():
    audio(text1, text2, text3, text4, text5)
    return "Function called successfully!"

@app.route('/call_word', methods=['POST'])
def call_word():
    pronounciation(vocabulary_word)
    return "Function called successfully!"
