# Introduction

This repository contains the code for the KeyUtils library, which is a Python wrapper for the Qubic KeyUtils C++ library.

# Implemented Functions

- `getSubseedFromSeed`
- `getPrivateKeyFromSubSeed`
- `getPublicKeyFromPrivateKey`
- `getIdentityFromPublicKey`
- `getDigestFromSiblings32`
- `getTxHashFromDigest`
- `getPublicKeyFromIdentity`
- `checkSumIdentity`
- `signWithNonceK`
- `sign`
- `verify`


# How to build

1. Install Python 3.10 or later
2. Install Visual Studio 2022 Community Edition
3. Set Environment Variables for `cl.exe`
4. Open a new VS2022 x64 Native Tools Command Prompt and run the following commands

```sh
cl /LD /EHsc /I. /FeKeyUtils.dll KeyUtils.cpp
```

5. Check the exports of the DLL

```sh
dumpbin -exports KeyUtils.dll
```

# For more information

- [Qubic KeyUtils](https://github.com/qubic/qubic-cli/blob/main/K12AndKeyUtil.h)
- [QubiPy Crypto Utils (Pull Request)](https://github.com/QubiPy-Labs/QubiPy/pull/3)