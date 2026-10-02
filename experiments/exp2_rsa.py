import os
import sys
import numpy as np
import pandas as pd
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ciphers.toy_rsa import gen_keys, encrypt
from attacks.factor import trial_division, fermat, pollard_rho, recover_private_key

random.seed(42)

def run_experiment():
    print("Running RSA Factoring Experiment...")
    bit_sizes = [16, 20, 24, 28, 32, 36, 40, 44, 48]
    trials = 10
    
    results = []
    
    for bits in bit_sizes:
        print(f"Testing {bits} bits...")
        times = {'trial': [], 'fermat': [], 'rho': []}
        iters = {'trial': [], 'fermat': [], 'rho': []}
        
        for _ in range(trials):
            (e, n), (d, _) = gen_keys(bits)
            m = random.randint(2, 100)
            c = encrypt(m, (e, n))
            
            # Trial Division (timeout 2s)
            res = trial_division(n, timeout=2.0)
            if res:
                p, q, i, t = res
                times['trial'].append(t)
                iters['trial'].append(i)
                priv, decrypt = recover_private_key(n, e, p)
                assert decrypt(c) == m
                
            # Fermat (timeout 2s)
            res = fermat(n, timeout=2.0)
            if res:
                p, q, i, t = res
                times['fermat'].append(t)
                iters['fermat'].append(i)
                
            # Pollard Rho (timeout 5s)
            res = pollard_rho(n, timeout=5.0)
            if res:
                p, q, i, t = res
                times['rho'].append(t)
                iters['rho'].append(i)
                
        row = {'bits': bits}
        for method in ['trial', 'fermat', 'rho']:
            if times[method]:
                row[f'{method}_time'] = np.median(times[method])
                row[f'{method}_iters'] = np.median(iters[method])
            else:
                row[f'{method}_time'] = None
                row[f'{method}_iters'] = None
                
        results.append(row)
        
    df = pd.DataFrame(results)
    os.makedirs('data/results', exist_ok=True)
    df.to_csv('data/results/rsa_factoring.csv', index=False)
    print("Saved rsa_factoring.csv")
    
    # Extrapolation for Pollard's Rho
    rho_df = df.dropna(subset=['rho_time']).copy()
    if not rho_df.empty and len(rho_df) > 2:
        x = rho_df['bits'].values
        y = np.log2(rho_df['rho_time'].values) # log2 of time
        
        # Fit linear polynomial (degree 1)
        coeffs = np.polyfit(x, y, 1)
        poly = np.poly1d(coeffs)
        
        print("\n--- Extrapolation for Pollard's Rho ---")
        print("Note: This extrapolation applies ONLY to Pollard's Rho.")
        print("Real-world attacks against 1024+ bit RSA use the General Number Field Sieve (GNFS), which is much faster than Rho.")
        
        for bits in [512, 1024, 2048]:
            log2_t = poly(bits)
            seconds = 2**log2_t
            years = seconds / (3600 * 24 * 365)
            print(f"Bits: {bits:4d} | Extrapolated Time: 2^{log2_t:.1f} seconds (~{years:.2e} years)")
            
        extrap_df = pd.DataFrame([{'bits': b, 'extrapolated_years': (2**poly(b))/(3600*24*365)} for b in [512, 1024, 2048]])
        extrap_df.to_csv('data/results/rsa_extrapolation.csv', index=False)
        
if __name__ == '__main__':
    run_experiment()
