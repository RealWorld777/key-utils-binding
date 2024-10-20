import ctypes

# Load the KeyUtils DLL
lib = ctypes.CDLL("./KeyUtils.dll")

# Define argument and return types for ctypes bindings

# bool getSubseedFromSeed(const uint8_t* seed, uint8_t* subseed)
lib.getSubseedFromSeed.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8)
]
lib.getSubseedFromSeed.restype = ctypes.c_bool

# void getPrivateKeyFromSubSeed(const uint8_t* seed, uint8_t* privateKey)
lib.getPrivateKeyFromSubSeed.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8)
]
lib.getPrivateKeyFromSubSeed.restype = None

# void getPublicKeyFromPrivateKey(const uint8_t* privateKey, uint8_t* publicKey)
lib.getPublicKeyFromPrivateKey.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8)
]
lib.getPublicKeyFromPrivateKey.restype = None

# void getIdentityFromPublicKey(const uint8_t* pubkey, char* identity, bool isLowerCase)
lib.getIdentityFromPublicKey.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_bool
]
lib.getIdentityFromPublicKey.restype = None

# void getTxHashFromDigest(const uint8_t* digest, char* txHash)
lib.getTxHashFromDigest.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_char)
]
lib.getTxHashFromDigest.restype = None

# void getPublicKeyFromIdentity(const char* identity, uint8_t* publicKey)
lib.getPublicKeyFromIdentity.argtypes = [
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_uint8)
]
lib.getPublicKeyFromIdentity.restype = None

# bool checkSumIdentity(const char* identity)
lib.checkSumIdentity.argtypes = [
    ctypes.c_char_p
]
lib.checkSumIdentity.restype = ctypes.c_bool

# Python wrapper functions
def getSubseedFromSeed(seed: bytes) -> bytes:
    if len(seed) != 55:
        raise ValueError("Seed must be exactly 55 bytes long.")
    subseed = (ctypes.c_uint8 * 32)()
    seed_array = (ctypes.c_uint8 * len(seed)).from_buffer_copy(seed)
    success = lib.getSubseedFromSeed(seed_array, subseed)
    if not success:
        raise ValueError("Invalid seed: must contain only lowercase letters a-z.")
    return subseed

def getPrivateKeyFromSubSeed(subseed: bytes) -> bytes:
    if len(subseed) != 32:
        raise ValueError("Subseed must be exactly 55 bytes long.")
    privateKey = (ctypes.c_uint8 * 32)()
    subseed_array = (ctypes.c_uint8 * len(subseed)).from_buffer_copy(subseed)
    lib.getPrivateKeyFromSubSeed(subseed_array, privateKey)
    return privateKey

def getPublicKeyFromPrivateKey(privateKey: bytes) -> bytes:
    if len(privateKey) != 32:
        raise ValueError("Private key must be exactly 32 bytes long.")
    publicKey = (ctypes.c_uint8 * 32)()
    privateKey_array = (ctypes.c_uint8 * len(privateKey)).from_buffer_copy(privateKey)
    lib.getPublicKeyFromPrivateKey(privateKey_array, publicKey)
    return publicKey

def getIdentityFromPublicKey(publicKey: bytes, isLowerCase: bool = False) -> str:
    if len(publicKey) != 32:
        raise ValueError("Public key must be exactly 32 bytes long.")
    identity = (ctypes.c_char * 60)()
    publicKey_array = (ctypes.c_uint8 * len(publicKey)).from_buffer_copy(publicKey)
    lib.getIdentityFromPublicKey(publicKey_array, identity, ctypes.c_bool(isLowerCase))
    return bytes(identity).decode('ascii')

def getTxHashFromDigest(digest: bytes) -> bytes:
    if len(digest) != 32:
        raise ValueError("Digest must be exactly 32 bytes long.")
    txHash = (ctypes.c_uint8 * 32)()
    digest_array = (ctypes.c_uint8 * len(digest)).from_buffer_copy(digest)
    lib.getTxHashFromDigest(digest_array, txHash)
    return txHash

def getPublicKeyFromIdentity(identity: str) -> bytes:
    if len(identity) != 60:
        raise ValueError("Identity must be exactly 60 characters long.")
    publicKey = (ctypes.c_uint8 * 32)()
    identity_bytes = identity.encode('utf-8')
    lib.getPublicKeyFromIdentity(identity_bytes, publicKey)
    return publicKey

def checkSumIdentity(identity: str) -> bool:
    if len(identity) != 60:
        raise ValueError("Identity must be exactly 60 characters long.")
    identity_bytes = identity.encode('utf-8')
    return bool(lib.checkSumIdentity(identity_bytes))

def getDigestFromSiblings32(
    depth: int,
    input_bytes: bytes,
    input_byte_len: int,
    input_index: int,
    siblings: list
) -> bytes:
    if len(input_bytes) != input_byte_len:
        raise ValueError("Input bytes length does not match input_byte_len.")
    if len(siblings) != depth or any(len(sib) != 32 for sib in siblings):
        raise ValueError("Each sibling must be exactly 32 bytes and match the depth.")
    
    output = (ctypes.c_uint8 * 32)()
    input_array = (ctypes.c_uint8 * len(input_bytes)).from_buffer_copy(input_bytes)
    
    # Create a 2D array for siblings
    SiblingsType = ctypes.c_uint8 * 32
    siblings_array = (SiblingsType * 32)()
    for i, sib in enumerate(siblings):
        if i >= 32:
            break  # Prevent overflow if depth > 32
        sib_array = SiblingsType(*sib)
        siblings_array[i] = sib_array
    
    lib.getDigestFromSiblings32(
        ctypes.c_uint(depth),
        input_array,
        ctypes.c_uint(input_byte_len),
        ctypes.c_uint(input_index),
        siblings_array,
        output
    )
    return output

# Example usage

seed = "wqbdupxgcaimwdsnchitjmsplzclkqokhadgehdxqogeeiovzvadstt"
publicId = "SUZFFQSCVPHYYBDCQODEMFAOKRJDDDIRJFFIWFLRDDJQRPKMJNOCSSKHXHGK"

subseed = getSubseedFromSeed(bytes(seed, 'utf-8'))
privateKey = getPrivateKeyFromSubSeed(subseed)
publicKey = getPublicKeyFromPrivateKey(privateKey)
identity = getIdentityFromPublicKey(publicKey)

print(identity == publicId)
