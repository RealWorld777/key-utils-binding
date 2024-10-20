#pragma once
extern "C"  bool __declspec(dllexport) getSubseedFromSeed(const uint8_t* seed, uint8_t* subseed);
extern "C"  void __declspec(dllexport) getPrivateKeyFromSubSeed(const uint8_t* seed, uint8_t* privateKey);
extern "C"  void __declspec(dllexport) getPublicKeyFromPrivateKey(const uint8_t* privateKey, uint8_t* publicKey);
extern "C"  void __declspec(dllexport) getIdentityFromPublicKey(const uint8_t* pubkey, char* identity, bool isLowerCase);
extern "C"  void __declspec(dllexport) getTxHashFromDigest(const uint8_t* digest, char* txHash);
extern "C"  void __declspec(dllexport) getPublicKeyFromIdentity(const char* identity, uint8_t* publicKey);
extern "C"  bool __declspec(dllexport) checkSumIdentity(char* identity);

// Compute the digest (root hash) from siblings of Merkle tree
template <unsigned int hashByteLen>
void getDigestFromSiblings(
    unsigned int depth,
    const uint8_t *input,
    unsigned int inputByteLen,
    unsigned int inputIndex,
    const uint8_t (*siblings)[hashByteLen],
    uint8_t *output);
