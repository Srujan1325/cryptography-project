import pytest
import string
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ciphers.vigenere import encrypt, decrypt
from ciphers.toy_rsa import gen_keys, encrypt as rsa_encrypt, decrypt as rsa_decrypt

def test_vigenere_round_trip():
    pt = "HELLOWORLD"
    key = "KEY"
    ct = encrypt(pt, key)
    assert decrypt(ct, key) == pt

def test_vigenere_caesar_case():
    pt = "ABC"
    key = "B" # Shift 1
    assert encrypt(pt, key) == "BCD"
    assert decrypt("BCD", key) == "ABC"

def test_rsa_round_trip():
    for _ in range(20):
        bits = 32
        pub, priv = gen_keys(bits)
        m = random.randint(1, 1000)
        c = rsa_encrypt(m, pub)
        assert rsa_decrypt(c, priv) == m
