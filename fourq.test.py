from fourq import *

seed = "wqbdupxgcaimwdsnchitjmsplzclkqokhadgehdxqogeeiovzvadstt"
publicId = "SUZFFQSCVPHYYBDCQODEMFAOKRJDDDIRJFFIWFLRDDJQRPKMJNOCSSKHXHGK"

subseed = get_subseed_from_seed(bytes(seed, 'utf-8'))
privateKey = get_private_key_from_subseed(subseed)
publicKey = get_public_key_from_private_key(privateKey)
identity = get_identity_from_public_key(publicKey)

print(identity == publicId)


tx = 'bba07fde537ea438760811910f2d874f017974eadcfdde70aa771533aa94064cf219230a0b56fbb94b3d73d3879f245390fccc3b23c1fdab0482f59b14a9fe16000000000000000100abfa9a00000000'
bt = bytes.fromhex(tx)

print(bt, len(bt))

message_digest = kangaroo_twelve(bt, len(bt), 32)
print(message_digest.hex())

