import os
import sys
import random
import string
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ciphers.vulnerable_check import safe_check
from attacks.timing import recover_secret
from ciphers.vigenere import encrypt
from attacks.vig_attack import break_vigenere
from collections import Counter

random.seed(42)

def run_mitigations():
    os.makedirs('data/results', exist_ok=True)
    
    # 1. Timing Mitigation
    print("Running Timing Mitigation Experiment...")
    charset = string.ascii_uppercase + "0123456789"
    secret_len = 8
    samples_list = [10, 50, 200, 1000, 5000]
    trials = 2  # Reduced from 20 because N=5000 takes over 10 minutes
    
    results = []
    
    for N in samples_list:
        correct_chars = 0
        total_chars = trials * secret_len
        for _ in range(trials):
            secret = ''.join(random.choices(charset, k=secret_len))
            oracle = lambda g: safe_check(g, secret)
            guessed = recover_secret(oracle, secret_len, charset, N)
            correct_chars += sum(1 for g, s in zip(guessed, secret) if g == s)
            
        accuracy = correct_chars / total_chars
        print(f"Safe Check Accuracy at N={N}: {accuracy:.2f} (Chance: {1/len(charset):.2f})")
        results.append({'samples': N, 'accuracy': accuracy})
        
    pd.DataFrame(results).to_csv('data/results/timing_safe_accuracy.csv', index=False)
    
    # 2. Vigenere Mitigation (One-Time Pad like)
    print("Running Vigenere Mitigation Experiment (Random key as long as plaintext)...")
    corpus_path = 'data/corpus/cleaned_english.txt'
    with open(corpus_path, 'r') as f:
        corpus = f.read()
    
    pt = corpus[:1000]
    long_key = ''.join(random.choices(string.ascii_uppercase, k=len(pt)))
    ct_long = encrypt(pt, long_key)
    
    res = break_vigenere(ct_long)
    success = (res['plaintext'] == pt)
    print(f"Break Vigenere with long random key: Success={success}")
    
    # Histograms
    print("Generating histograms data...")
    short_key = "CRYPTO"
    ct_short = encrypt(pt, short_key)
    
    hist_short = Counter(ct_short)
    hist_long = Counter(ct_long)
    
    short_df = pd.DataFrame([{'char': k, 'count': v} for k, v in hist_short.items()])
    long_df = pd.DataFrame([{'char': k, 'count': v} for k, v in hist_long.items()])
    
    short_df.to_csv('data/results/hist_short_key.csv', index=False)
    long_df.to_csv('data/results/hist_long_key.csv', index=False)

if __name__ == '__main__':
    run_mitigations()
