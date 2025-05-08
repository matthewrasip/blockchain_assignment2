from flask import Flask, render_template, request
import json
import os


# import funcitons
from utils.rsa_utils import encrypt, verification

# import variables/objects from key files
import data.InventoryA.inventory_A_keys as A
import data.InventoryB.inventory_B_keys as B
import data.InventoryC.inventory_C_keys as C
import data.InventoryD.inventory_D_keys as D

# creating list for inventories
inventories = [A.inventory_A_object, B.inventory_B_object, C.inventory_C_object, D.inventory_D_object]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    successful_checks = 0

    node    = request.form['node']       # 'A','B','C' or 'D'
    item_id = request.form['item_id']
    qty     = int(request.form['qty'])
    price   = float(request.form['price'])

    combined_string = f"{item_id}{qty}{price}{node}"

    if node == "A":
        relevant_public_key = A.inventory_A_object.public_key
        relevant_private_key = A.inventory_A_object.private_key
    elif node == "B":
        relevant_public_key = B.inventory_B_object.public_key
        relevant_private_key = B.inventory_B_object.private_key
    elif node == "C":
        relevant_public_key = C.inventory_C_object.public_key
        relevant_private_key = C.inventory_C_object.private_key
    elif node == "D":
        relevant_public_key = D.inventory_D_object.public_key
        relevant_private_key = D.inventory_D_object.private_key
        

    encrypted_message = encrypt(combined_string, relevant_private_key, relevant_public_key)

    # begin consensus / verificaiton 
    for inventory in inventories:
        if verification(encrypted_message[0], encrypted_message[1], relevant_public_key):
            successful_checks += 1
    
    if successful_checks >= (len(inventories)/3 * 2): 
        print("success!!!")


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