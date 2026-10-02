import os
import sys
import random
import string
import time
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ciphers.vulnerable_check import check
from attacks.timing import recover_secret

random.seed(42)

def run_experiment():
    print("Running Timing Attack Experiment...")
    charset = string.ascii_uppercase + "0123456789" # 36 chars
    secret_len = 8
    
    samples_list = [10, 50, 200, 1000, 5000]
    trials = 20
    
    results = []
    
    for N in samples_list:
        print(f"Testing with N={N} samples per guess...")
        correct_chars_total = 0
        total_chars_attempted = trials * secret_len
        
        for _ in range(trials):
            secret = ''.join(random.choices(charset, k=secret_len))
            oracle = lambda g: check(g, secret)
            
            guessed = recover_secret(oracle, secret_len, charset, N)
            
            correct = sum(1 for g, s in zip(guessed, secret) if g == s)
            correct_chars_total += correct
            
        accuracy = correct_chars_total / total_chars_attempted
        print(f"Accuracy at N={N}: {accuracy:.2f}")
        results.append({'samples': N, 'accuracy': accuracy})
        
    os.makedirs('data/results', exist_ok=True)
    pd.DataFrame(results).to_csv('data/results/timing_accuracy.csv', index=False)
    
    # Save median timing for one position to show the leak signal
    print("Generating single-position leak signal data...")
    secret = "CRYPTO42"
    pos = 0 # Testing the first character
    candidate_timings = []
    oracle = lambda g: check(g, secret)
    
    for candidate in charset:
        guess = candidate + 'A' * 7
        t = []
        for _ in range(1000):
            start = time.perf_counter_ns()
            oracle(guess)
            end = time.perf_counter_ns()
            t.append(end - start)
        candidate_timings.append({'char': candidate, 'median_time_ns': np.median(t)})
        
    pd.DataFrame(candidate_timings).to_csv('data/results/timing_signal.csv', index=False)
    print("Saved timing results.")

if __name__ == '__main__':
    run_experiment()
