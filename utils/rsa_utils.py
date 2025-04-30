from hashlib import md5

def encrypt(raw_data : str, private_key : int, public_key : list):
    # turn raw data into md5 hash (hex), then into decimal (int)
    hex_data = md5(raw_data)
    decimal_data = int(hex_data, 16)

    # generate the signature
    signature = pow(decimal_data, private_key, public_key[0])
    return [decimal_data, signature]


def verification(message : int , signature : int, public_key : list):
    if pow(signature, public_key[0], public_key[1]) == message:
        return True
    else:
        return False
    
