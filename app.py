import os
import yaml

from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)

SUPPORTED_WIKIPEDIA_LANGUAGE_CODES = ['en', 'de', 'nl', 'es', 'it', 'ru', 'fr', 'zh', 'ar', 'vi', 'ja', 'fi', 'ko',
                                      'tr', 'ro', 'cs', 'et', 'lt', 'kk', 'lv', 'hi', 'ne', 'my', 'si', 'gu']

__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, 'default_config.yaml'))))
try:
    app.config.update(
        yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))
except IOError:
    # It is ok if there is no local config file
    pass

# Enable CORS for API endpoints
#CORS(app, resources={'*': {'origins': '*'}})
CORS(app)

@app.route('/')
def index():
    lang, title = validate_api_args()
    return render_template('index.html', lang=lang, title=title)

def validate_lang(lang):
    return lang in SUPPORTED_WIKIPEDIA_LANGUAGE_CODES

def validate_api_args():
    lang = None
    if 'lang' in request.args:
        if validate_lang(request.args['lang'].lower()):
            lang = request.args['lang'].lower()

    title = None
    if 'title' in request.args:
        title = request.args['title'].replace('_', ' ')

    return lang, title