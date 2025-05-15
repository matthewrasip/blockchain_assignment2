from utils.rsa_utils import public_key_generation, private_key_generation, Inventory

p = 1080954735722463992988394149602856332100628417
q = 1158106283320086444890911863299879973542293243
e = 106506253943651610547613

officer_public_key = public_key_generation(p, q, e)
officer_private_key = [private_key_generation(p, q, officer_public_key), p*q]

officer_object = Inventory(officer_public_key, officer_private_key, 0, 0)