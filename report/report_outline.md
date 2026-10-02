# Cryptanalysis / Security Analysis Report

## 1. Introduction and Objectives
This project demonstrates and quantifies attacks on deliberately weak cryptographic systems. The objective is to understand cryptographic failures in practice by exploiting them on toy implementations, measuring the cost of these attacks, and proving the effectiveness of standard mitigations.

## 2. Background
- **Vigenère Cipher**: A polyalphabetic substitution cipher. Breaks when key length is discovered, reducing it to multiple Caesar ciphers.
- **RSA**: An asymmetric cryptosystem based on integer factorization. Breaks when the public modulus $N$ can be factored.
- **Timing Side Channels**: Exploits variations in execution time to infer secret data. Occurs often in naive string comparisons that exit early on a mismatch.

## 3. Threat Model
- **Vigenère**: Ciphertext-only attack. The attacker possesses intercepted ciphertext and knows the language (English).
- **RSA**: Public-key-only. The attacker has $N$ and $e$.
- **Timing Attack**: Chosen-ciphertext/oracle. Attacker can submit arbitrary guesses and precisely measure response times.

## 4. Implementation and Methodology
All attacks target local Python implementations. Random seeds are fixed to `42` for reproducibility.
- **Vigenère Break**: Uses Index of Coincidence to determine key length, followed by Chi-Squared scoring against English letter frequencies.
- **RSA Break**: Compares Trial Division, Fermat, and Pollard's Rho factoring.
- **Timing Break**: Submits character guesses and measures median time (over $N$ samples) using `time.perf_counter_ns()`.

## 5. Attack Results
### 5.1 Vigenère Cipher
The attack reliably cracks keys of length up to 10 characters given 1000 characters of ciphertext. Success rate nears 100%. (Reference: `vigenere_success.png`, `vigenere_ic.png`).

### 5.2 Toy RSA
Pollard's Rho dramatically outperformed Trial Division and Fermat. 48-bit moduli were factored in fractions of a second. (Reference: `rsa_factoring.png`).

### 5.3 Timing Attack
With $N=1000$ samples per guess, the 8-character secret (from a 36-character set) was reliably recovered, reaching near 1.0 accuracy. (Reference: `timing_attack.png`).

## 6. Security Quantification and Extrapolation
- **Caesar**: 26 keys.
- **Vigenère (k=6)**: $26^6 \approx 3 \times 10^8$.
- **RSA Extrapolation**: Pollard's Rho scales exponentially. Extrapolating the log-linear fit to 1024 bits yields an infeasible number of years for Rho alone.
- **Timing**: Reduced the search space of $36^8$ to $36 \times 8 = 288$ character tests, multiplied by $N$ samples.

## 7. Mitigations and their Measured Effect
- **Vigenère**: Using a random key as long as the plaintext (One-Time Pad approximation). Result: Success rate dropped to 0%, histogram flattened.
- **RSA**: Increasing modulus size to 2048 bits and using OAEP padding prevents basic integer factorization and padding oracle attacks.
- **Timing**: Swapping the vulnerable check for `hmac.compare_digest()`. Result: Attack accuracy dropped to ~1/36 (random chance).

## 8. Limitations
- Experiments used small, toy sizes for runtime reasons.
- Python introduces significant timing noise, necessitating an artificial ~50µs delay in the vulnerable oracle to simulate network/system jitter reliably.
- Real RSA attacks use General Number Field Sieve (GNFS), not Pollard's Rho.

## 9. Conclusion
The project successfully demonstrated that theoretical cryptographic flaws lead to practical exploits. Mitigations must address the root mathematical vulnerabilities (small key spaces, predictable patterns) and implementation flaws (side channels).

## 10. References
- Kocher, P. (1996). Timing Attacks on Implementations of Diffie-Hellman, RSA, DSS, and Other Systems.
- Pollard, J. M. (1975). A Monte Carlo method for factorization.
- Kasiski, F. W. (1863). Die Geheimschriften und die Dechiffrir-Kunst.
