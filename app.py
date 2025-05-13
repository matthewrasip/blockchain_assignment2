from flask import Flask, render_template, request
import json
from json import JSONDecodeError
import os

# import functions
from utils.rsa_utils import encrypt, verification

# import key objects
import data.InventoryA.inventory_A_keys as A
import data.InventoryB.inventory_B_keys as B
import data.InventoryC.inventory_C_keys as C
import data.InventoryD.inventory_D_keys as D

# list of all inventory objects (for consensus)
inventories = [
    A.inventory_A_object,
    B.inventory_B_object,
    C.inventory_C_object,
    D.inventory_D_object
]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    successful_checks = 0

    # 1) Pull form data
    location = request.form['location']   # 'A','B','C' or 'D'
    item_id  = request.form['item_id']
    qty      = int(request.form['qty'])
    price    = float(request.form['price'])

    combined_string = f"{item_id}{qty}{price}{location}"

    # 2) Select the right key pair
    if location == "A":
        relevant_public_key  = A.inventory_A_object.public_key
        relevant_private_key = A.inventory_A_object.private_key
    elif location == "B":
        relevant_public_key  = B.inventory_B_object.public_key
        relevant_private_key = B.inventory_B_object.private_key
    elif location == "C":
        relevant_public_key  = C.inventory_C_object.public_key
        relevant_private_key = C.inventory_C_object.private_key
    elif location == "D":
        relevant_public_key  = D.inventory_D_object.public_key
        relevant_private_key = D.inventory_D_object.private_key
    else:
        return render_template('index.html', error="Invalid location")

    # 3) Encrypt and verify across all nodes
    encrypted_message = encrypt(combined_string, relevant_private_key, relevant_public_key)
    for inventory in inventories:
        if verification(encrypted_message[0], encrypted_message[1], relevant_public_key):
            successful_checks += 1

    # 4) If ≥2/3 consensus, append to every JSON
    if successful_checks >= (len(inventories) / 3 * 2):
        print("success!!!")

        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        for loc in ['A', 'B', 'C', 'D']:
            inv_dir = os.path.join(data_dir, f"Inventory{loc}")
            os.makedirs(inv_dir, exist_ok=True)

            fname = os.path.join(inv_dir, f"inventory_{loc}.json")

            # load existing or initialize if missing/invalid
            try:
                with open(fname, 'r') as f:
                    db = json.load(f)
            except (FileNotFoundError, JSONDecodeError):
                db = {'records': []}
                

            # append new record
            db['records'].append({
                'item_id':  item_id,
                'qty':      qty,
                'price':    price,
                'location': location,
            })

            # write back out
            with open(fname, 'w') as f:
                json.dump(db, f, indent=2)

        return render_template('index.html', message="Record written to all inventories")

    # 5) Consensus failed
    return render_template('index.html', error="Verification failed")

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
