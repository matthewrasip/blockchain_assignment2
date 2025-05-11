from utils.rsa_utils import public_key_generation, private_key_generation, PKG

p = 1004162036461488639338597000466705179253226703
q = 950133741151267522116252385927940618264103623
e = 973028207197278907211

pkg_public = public_key_generation(p, q, e) # [n, e]
pkg_private = [private_key_generation(p, q, pkg_public), p*q] # [d, n]

pkg = PKG(pkg_public, pkg_private)