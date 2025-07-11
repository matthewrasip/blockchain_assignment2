from utils.rsa_utils import public_key_generation, private_key_generation, Inventory

p = 1287737200891425621338551020762858710281638317
q = 1330909125725073469794953234151525201084537607
e = 33981230465225879849295979

public_key_D = public_key_generation(p, q, e)
private_key_D = private_key_generation(p , q, public_key_D)

identity_D = 129
rand_int_D = 921

inventory_D_object = Inventory(public_key_D, private_key_D, identity_D, rand_int_D)