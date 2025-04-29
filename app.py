from flask import Flask, render_template, request
import json
import os
from utils.rsa_utils import get_keypair, sign_message, verify_message

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

    # 1) Build message string and sign it
    message   = f"{node}-{item_id}-{qty}-{price}"
    priv, pub = get_keypair(node)
    signature = sign_message(message, priv)

    # 2) Verify signature using each node’s public key
    verification = {}
    for other in ['A','B','C','D']:
        _, other_pub = get_keypair(other)
        verification[other] = verify_message(message, signature, other_pub)

    # 3) Append to this node's JSON file
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    fname    = os.path.join(data_dir, f"inventory_{node}.json")
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            db = json.load(f)
    else:
        db = {'records': []}

    db['records'].append({
        'item_id':  item_id,
        'qty':      qty,
        'price':    price,
        'signature': signature
    })
    with open(fname, 'w') as f:
        json.dump(db, f, indent=2)

    return render_template('result.html',
                           node=node,
                           message=message,
                           signature=signature,
                           verification=verification)

if __name__ == '__main__':
    app.run(debug=True)