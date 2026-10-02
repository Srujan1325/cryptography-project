# Summary Table

| System | Attacker Model | Attack | Measured Cost | Result | Mitigation | Mitigation Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Vigenère Cipher | Ciphertext-only | Index of Coincidence + Chi-Squared | ~O(k_max * N) | Exactly recovers key and plaintext (success ~1.0 for len 1000+) | Key as long as plaintext (One-Time Pad) | Success drops to ~0.0; frequency becomes uniform |
| Toy RSA (16-48 bit) | Public Key-only | Pollard's Rho Factoring | ~O(sqrt(p)) steps | Fully factors 48-bit modulus in fractions of a second | Increase key size (2048+ bits), OAEP padding | Factoring becomes computationally infeasible (~years) |
| Early-Exit String Check | Side-Channel (Timing) | Character-by-Character Timing Attack | Length * Charset * Samples | Recovers secret exactly (accuracy ~1.0) with high N (e.g., N=1000) | Constant-time comparison (`hmac.compare_digest`) | Accuracy drops to random chance (~1/36) |

# Key-Space Analysis

| System | Key Space Size (Theoretical) | Effective Security (Bits) |
| :--- | :--- | :--- |
| Caesar Cipher | 26 | ~4.7 bits |
| Vigenère Cipher | $26^k$ | ~$4.7k$ bits |
| Toy RSA (48-bit) | $\approx 2^{48}$ | Extrapolated from Rho cost, much lower than 48 |
| Timing Vulnerability | $C^L$ (e.g., $36^8$) | $C \times L \times N$ (e.g., $36 \times 8 \times 1000 \approx 288,000$ queries) |
