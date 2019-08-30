# lfucache
Python 3.7 implementation of Least Frequently Used library.

## Usage

Run tests with the following:

```bash
pip install -r dev-requirements.txt
tox
```
Manual testing of the library can be perfomed via the Python 3.7 REPL:

```bash
python
>>> from lfucache.lfulib import LFUCache
>>> cache = LFUCache(2)
>>> cache.put(1, 1)
>>> cache.put(2, 2)
>>> cache.get(1)
1
>>> cache.put(3, 3)
>>> cache.get(2)
-1
>>> cache.get(3)
3
>>> cache.put(4, 4)
>>> cache.get(1)
-1
>>> cache.get(3)
3
>>> cache.get(4)
4
```
