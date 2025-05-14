from hashlib import md5

class Inventory:
    # experimenting with ways we can get public and private keys to app.py
    def __init__(self, public_key : list, private_key : int, identity : int, rand_int : int):
        self.public_key = public_key
        self.private_key = private_key
        self.identity = identity
        self.rand_int = rand_int
        self.secret_key = 0
        self.t_value = 0
        self.signature = 0


class PKG:
    def __init__(self, pkg_public_key : list, pkg_private_key : list):
        self.pkg_public_key = pkg_public_key
        self.pkg_private_key = pkg_private_key

    # secret key generation
    def signIdentity(self, identity : int):
        return pow(identity, self.pkg_private_key[0], self.pkg_private_key[1])
    

    def computeT(self, rand_int : int):
        return pow(rand_int, self.pkg_public_key[1], self.pkg_public_key[0])
    
    def aggregate(self, t_values : list):
        result = 1
        for values in t_values:
            result *= values
        return result % self.pkg_public_key[0]


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
    hex_object = md5(raw_data.encode("utf-8"))
    hex_data = hex_object.hexdigest()
    decimal_data = int(hex_data, 16)

    # generate the signature, returns (m, s)
    signature = pow(decimal_data, private_key, public_key[0])
    return [decimal_data, signature]

def hashAggTandMessage(t : int, m : str):
    combined_raw_data = f"{t}{m}"
    hex_object = md5(combined_raw_data.encode("utf-8"))
    hex_data = hex_object.hexdigest()
    return int(hex_data, 16)


def verification(message : int , signature : int, public_key : list):
    if pow(signature, public_key[1], public_key[0]) == message:
        return True
    else:
        return False

