from utils.rsa_utils import *

p = 1210613765735147311106936311866593978079938707
q = 1247842850282035753615951347964437248190231863
e = 815459040813953176289801

public_key_A = public_key_generation(p, q, e)
private_key_A = private_key_generation(p , q, public_key_A)

invenA = Inventory(public_key_A, private_key_A)

print(invenA.public_key, invenA.private_key)