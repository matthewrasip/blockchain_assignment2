from utils.rsa_utils import public_key_generation, private_key_generation, Inventory

p = 787435686772982288169641922308628444877260947
q = 1325305233886096053310340418467385397239375379
e = 692450682143089563609787

public_key_B = public_key_generation(p, q, e)
private_key_B = private_key_generation(p , q, public_key_B)

identity_B = 127
rand_int_B = 721

inventory_B_object = Inventory(public_key_B, private_key_B, identity_B, rand_int_B)
