import hashlib

raw = str(input()).encode()

print(hashlib.md5(raw).hexdigest())
