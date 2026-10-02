import string
import math
from collections import Counter
from typing import Dict, List, Tuple

ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00015,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def get_ic(text: str) -> float:
    """Calculate the Index of Coincidence."""
    if len(text) < 2:
        return 0.0
    counts = Counter(text)
    n = len(text)
    ic = sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))
    return ic

def chi_squared(text: str) -> float:
    """Calculate chi-squared statistic against English frequencies."""
    if not text:
        return float('inf')
    counts = Counter(text)
    n = len(text)
    chi_sq = 0.0
    for char in string.ascii_uppercase:
        expected = ENGLISH_FREQ[char] * n
        observed = counts.get(char, 0)
        if expected > 0:
            chi_sq += ((observed - expected) ** 2) / expected
    return chi_sq

def solve_caesar(text: str) -> Tuple[int, float]:
    """Solve Caesar cipher, returning (shift, score)."""
    best_shift = 0
    best_score = float('inf')
    for shift in range(26):
        decrypted = ''.join(chr(((ord(c) - 65 - shift) % 26) + 65) for c in text)
        score = chi_squared(decrypted)
        if score < best_score:
            best_score = score
            best_shift = shift
    return best_shift, best_score

def get_factors(n: int) -> List[int]:
    factors = []
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            if i != n // i:
                factors.append(n // i)
    factors.append(n)
    return factors

def kasiski_key_length(ct: str, max_len: int = 20) -> int:
    """Estimate key length using Kasiski examination."""
    seq_spacings = {}
    for i in range(len(ct) - 2):
        seq = ct[i:i+3]
        if seq not in seq_spacings:
            next_idx = ct.find(seq, i + 3)
            if next_idx != -1:
                seq_spacings[seq] = next_idx - i
                
    if not seq_spacings:
        return 1
        
    factor_counts = Counter()
    for dist in seq_spacings.values():
        for factor in get_factors(dist):
            if factor <= max_len:
                factor_counts[factor] += 1
                
    if not factor_counts:
        return 1
    return factor_counts.most_common(1)[0][0]

def ic_key_length(ct: str, max_len: int = 20) -> int:
    """Estimate key length using Index of Coincidence."""
    best_k = 1
    best_ic = 0.0
    
    for k in range(1, max_len + 1):
        cols = [''] * k
        for i, c in enumerate(ct):
            cols[i % k] += c
            
        avg_ic = sum(get_ic(col) for col in cols) / k
        if avg_ic > 0.06:
            return k
        if avg_ic > best_ic:
            best_ic = avg_ic
            best_k = k
    return best_k

def recover_key(ct: str, k: int) -> str:
    """Recover the key given its length."""
    key = []
    cols = [''] * k
    for i, c in enumerate(ct):
        cols[i % k] += c
    for col in cols:
        shift, _ = solve_caesar(col)
        key.append(chr(shift + 65))
    return ''.join(key)

def break_vigenere(ct: str) -> dict:
    """Break Vigenere ciphertext."""
    from ciphers.vigenere import decrypt
    
    k_ic = ic_key_length(ct)
    key = recover_key(ct, k_ic)
    pt = decrypt(ct, key)
    
    return {
        'key_length': k_ic,
        'key': key,
        'plaintext': pt,
        'method_used': 'IC'
    }
