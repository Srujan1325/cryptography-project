import os
import sys
import random

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from ciphers.vigenere import encrypt
from attacks.vig_attack import break_vigenere
from ciphers.toy_rsa import gen_keys, encrypt as rsa_encrypt
from attacks.factor import pollard_rho, recover_private_key
from ciphers.vulnerable_check import check, safe_check
from attacks.timing import recover_secret

def main():
    print("="*50)
    print("LIVE DEMO: Cryptanalysis")
    print("="*50)
    
    # 1. Vigenere Break
    print("\n[1] Vigenere Cipher Attack")
    corpus_path = 'data/corpus/cleaned_english.txt'
    with open(corpus_path, 'r') as f:
        corpus = f.read()
    pt = corpus[:1000]
    key = "HACKED"
    ct = encrypt(pt, key)
    print(f"Key: {key}")
    res = break_vigenere(ct)
    print(f"Recovered Key: {res['key']}")
    print(f"Success: {res['key'] == key}")
    
    # 2. RSA Factoring
    print("\n[2] 40-bit RSA Factoring")
    bits = 40
    (e, n), (d, _) = gen_keys(bits)
    print(f"Generated {bits}-bit Modulus N = {n}")
    res_factor = pollard_rho(n, timeout=10.0)
    if res_factor:
        p, q, i, t = res_factor
        print(f"Factored in {t:.4f}s: p={p}, q={q}")
    else:
        print("Failed to factor in time.")
        
    # 3. Timing Attack
    print("\n[3] Timing Attack (Vulnerable Check)")
    secret = "SECURE42"
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    oracle = lambda g: check(g, secret)
    print(f"Secret: {secret}")
    guessed = recover_secret(oracle, len(secret), charset, samples=100)
    print(f"Recovered: {guessed}")
    
    # 4. Constant-Time Fix
    print("\n[4] Constant-Time Fix (Safe Check)")
    oracle_safe = lambda g: safe_check(g, secret)
    guessed_safe = recover_secret(oracle_safe, len(secret), charset, samples=100)
    print(f"Recovered (should be garbage): {guessed_safe}")

if __name__ == '__main__':
    main()
