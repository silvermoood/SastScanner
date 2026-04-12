import hashlib
import os

user = input("Enter password: ")

h = hashlib.md5(user.encode())
os.system(user)
