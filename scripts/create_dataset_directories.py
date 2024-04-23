import os

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXY"

for letter in ALPHABET:
    os.makedirs(f"../data/merged/{letter}", exist_ok=True)
