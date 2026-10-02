import pytest
import sys
import os
import random
import string

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attacks.vig_attack import get_ic, break_vigenere
from ciphers.vigenere import encrypt

def test_ic_values():
    # English IC should be ~0.066
    english_text = "THISISASAMPLEENGLISHTEXTTOCHECKTHEINDEXOFCOINCIDENCEITSHOULDBEAROUNDZEROSIXSIX"
    eng_ic = get_ic(english_text)
    assert 0.05 < eng_ic < 0.09
    
    # Random text IC should be ~0.038
    random.seed(42)
    random_text = ''.join(random.choices(string.ascii_uppercase, k=1000))
    rand_ic = get_ic(random_text)
    assert 0.03 < rand_ic < 0.05

def test_full_attack():
    corpus_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/corpus/cleaned_english.txt')
    if not os.path.exists(corpus_path):
        pytest.skip("Corpus not available")
        
    with open(corpus_path, 'r') as f:
        corpus = f.read()
        
    pt = corpus[:1000]
    key = "SECRET"
    ct = encrypt(pt, key)
    
    res = break_vigenere(ct)
    assert res['key'] == key
    assert res['plaintext'] == pt
