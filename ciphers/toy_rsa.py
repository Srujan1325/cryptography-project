import sympy

def gen_keys(bits: int) -> tuple:
    """Generate (public_key, private_key) = ((e, n), (d, n))."""
    p_bits = bits // 2
    q_bits = bits - p_bits
    
    p = sympy.randprime(2**(p_bits-1), 2**p_bits - 1)
    q = sympy.randprime(2**(q_bits-1), 2**q_bits - 1)
    
    while p == q:
        q = sympy.randprime(2**(q_bits-1), 2**q_bits - 1)
        
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    if sympy.gcd(e, phi) != 1:
        e = 3
        while sympy.gcd(e, phi) != 1:
            e += 2
            
    d = sympy.mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(m: int, public_key: tuple) -> int:
    """Encrypt integer message m."""
    e, n = public_key
    return pow(m, e, n)

def decrypt(c: int, private_key: tuple) -> int:
    """Decrypt integer ciphertext c."""
    d, n = private_key
    return pow(c, d, n)
