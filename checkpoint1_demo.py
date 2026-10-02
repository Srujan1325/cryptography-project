import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ciphers.vigenere import encrypt
from attacks.vig_attack import break_vigenere

def main():
    print("=== CHECKPOINT 1 DEMO: VIGENERE BREAK ===")
    corpus_path = 'data/corpus/cleaned_english.txt'
    with open(corpus_path, 'r') as f:
        corpus = f.read()
        
    pt = corpus[:1000]
    key = "CRYPTO"
    print(f"Original Text (first 50 chars): {pt[:50]}...")
    print(f"True Key: {key}")
    
    ct = encrypt(pt, key)
    print(f"Ciphertext (first 50 chars): {ct[:50]}...")
    print("\nRunning break_vigenere...")
    
    result = break_vigenere(ct)
    
    print("\n--- RESULTS ---")
    print(f"Detected Key Length: {result['key_length']}")
    print(f"Recovered Key: {result['key']}")
    print(f"Recovered Text (first 50 chars): {result['plaintext'][:50]}...")
    print(f"Correctness: {result['key'] == key}")
    
if __name__ == '__main__':
    main()
