# Introduction

This repository contains the code for the KeyUtils library, which is a Python wrapper for the Qubic KeyUtils C++ library.

# Motivation

The Qubic KeyUtils library is a C++ library that provides functions for generating keys and signatures for the Qubic blockchain. It is using fourq for hash algorithm, but unfortunatly it is not implemented in Python. So for the purpose of using Qubic in Python, I implemented binding for the KeyUtils library in Python.

# Implemented Functions

- `get_subseed_from_seed`
- `get_private_key_from_subseed`
- `get_public_key_from_private_key`
- `get_identity_from_public_key`
- `get_digest_from_siblings32`
- `get_tx_hash_from_digest`
- `get_public_key_from_identity`
- `check_sum_identity`
- `sign_with_nonce_k`
- `sign`
- `verify`
- `kangaroo_twelve`

# How to build

## For Windows

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

## For Linux

1. Install build essentials

```sh
sudo apt install build-essential
```

2. Build the DLL

```sh
g++ -shared -fPIC -o KeyUtils.so KeyUtils.cpp
```

3. Check DLL functions

```sh
nm -D libKeyUtils.so
```

## For macOS

1. Build

```sh
clang++ -shared -o libKeyUtils.dylib KeyUtils.cpp
```

2. Check Lib functions

```sh
nm -g libKeyUtils.dylib
```

# For more information

- [Qubic KeyUtils](https://github.com/qubic/qubic-cli/blob/main/K12AndKeyUtil.h)
- [QubiPy Repository](https://github.com/QubiPy-Labs/QubiPy)
