import string

def normalize(text: str) -> str:
    """Uppercase and strip non-letters."""
    return ''.join(c for c in text.upper() if c in string.ascii_uppercase)

def encrypt(plaintext: str, key: str) -> str:
    """Encrypt using Vigenère cipher."""
    plaintext = normalize(plaintext)
    key = normalize(key)
    if not key:
        return plaintext
    
    ciphertext = []
    for i, p in enumerate(plaintext):
        k = key[i % len(key)]
        c = chr(((ord(p) - 65 + ord(k) - 65) % 26) + 65)
        ciphertext.append(c)
    return ''.join(ciphertext)

def decrypt(ciphertext: str, key: str) -> str:
    """Decrypt using Vigenère cipher."""
    ciphertext = normalize(ciphertext)
    key = normalize(key)
    if not key:
        return ciphertext
    
    plaintext = []
    for i, c in enumerate(ciphertext):
        k = key[i % len(key)]
        p = chr(((ord(c) - 65 - (ord(k) - 65)) % 26) + 65)
        plaintext.append(p)
    return ''.join(plaintext)
