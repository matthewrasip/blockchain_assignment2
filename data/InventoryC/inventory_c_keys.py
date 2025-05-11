from utils.rsa_utils import public_key_generation, private_key_generation, Inventory

p = 1014247300991039444864201518275018240361205111
q = 904030450302158058469475048755214591704639633
e = 1158749422015035388438057

public_key_C = public_key_generation(p, q, e)
private_key_C = private_key_generation(p , q, public_key_C)

identity_C = 128
rand_int_C = 821

inventory_C_object = Inventory(public_key_C, private_key_C, identity_C, rand_int_C)