import typing

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


stores = [
    {
        'name': 'Chidinma\'s Store',
        'items': [
            {
                'name': 'Macbook Pro',
                'price': 1000,
            }
        ]
    }
]

# @app.route('/')
# def home():
#     return "Hello World Class Developer!"

@app.route('/')
def home():
    return render_template('index.html')


# POST - Used to tell the server to receive/create data
# GET - Used to tell the server to retrieve data
# 
# ---------------------------------------------------------

# POST /store data:{name}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store_name(name: str):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

# GET /store
@app.route('/store', methods=['GET'])
def get_all_stores():
    return jsonify({'stores':stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name: str):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item_in_store = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item_in_store)
            return jsonify(new_item_in_store)
    return jsonify({'message': 'store not found'})

# GET /store/string:name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_item_in_store(name: str):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})

if __name__ == '__main__':
    app.run(port=2000, debug=True)