# How to build

1. Install Visual Studio 2022 Community Edition
2. Set Environment Variables for `cl.exe`

```
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64
```

```sh
vcvarsall.bat x64
```

```sh
cl /LD /EHsc /I. /FeKeyUtils.dll KeyUtils.cpp
```



```sh
pip install -r Cython
```

```sh
python setup.py build_ext --inplace
```

```sh
dumpbin -exports KeyUtils.dll
```