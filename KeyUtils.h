#pragma once

#ifdef _WIN32
    #define VOID_FUNC_DECL extern "C" void __declspec(dllexport)
    #define BOOL_FUNC_DECL extern "C" bool __declspec(dllexport)
#else
    #define VOID_FUNC_DECL extern "C" void __attribute__((visibility("default")))
    #define BOOL_FUNC_DECL extern "C" bool __attribute__((visibility("default")))
#endif

BOOL_FUNC_DECL getSubseedFromSeed(const uint8_t* seed, uint8_t* subseed);
VOID_FUNC_DECL getPrivateKeyFromSubSeed(const uint8_t* seed, uint8_t* privateKey);
VOID_FUNC_DECL getPublicKeyFromPrivateKey(const uint8_t* privateKey, uint8_t* publicKey);
VOID_FUNC_DECL getIdentityFromPublicKey(const uint8_t* pubkey, char* identity, bool isLowerCase);
VOID_FUNC_DECL getTxHashFromDigest(const uint8_t* digest, char* txHash);
VOID_FUNC_DECL getPublicKeyFromIdentity(const char* identity, uint8_t* publicKey);
BOOL_FUNC_DECL checkSumIdentity(char* identity);

// Compute the digest (root hash) from siblings of Merkle tree
template <unsigned int hashByteLen>
void getDigestFromSiblings(
    unsigned int depth,
    const uint8_t *input,
    unsigned int inputByteLen,
    unsigned int inputIndex,
    const uint8_t (*siblings)[hashByteLen],
    uint8_t *output);
