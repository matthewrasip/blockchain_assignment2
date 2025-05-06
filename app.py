from flask import Flask, render_template, request
import json
import os

# import funcitons
import utils.rsa_utils

# import variables/objects from key files
import data.InventoryA.inventory_A_keys as A

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    node    = request.form['node']       # 'A','B','C' or 'D'
    item_id = request.form['item_id']
    qty     = int(request.form['qty'])
    price   = float(request.form['price'])

    print(f"{node}, {item_id}, {qty}, {price}")

    # 3) Append to this node's JSON file
    # data_dir = os.path.join(os.path.dirname(__file__), 'data')
    # fname    = os.path.join(data_dir, f"inventory_{node}.json")
    # if os.path.exists(fname):
    #     with open(fname, 'r') as f:
    #         db = json.load(f)
    # else:
    #     db = {'records': []}

    # db['records'].append({
    #     'item_id':  item_id,
    #     'qty':      qty,
    #     'price':    price,
    #     'signature': signature
    # })
    # with open(fname, 'w') as f:
    #     json.dump(db, f, indent=2)

    return render_template('index.html')
    #                        node=node,
    #                        message=message,
    #                        signature=signature,
    #                        verification=verification)


if __name__ == '__main__':
    app.run(debug=True)