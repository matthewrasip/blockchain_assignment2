from hashlib import md5

class Inventory:
    # experimenting with ways we can get public and private keys to app.py
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        

def public_key_generation(p : int, q : int, e : int):
    public_key = [p*q, e]
    return public_key

def phi(p : int, q : int):
    return (p - 1)*(q - 1)

def private_key_generation(p : int, q: int, public_key : list):
    phi_n = phi(p, q)
    return pow(public_key[1], -1, phi_n)

def encrypt(raw_data : str, private_key : int, public_key : list):
    # turn raw data into md5 hash (hex), then into decimal (int)
    hex_data = md5(raw_data.encode("utf-8"))
    decimal_data = int(hex_data, 16)

    # generate the signature
    signature = pow(decimal_data, private_key, public_key[0])
    return [decimal_data, signature]


def verification(message : int , signature : int, public_key : list):
    if pow(signature, public_key[0], public_key[1]) == message:
        return True
    else:
        return False
    
