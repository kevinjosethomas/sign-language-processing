import os

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for letter in ALPHABET:
    os.makedirs(f"../data/nets/test/{letter}", exist_ok=True)
    os.makedirs(f"../data/nets/train/{letter}", exist_ok=True)
