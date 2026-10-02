import os
import random
import string
import pandas as pd
import sys

# Add parent directory to path so we can import from ciphers and attacks
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.vigenere import encrypt
from attacks.vig_attack import break_vigenere, get_ic

random.seed(42)

def generate_random_key(length: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def run_experiment():
    print("Running Vigenere Experiment...")
    # Assuming run from crypto-analysis root
    corpus_path = 'data/corpus/cleaned_english.txt'
    with open(corpus_path, 'r') as f:
        corpus = f.read()

    lengths = [100, 300, 500, 1000, 3000]
    key_lengths = [3, 6, 10]
    trials = 50

    results = []

    for k_len in key_lengths:
        for l in lengths:
            success_count = 0
            for _ in range(trials):
                start = random.randint(0, len(corpus) - l - 1)
                pt = corpus[start:start+l]
                
                key = generate_random_key(k_len)
                ct = encrypt(pt, key)
                
                res = break_vigenere(ct)
                if res['key'] == key:
                    success_count += 1
            
            rate = success_count / trials
            print(f"Key Length: {k_len:2d} | Text Length: {l:4d} | Success Rate: {rate:.2f}")
            results.append({
                'key_length': k_len,
                'text_length': l,
                'success_rate': rate
            })
            
    print("Generating IC vs K curve data...")
    pt = corpus[:1000]
    key = generate_random_key(6)
    ct = encrypt(pt, key)
    
    ic_data = []
    for k in range(1, 21):
        cols = [''] * k
        for i, c in enumerate(ct):
            cols[i % k] += c
        avg_ic = sum(get_ic(col) for col in cols) / k
        ic_data.append({'k': k, 'ic': avg_ic})
        
    os.makedirs('data/results', exist_ok=True)
    pd.DataFrame(results).to_csv('data/results/vigenere_success.csv', index=False)
    pd.DataFrame(ic_data).to_csv('data/results/vigenere_ic.csv', index=False)
    print("Results saved to data/results/.")

if __name__ == '__main__':
    run_experiment()
