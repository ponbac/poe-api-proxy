from flask import Flask
from flask_cors import CORS
from requests import get

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "<h1>/get/(your-url) to get some cool data</h1>"


@app.route('/get/', defaults={'path': ''})
@app.route('/get/<path:path>')
def proxy(path):
    return get(f'{path}', headers={'cookie': 'POESESSID=5fac1b643f65f2591d27a0ab8a2bd345'}).content


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
