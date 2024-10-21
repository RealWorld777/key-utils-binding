import os
import ctypes

lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "KeyUtils.dll"))

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

# void signWithNonceK(const unsigned char* k, const unsigned char* publicKey, const unsigned char* messageDigest, unsigned char* signature)
lib.signWithNonceK.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8)
]
lib.signWithNonceK.restype = None

# void sign(const unsigned char* subseed, const unsigned char* publicKey, const unsigned char* messageDigest, unsigned char* signature) 
lib.sign.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8)
]
lib.sign.restype = None

# bool verify(const unsigned char* publicKey, const unsigned char* messageDigest, const unsigned char* signature)
lib.verify.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8)
]
lib.verify.restype = ctypes.c_bool

# void KangarooTwelve(const uint8_t *input, unsigned int inputByteLen, uint8_t *output, unsigned int outputByteLen)
lib.KangarooTwelve.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint
]
lib.KangarooTwelve.restype = None

# Python wrapper functions
def get_subseed_from_seed(seed: bytes) -> bytes:
    """
    Generates a subseed from the provided seed.

    Args:
        seed (bytes): A 55-byte seed used to generate the subseed.

    Returns:
        bytes: A 32-byte subseed.

    Raises:
        ValueError: If the seed is not exactly 55 bytes long or contains invalid characters.
    """

    if len(seed) != 55:
        raise ValueError("Seed must be exactly 55 bytes long.")
    subseed = (ctypes.c_uint8 * 32)()
    seed_array = (ctypes.c_uint8 * len(seed)).from_buffer_copy(seed)
    success = lib.getSubseedFromSeed(seed_array, subseed)
    if not success:
        raise ValueError("Invalid seed: must contain only lowercase letters a-z.")
    return subseed

def get_private_key_from_subseed(subseed: bytes) -> bytes:
    """
    Derives a private key from the provided subseed.

    Args:
        subseed (bytes): A 32-byte subseed used to generate the private key.

    Returns:
        bytes: A 32-byte private key.

    Raises:
        ValueError: If the subseed is not exactly 32 bytes long.
    """

    if len(subseed) != 32:
        raise ValueError("Subseed must be exactly 55 bytes long.")
    private_key = (ctypes.c_uint8 * 32)()
    subseed_array = (ctypes.c_uint8 * len(subseed)).from_buffer_copy(subseed)
    lib.getPrivateKeyFromSubSeed(subseed_array, private_key)
    return private_key

def get_public_key_from_private_key(private_key: bytes) -> bytes:
    """
    Generates a public key from the provided private key.

    Args:
        private_key (bytes): A 32-byte private key used to generate the public key.

    Returns:
        bytes: A 32-byte public key.

    Raises:
        ValueError: If the private key is not exactly 32 bytes long.
    """

    if len(private_key) != 32:
        raise ValueError("Private key must be exactly 32 bytes long.")
    public_key = (ctypes.c_uint8 * 32)()
    private_key_array = (ctypes.c_uint8 * len(private_key)).from_buffer_copy(private_key)
    lib.getPublicKeyFromPrivateKey(private_key_array, public_key)
    return public_key

def get_identity_from_public_key(public_key: bytes, is_lower_case: bool = False) -> str:
    """
    Derives an identity string from the provided public key.

    Args:
        public_key (bytes): A 32-byte public key used to generate the identity.
        is_lower_case (bool, optional): Flag to determine if the identity should be in lowercase. Defaults to False.

    Returns:
        str: A 60-character identity string.

    Raises:
        ValueError: If the public key is not exactly 32 bytes long.
    """

    if len(public_key) != 32:
        raise ValueError("Public key must be exactly 32 bytes long.")
    identity = (ctypes.c_char * 60)()
    public_key_array = (ctypes.c_uint8 * len(public_key)).from_buffer_copy(public_key)
    lib.getIdentityFromPublicKey(public_key_array, identity, ctypes.c_bool(is_lower_case))
    return bytes(identity).decode('ascii')

def get_tx_hash_from_digest(digest: bytes) -> bytes:
    """
    Generates a transaction hash from the provided digest.

    Args:
        digest (bytes): A 32-byte digest used to generate the transaction hash.

    Returns:
        bytes: A 32-byte transaction hash.

    Raises:
        ValueError: If the digest is not exactly 32 bytes long.
    """

    if len(digest) != 32:
        raise ValueError("Digest must be exactly 32 bytes long.")
    tx_hash = (ctypes.c_uint8 * 32)()
    digest_array = (ctypes.c_uint8 * len(digest)).from_buffer_copy(digest)
    lib.getTxHashFromDigest(digest_array, tx_hash)
    return tx_hash

