import hashlib
import random
import ssl
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def hash_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

def hash_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest()

def hash_without_salt(password):
    return hashlib.sha256(password.encode()).hexdigest()

def weak_random_token():
    return str(random.random())

def generate_token():
    return str(random.randint(100000, 999999))

def encrypt_ecb(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)

def get_secret_key():
    return b"1234567890123456"

def create_unverified_context():
    return ssl._create_unverified_context()

def predictable_random():
    random.seed(42)
    return random.randint(1, 100)

def short_key():
    return get_random_bytes(4) 


if __name__ == "__main__":
    hash_md5("password")
    hash_sha1("password")
    hash_without_salt("password")
    weak_random_token()
    generate_token()
    encrypt_ecb(b"1234567890123456", b"1234567890123456")
    get_secret_key()
    create_unverified_context()
    predictable_random()
    short_key()
