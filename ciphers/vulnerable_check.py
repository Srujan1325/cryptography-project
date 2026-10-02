import time
import hmac

def check(guess: str, secret: str) -> bool:
    """
    Compares byte by byte, returns False at the first mismatch.
    Adds a ~50 microsecond busy-wait to amplify the leak so Python timing noise stays manageable.
    """
    if len(guess) != len(secret):
        return False
        
    guess_bytes = guess.encode()
    secret_bytes = secret.encode()
    
    for g, s in zip(guess_bytes, secret_bytes):
        if g != s:
            return False
            
        # Busy-wait ~50 microseconds
        start = time.perf_counter_ns()
        while time.perf_counter_ns() - start < 50_000:
            pass
            
    return True

def safe_check(guess: str, secret: str) -> bool:
    """Secure constant-time comparison."""
    return hmac.compare_digest(guess.encode(), secret.encode())
