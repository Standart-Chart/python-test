from flask import *
import json, time

app = Flask(__name__)


@app.route('/smartphones', methods=['GET'])
def request_page():
    price = str(request.args.get('price'))

    with open('../smartphones.json') as all_smartphones:
        data = json.load(all_smartphones)

    display_data = []

    for smartphone in data:
        if price == smartphone['price']:
            display_data.append(smartphone)

    return display_data


if __name__ == '__main__':
    app.run(port=8000)
