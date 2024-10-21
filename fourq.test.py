from fourq import *

seed = "wqbdupxgcaimwdsnchitjmsplzclkqokhadgehdxqogeeiovzvadstt"
publicId = "SUZFFQSCVPHYYBDCQODEMFAOKRJDDDIRJFFIWFLRDDJQRPKMJNOCSSKHXHGK"

subseed = get_subseed_from_seed(bytes(seed, 'utf-8'))
privateKey = get_private_key_from_subseed(subseed)
publicKey = get_public_key_from_private_key(privateKey)
identity = get_identity_from_public_key(publicKey)

print(identity == publicId)
