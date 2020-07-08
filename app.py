from flask import Flask
from flask import request
from flask import send_file, send_from_directory, safe_join, abort
from flask_cors import CORS
import requests
from requests import get
from requests import cookies

app = Flask(__name__)
app.config.from_object("config.Config")
CORS(app)

NINJA_CURRENCY_URL = 'https://poe.ninja/api/data/currencyoverview'
NINJA_ITEM_URL = 'https://poe.ninja/api/data/itemoverview'

@app.route('/')
def index():
    return "<h1>/get/(your-url) to get some cool data</h1>"


@app.route('/get/', defaults={'path': ''})
@app.route('/get/<path:path>')
def proxy(path):
    s = requests.Session()

    if (path == NINJA_CURRENCY_URL):
        return get_ninja_file(request.args.get('type'))
    # s.get(f'{path}')

    s.cookies.set('POESESSID', None)
    s.cookies.set('POESESSID', request.args.get('POESESSID'))

    # cookie_obj = requests.cookies.create_cookie(domain='pathofexile.com', name='POESESSID', value='xxx')
    # s.cookies.set_cookie(cookie_obj)

    # print(s.cookies)
    # print(f'{path}')
    # print(request.args)

    return s.get(path, cookies=s.cookies, params=request.args).content


def get_ninja_file(type):
    file = ''

    if type == 'Currency':
        file = 'currency.json'
    elif type == 'Fragment':
        file = 'fragment.json'

    return send_from_directory(app.config["NINJA_DATA"], filename=file, as_attachment=False) # Maybe remove as attachment


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
