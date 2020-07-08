import os
from flask import Flask, request, send_file, send_from_directory, safe_join, abort
from flask_cors import CORS
import requests
from requests import get
from requests import cookies
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object("config.Config")
CORS(app)

NINJA_CURRENCY_URL = 'https://poe.ninja/api/data/currencyoverview'
NINJA_ITEM_URL = 'https://poe.ninja/api/data/itemoverview'

last_updated_dict = {
    'Currency': None,
    'Fragment': None,
    'Oil': None,
    'Incubator': None,
    'Scarab': None,
    'Fossil': None,
    'Resonator': None,
    'Essence': None,
    'DivinationCard': None,
    'Prophecy': None,
    'SkillGem': None,
    'UniqueMap': None,
    'Map': None,
    'UniqueJewel': None,
    'UniqueFlask': None,
    'UniqueWeapon': None,
    'UniqueArmour': None,
    'Watchstone': None,
    'UniqueAccessory': None,
    'DeliriumOrb': None,
    'Beast': None,
    'Vial': None,
}


@app.route('/')
def index():
    return "<h1>/get/(your-url) to get some cool data</h1>"


@app.route('/get/', defaults={'path': ''})
@app.route('/get/<path:path>')
def proxy(path):
    s = requests.Session()

    # Asks for POENINJA data
    if (path == NINJA_CURRENCY_URL or path == NINJA_ITEM_URL):
        objectType = request.args.get('type')
        folder_path = app.config['NINJA_DATA']
        filename = get_ninja_filename(objectType)
        full_path = folder_path + '/' + filename

        if is_not_empty(full_path) and age_is_ok(objectType):
            return send_from_directory(folder_path, filename=filename, as_attachment=False)
        else:
            ninja_data = s.get(path, params=request.args).content
            write_to_file(full_path, ninja_data)
            last_updated_dict[objectType] = datetime.now()
            return send_from_directory(folder_path, filename=filename, as_attachment=False)
            

    # Asks for everything else
    s.cookies.set('POESESSID', None)
    s.cookies.set('POESESSID', request.args.get('POESESSID'))

    return s.get(path, cookies=s.cookies, params=request.args).content


def age_is_ok(type_to_check):
    if last_updated_dict[type_to_check] is None:
        return False

    past = last_updated_dict[type_to_check]
    present = datetime.now()

    return past > (present - timedelta(minutes=app.config['MAX_AGE_NINJA_DATA']))


def is_not_empty(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def write_to_file(fpath, data_to_write):
    f = open(fpath,"w+")
    f.write(data_to_write.decode('utf-8'))
    f.close


def get_ninja_filename(type):
    file = ''

    if type == 'Currency':
        file = 'currency.json'
    elif type == 'Fragment':
        file = 'fragment.json'
    elif type == 'Oil':
        file = 'oil.json'
    elif type == 'Incubator':
        file = 'incubator.json'
    elif type == 'Scarab':
        file = 'scarab.json'
    elif type == 'Fossil':
        file = 'fossil.json'
    elif type == 'Resonator':
        file = 'resonator.json'
    elif type == 'Essence':
        file = 'essence.json'
    elif type == 'DivinationCard':
        file = 'divination_card.json'
    elif type == 'Prophecy':
        file = 'prophecy.json'
    elif type == 'SkillGem':
        file = 'skill_gem.json'
    elif type == 'UniqueMap':
        file = 'unique_map.json'
    elif type == 'Map':
        file = 'map.json'
    elif type == 'UniqueJewel':
        file = 'unique_jewel.json'
    elif type == 'UniqueFlask':
        file = 'unique_flask.json'
    elif type == 'UniqueWeapon':
        file = 'unique_weapon.json'
    elif type == 'UniqueArmour':
        file = 'unique_armour.json'
    elif type == 'Watchstone':
        file = 'watchstone.json'
    elif type == 'UniqueAccessory':
        file = 'unique_accessory.json'
    elif type == 'DeliriumOrb':
        file = 'delirium_orb.json'
    elif type == 'Beast':
        file = 'beast.json'
    elif type == 'Vial':
        file = 'vial.json'

    return file


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
