from flask import Flask, render_template, request
import json
from json import JSONDecodeError
import os
import struct

# import functions
from utils.rsa_utils import *

# import key objects
import data.InventoryA.inventory_A_keys as A
import data.InventoryB.inventory_B_keys as B
import data.InventoryC.inventory_C_keys as C
import data.InventoryD.inventory_D_keys as D

import data.officer as O

import data.pkg as server

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

        return render_template('index.html', message="Record Successfully Added")

    # 5) Consensus failed
    print("fail")
    return render_template('index.html', error="Failed to Add Record")


@app.route('/search', methods=['GET'])
def search():
    query_id = request.args.get('query_id', '').strip()
    record = None
    error = False
    record_string = None

    if query_id:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        found_inventories = []

        # STEP 2: scan each inventory
        for loc in ['A','B','C','D']:
            path = os.path.join(data_dir, f"Inventory{loc}", f"inventory_{loc}.json")
            try:
                with open(path, 'r') as f:
                    db = json.load(f)
            except (FileNotFoundError, JSONDecodeError):
                continue

            for rec in db.get('records', []):
                if rec.get('item_id') == query_id:
                    found_inventories.append((loc, rec))
                    break

        # STEP 3: consensus check ≥ 2/3 of nodes
        total_nodes = len(inventories)      # 4
        threshold   = (total_nodes / 3) * 2
        if len(found_inventories) >= threshold:
            loc, rec = found_inventories[0]

            # format price
            price = rec['price']
            if isinstance(price, float) and price.is_integer():
                price_str = f"{price:.0f}"
            else:
                price_str = str(price)

            # build record string
            record_string = f"{rec['item_id']}{rec['qty']}{price_str}{loc}"
            print(f"Consensus OK ({len(found_inventories)}/{total_nodes}), record: {record_string}")

            record = {
                'item_id':  rec['item_id'],
                'qty':       rec['qty'],
                'price':     price_str,
                'location':  loc
            }
        else:
            print(f"Consensus FAILED ({len(found_inventories)}/{total_nodes}), aborting search")
            error = True


        # print to terminal only
        if record_string:
            # print(f"Found record: {record_string}")

            # PKG variable loaded
            pkg = server.pkg


            # STEP 4: generate secret keys using identities
            for inventory in inventories:
                inventory.secret_key = pkg.signIdentity(inventory.identity)

            # STEP 5: compute t values
            for inventory in inventories:
                inventory.t_value = pkg.computeT(inventory.rand_int)

            # STEP 6: with t values, calc aggregate t
            t_values = []
            for inventory in inventories:
                t_values.append(inventory.t_value)
            aggregate_t = pkg.aggregate(t_values)


            # STEP 7: calculate hash(t,m)
            decimal_hash = hashAggTandMessage(aggregate_t, record_string)

            # STEP 8: each inventory signs the hash
            for inventory in inventories:
                inventory.signature = inventory.secret_key * pow(inventory.rand_int, decimal_hash, pkg.pkg_public_key[0])


            # STEP 9 : calculate aggregate s
            signatures = []
            for inventory in inventories:
                signatures.append(inventory.signature)
            aggregate_s = pkg.aggregate(signatures)

            # STEP 10: return (aggT, aggS) to pkg

            # STEP 11: verificaiton occurs IN PKG (I THINK??)
            # start verification 1
            verif1 = pow(aggregate_s, pkg.pkg_public_key[1], pkg.pkg_public_key[0])

            # start verification 2
            aggregate_i = 1
            for inventory in inventories:
                aggregate_i *= inventory.identity

            result1 = aggregate_i % pkg.pkg_public_key[0]
            result2 = pow(aggregate_t, decimal_hash, pkg.pkg_public_key[0])

            verif2 = (result1 * result2) % pkg.pkg_public_key[0]

            if verif1 == verif2:
                print("success!!!")
                # STEP 12: encrypt message
                record_string_bytes = bytes(record_string, "utf-8")
                decimal_string = int.from_bytes(record_string_bytes, "big")
                ciphertext = pow(decimal_string, O.officer_public_key[1], O.officer_public_key[0])

                # STEP 13: decrypt message
                decrypted_decimal = pow(ciphertext, O.officer_private_key[0], O.officer_private_key[1])
                res = struct.pack(">Q", decrypted_decimal)
                decrypted_message = res.decode("utf-8")
                print(decrypted_message)
            else: 
                print("fail :(")
                # do not encrypt and ABORT

        else:
            print(f"No record found for Item ID {query_id}")

    # Render the same search page, passing in record or error
    return render_template('search.html', record=record, error=error)


if __name__ == '__main__':
    app.run(debug=True)
