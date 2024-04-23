import os

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXY"

for letter in ALPHABET:
    os.makedirs(f"../data/dataset/left/test/{letter}", exist_ok=True)
    os.makedirs(f"../data/dataset/left/train/{letter}", exist_ok=True)
    os.makedirs(f"../data/dataset/right/test/{letter}", exist_ok=True)
    os.makedirs(f"../data/dataset/right/train/{letter}", exist_ok=True)