def get_public_key_from_identity(identity: str) -> bytes:
    """
    Retrieves a public key from the provided identity string.

    Args:
        identity (str): A 60-character identity string.

    Returns:
        bytes: A 32-byte public key.

    Raises:
        ValueError: If the identity string is not exactly 60 characters long.
    """

    if len(identity) != 60:
        raise ValueError("Identity must be exactly 60 characters long.")
    public_key = (ctypes.c_uint8 * 32)()
    identity_bytes = identity.encode('utf-8')
    lib.getPublicKeyFromIdentity(identity_bytes, public_key)
    return public_key

def check_sum_identity(identity: str) -> bool:
    """
    Validates the checksum of the provided identity string.

    Args:
        identity (str): A 60-character identity string to validate.

    Returns:
        bool: True if the checksum is valid, False otherwise.

    Raises:
        ValueError: If the identity string is not exactly 60 characters long.
    """

    if len(identity) != 60:
        raise ValueError("Identity must be exactly 60 characters long.")
    identity_bytes = identity.encode('utf-8')
    return bool(lib.checkSumIdentity(identity_bytes))

def kangaroo_twelve(input: bytes, input_byte_len: int, output_byte_len: int) -> bytes:
    """
    Generates a KangarooTwelve hash from the provided input.

    Args:
        input (bytes): The input bytes for which the KangarooTwelve hash is to be computed.
        input_byte_len (int): The length of the input bytes.
        output_byte_len (int): The length of the output bytes.

    Returns:
        bytes: A bytes object representing the KangarooTwelve hash.
    """
    output = (ctypes.c_uint8 * output_byte_len)()
    input_array = (ctypes.c_uint8 * len(input)).from_buffer_copy(input)
    lib.KangarooTwelve(input_array, input_byte_len, output, output_byte_len)
    return output

def get_digest_from_siblings32(
    depth: int,
    input_bytes: bytes,
    input_byte_len: int,
    input_index: int,
    siblings: list
) -> bytes:
    """
    Computes a digest from the provided input bytes and sibling nodes.

    Args:
        depth (int): The depth of the tree.
        input_bytes (bytes): The input bytes for which the digest is to be computed.
        input_byte_len (int): The length of the input bytes.
        input_index (int): The index of the input in the tree.
        siblings (list): A list of sibling node bytes, each 32 bytes long.

    Returns:
        bytes: A 32-byte digest.

    Raises:
        ValueError: If the input bytes length does not match input_byte_len or if siblings do not match the depth and required length.
    """

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

def sign_with_nonce_k(k: bytes, public_key: bytes, message_digest: bytes) -> bytes:
    """
    Generates a signature using a nonce k, public key, and message digest.

    Args:
        k (bytes): A nonce value used in signing.
        public_key (bytes): A 32-byte public key.
        message_digest (bytes): A 32-byte message digest to sign.

    Returns:
        bytes: A 64-byte signature.
    """

    signature = (ctypes.c_uint8 * 64)()
    k_array = (ctypes.c_uint8 * len(k)).from_buffer_copy(k)
    public_key_array = (ctypes.c_uint8 * len(public_key)).from_buffer_copy(public_key)
    message_digest_array = (ctypes.c_uint8 * len(message_digest)).from_buffer_copy(message_digest)
    lib.signWithNonceK(k_array, public_key_array, message_digest_array, signature)
    return signature

def sign(subseed: bytes, public_key: bytes, message_digest: bytes) -> bytes:
    """
    Generates a signature using a subseed, public key, and message digest.

    Args:
        subseed (bytes): A 32-byte subseed used in signing.
        public_key (bytes): A 32-byte public key.
        message_digest (bytes): A 32-byte message digest to sign.

    Returns:
        bytes: A 64-byte signature.
    """

    signature = (ctypes.c_uint8 * 64)()
    subseed_array = (ctypes.c_uint8 * len(subseed)).from_buffer_copy(subseed)
    public_key_array = (ctypes.c_uint8 * len(public_key)).from_buffer_copy(public_key)
    message_digest_array = (ctypes.c_uint8 * len(message_digest)).from_buffer_copy(message_digest)
    lib.sign(subseed_array, public_key_array, message_digest_array, signature)
    return signature

def verify(public_key: bytes, message_digest: bytes, signature: bytes) -> bool:
    """
    Verifies the provided signature against the public key and message digest.

    Args:
        public_key (bytes): A 32-byte public key.
        message_digest (bytes): A 32-byte message digest.
        signature (bytes): A 64-byte signature to verify.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """

    public_key_array = (ctypes.c_uint8 * len(public_key)).from_buffer_copy(public_key)
    message_digest_array = (ctypes.c_uint8 * len(message_digest)).from_buffer_copy(message_digest)
    signature_array = (ctypes.c_uint8 * len(signature)).from_buffer_copy(signature)
    return bool(lib.verify(public_key_array, message_digest_array, signature_array))
