import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_vigenere():
    os.makedirs('plots', exist_ok=True)
    
    # 1. Success Rate Plot
    df = pd.read_csv('data/results/vigenere_success.csv')
    plt.figure(figsize=(8, 6))
    for k_len in df['key_length'].unique():
        sub_df = df[df['key_length'] == k_len]
        plt.plot(sub_df['text_length'], sub_df['success_rate'], marker='o', label=f'Key Len = {k_len}')
    
    plt.title('Vigenère Cipher Attack Success Rate')
    plt.xlabel('Ciphertext Length (characters)')
    plt.ylabel('Success Rate (exact key recovery)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/vigenere_success.png', dpi=300)
    plt.close()
    
    # 2. IC vs K Plot
    ic_df = pd.read_csv('data/results/vigenere_ic.csv')
    plt.figure(figsize=(8, 6))
    plt.plot(ic_df['k'], ic_df['ic'], marker='s', color='purple')
    plt.axhline(y=0.066, color='r', linestyle='--', label='Expected English IC (~0.066)')
    plt.axhline(y=0.038, color='k', linestyle=':', label='Expected Random IC (~0.038)')
    
    true_k = 6 # Set in exp1
    plt.axvline(x=true_k, color='g', linestyle='-.', label=f'True Key Length ({true_k})')
    
    plt.title('Index of Coincidence vs. Guessed Key Length')
    plt.xlabel('Guessed Key Length (k)')
    plt.ylabel('Average Index of Coincidence')
    plt.xticks(range(1, 21))
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/vigenere_ic.png', dpi=300)
    plt.close()
    
    # 3. RSA Log-Scale Plot
    if os.path.exists('data/results/rsa_factoring.csv'):
        rsa_df = pd.read_csv('data/results/rsa_factoring.csv')
        plt.figure(figsize=(8, 6))
        for method in ['trial', 'fermat', 'rho']:
            col = f'{method}_time'
            if col in rsa_df.columns:
                sub_df = rsa_df.dropna(subset=[col])
                if not sub_df.empty:
                    plt.plot(sub_df['bits'], np.log2(sub_df[col]), marker='o', label=method.capitalize())
                    
        # Add extrapolation line for rho
        rho_df = rsa_df.dropna(subset=['rho_time'])
        if not rho_df.empty and len(rho_df) > 2:
            x = rho_df['bits'].values
            y = np.log2(rho_df['rho_time'].values)
            coeffs = np.polyfit(x, y, 1)
            poly = np.poly1d(coeffs)
            x_ext = np.linspace(min(x), max(x) + 10, 50)
            plt.plot(x_ext, poly(x_ext), 'k--', label='Rho Extrapolation')

        plt.title('RSA Factoring Time (Log Scale)')
        plt.xlabel('Modulus Size (bits)')
        plt.ylabel('Log2(Time in seconds)')
        plt.legend()
        plt.grid(True)
        plt.savefig('plots/rsa_factoring.png', dpi=300)
        plt.close()
        
    # 4. Timing Attack Plot
    if os.path.exists('data/results/timing_accuracy.csv') and os.path.exists('data/results/timing_safe_accuracy.csv'):
        t_df = pd.read_csv('data/results/timing_accuracy.csv')
        ts_df = pd.read_csv('data/results/timing_safe_accuracy.csv')
        plt.figure(figsize=(8, 6))
        plt.plot(t_df['samples'], t_df['accuracy'], marker='o', color='red', label='Vulnerable Check')
        plt.plot(ts_df['samples'], ts_df['accuracy'], marker='s', color='green', label='Safe Check (Mitigated)')
        plt.axhline(y=1/36, color='k', linestyle='--', label='Random Chance')
        
        plt.title('Timing Attack Accuracy vs Samples per Guess')
        plt.xlabel('Samples per guess (N)')
        plt.ylabel('Accuracy (fraction of correct chars)')
        plt.legend()
        plt.grid(True)
        plt.savefig('plots/timing_attack.png', dpi=300)
        plt.close()
        
    print("All plots generated in plots/")

if __name__ == '__main__':
    plot_vigenere()

