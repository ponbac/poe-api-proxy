from flask import Flask
from flask_cors import CORS
import requests
from requests import get
from requests import cookies

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "<h1>/get/(your-url) to get some cool data</h1>"


@app.route('/get/', defaults={'path': ''})
@app.route('/get/<path:path>')
def proxy(path):
    s = requests.Session()
    s.get(f'{path}')

    cookie_obj = requests.cookies.create_cookie(domain='pathofexile.com', name='POESESSID', value='5fac1b643f65f2591d27a0ab8a2bd345')
    s.cookies.set_cookie(cookie_obj)

    print(s.cookies)

    return s.get(f'{path}', cookies=s.cookies).content


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
