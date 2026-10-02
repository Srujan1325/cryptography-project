import time
import numpy as np

def recover_secret(oracle, length: int, charset: str, samples: int) -> str:
    """Recover secret character by character using timing attacks."""
    recovered = []
    
    for pos in range(length):
        best_char = 'A'
        max_time = -1
        
        # To avoid early length check failure in the oracle, pad the guess
        # to the correct total length.
        # Format: [already_recovered] + [guess] + [filler]
        for candidate in charset:
            filler = 'A' * (length - pos - 1)
            guess = ''.join(recovered) + candidate + filler
            
            timings = []
            for _ in range(samples):
                start = time.perf_counter_ns()
                oracle(guess)
                end = time.perf_counter_ns()
                timings.append(end - start)
                
            median_time = np.median(timings)
            
            if median_time > max_time:
                max_time = median_time
                best_char = candidate
                
        recovered.append(best_char)
        
    return ''.join(recovered)
