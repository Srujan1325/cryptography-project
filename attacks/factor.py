import time
import math
import sympy
from typing import Optional, Tuple

def trial_division(n: int, timeout: float = 2.0) -> Optional[Tuple[int, int, int, float]]:
    """Trial division factoring with timeout."""
    start_time = time.perf_counter()
    iterations = 0
    limit = int(math.sqrt(n)) + 1
    
    # Check 2 first
    if n % 2 == 0:
        return (2, n // 2, 1, time.perf_counter() - start_time)
        
    for i in range(3, limit, 2):
        iterations += 1
        if n % i == 0:
            return (i, n // i, iterations, time.perf_counter() - start_time)
        if time.perf_counter() - start_time > timeout:
            return None
    return None

def fermat(n: int, timeout: float = 2.0) -> Optional[Tuple[int, int, int, float]]:
    """Fermat factorization method."""
    start_time = time.perf_counter()
    if n % 2 == 0:
        return (2, n // 2, 1, time.perf_counter() - start_time)
        
    a = math.isqrt(n)
    if a * a == n:
        return (a, a, 1, time.perf_counter() - start_time)
        
    a += 1
    b2 = a * a - n
    iterations = 0
    
    while True:
        iterations += 1
        b = math.isqrt(b2)
        if b * b == b2:
            return (a - b, a + b, iterations, time.perf_counter() - start_time)
        a += 1
        b2 = a * a - n
        
        if time.perf_counter() - start_time > timeout:
            return None

def pollard_rho(n: int, timeout: float = 5.0) -> Optional[Tuple[int, int, int, float]]:
    """Pollard's rho algorithm."""
    start_time = time.perf_counter()
    if n % 2 == 0:
        return (2, n // 2, 1, time.perf_counter() - start_time)
        
    x = 2
    y = 2
    d = 1
    c = 1
    iterations = 0
    
    f = lambda val: (val**2 + c) % n
    
    while d == 1:
        iterations += 1
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        
        if d == n:
            # cycle detected, change c and restart
            x = 2
            y = 2
            c += 1
            d = 1
            
        if time.perf_counter() - start_time > timeout:
            return None
            
    return (d, n // d, iterations, time.perf_counter() - start_time)

def recover_private_key(n: int, e: int, p: int) -> tuple:
    """Recover private key and return a decrypt function to verify."""
    q = n // p
    phi = (p - 1) * (q - 1)
    d = sympy.mod_inverse(e, phi)
    
    def decrypt(c: int) -> int:
        return pow(c, d, n)
        
    return (d, n), decrypt
