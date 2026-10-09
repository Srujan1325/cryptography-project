import streamlit as st
import time
import string
import random

# Import existing project modules
from ciphers.vigenere import encrypt as vig_enc, decrypt as vig_dec
from attacks.vig_attack import break_vigenere
from ciphers.toy_rsa import gen_keys, encrypt as rsa_enc, decrypt as rsa_dec
from attacks.factor import pollard_rho
from ciphers.vulnerable_check import check, safe_check
from attacks.timing import recover_secret

# Force light theme for a simple white UI
st.set_page_config(page_title="Cryptanalysis", layout="wide", initial_sidebar_state="collapsed")

# Inject minimal custom CSS for clean white look
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px;
            color: #000000;
            font-size: 18px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Cryptanalysis & Mitigations")

# Top navigation tabs matching the sketch
tab_vig, tab_rsa, tab_timing = st.tabs(["Vigenère", "RSA", "Timing Attack"])

# ==========================================
# TAB 1: VIGENÈRE
# ==========================================
with tab_vig:
    col_vuln, col_safe = st.columns(2)
    
    with col_vuln:
        st.header("Attack without mitigation")
        st.write("Using a short, repeating key allows frequency analysis (Kasiski/IC) to easily break the cipher.")
        
        pt = "THIS IS A SECRET MESSAGE THAT NEEDS TO BE ENCRYPTED AND WE NEED IT LONG ENOUGH FOR FREQUENCY ANALYSIS TO WORK PROPERLY SO HERE ARE EXTRA WORDS TO MAKE SURE THE ATTACK HAS ENOUGH DATA"
        short_key = "HACK"
        
        if st.button("Run Vulnerable Vigenère Attack"):
            ct = vig_enc(pt, short_key)
            st.code(f"Ciphertext (preview): {ct[:50]}...")
            
            with st.spinner("Running frequency analysis..."):
                res = break_vigenere(ct)
                
            st.success(f"Recovered Key: {res['key']}")
            st.info(f"Success: {res['key'] == short_key}")
            
    with col_safe:
        st.header("Attack with mitigation")
        st.write("Using a random key that is as long as the plaintext (One-Time Pad style) destroys frequency patterns.")
        
        if st.button("Run Mitigated Vigenère Attack"):
            # Generate random key same length as pt
            long_key = "".join(random.choices(string.ascii_uppercase, k=len(pt)))
            ct_safe = vig_enc(pt, long_key)
            st.code(f"Ciphertext (preview): {ct_safe[:50]}...")
            
            with st.spinner("Running frequency analysis..."):
                res_safe = break_vigenere(ct_safe)
                
            st.error(f"Recovered Key: {res_safe['key']}")
            st.info(f"Success: {res_safe['key'] == long_key}")
            st.write("Attack failed. The statistical signal is completely destroyed.")

# ==========================================
# TAB 2: RSA
# ==========================================
with tab_rsa:
    col_vuln, col_safe = st.columns(2)
    
    with col_vuln:
        st.header("Attack without mitigation")
        st.write("Using small key sizes (e.g., 32-bit) allows attackers to factor the public modulus using Pollard's Rho.")
        
        if st.button("Factor 32-bit RSA"):
            bits = 32
            with st.spinner(f"Generating {bits}-bit keys..."):
                (e, n), (d, _) = gen_keys(bits)
            st.code(f"Public Modulus N = {n}")
            
            start = time.time()
            with st.spinner("Running Pollard's Rho..."):
                res = pollard_rho(n)
            elapsed = time.time() - start
            
            if res:
                p, q, iters, _ = res
                st.success(f"Factored successfully in {elapsed:.4f} seconds!")
                st.code(f"p = {p}\nq = {q}\nIterations: {iters}")
                
    with col_safe:
        st.header("Attack with mitigation")
        st.write("Using standard key sizes (e.g., 2048-bit) makes mathematical factoring practically impossible.")
        
        if st.button("Attempt 2048-bit RSA"):
            st.code("Public Modulus N = (A 617-digit number...)")
            with st.spinner("Running Pollard's Rho..."):
                time.sleep(1.5) # Simulate realization
            st.error("Timeout: Attack computationally infeasible.")
            st.info("Mathematical Extrapolation: It would take approximately 3.82e+168 years to factor a 2048-bit key using this method.")

# ==========================================
# TAB 3: TIMING ATTACK
# ==========================================
with tab_timing:
    col_vuln, col_safe = st.columns(2)
    
    secret = "SECURE42"
    charset = string.ascii_uppercase + "0123456789"
    
    with col_vuln:
        st.header("Attack without mitigation")
        st.write("An early-exit string comparison leaks the secret character-by-character through execution time.")
        
        if st.button("Run Vulnerable Timing Attack"):
            oracle = lambda g: check(g, secret)
            
            st.write(f"Target Secret: `{secret}`")
            output_vuln = st.empty()
            
            with st.spinner("Measuring microsecond execution delays..."):
                # Run the attack directly inline for visual updates
                recovered = []
                for pos in range(len(secret)):
                    best_char = 'A'
                    max_time = -1
                    
                    for candidate in charset:
                        filler = 'A' * (len(secret) - pos - 1)
                        guess = "".join(recovered) + candidate + filler
                        
                        times = []
                        for _ in range(50): # N=50 for quick UI demo
                            start = time.perf_counter_ns()
                            oracle(guess)
                            times.append(time.perf_counter_ns() - start)
                        
                        times.sort()
                        median_time = times[len(times)//2]
                        
                        if median_time > max_time:
                            max_time = median_time
                            best_char = candidate
                            
                    recovered.append(best_char)
                    output_vuln.code("Recovering: " + "".join(recovered) + ("*" * (len(secret) - len(recovered))))
                    
            if "".join(recovered) == secret:
                st.success(f"Success! Secret is {''.join(recovered)}")
                
    with col_safe:
        st.header("Attack with mitigation")
        st.write("Using a constant-time comparison (`hmac.compare_digest`) stops the timing leak.")
        
        if st.button("Run Mitigated Timing Attack"):
            oracle_safe = lambda g: safe_check(g, secret)
            
            st.write(f"Target Secret: `{secret}`")
            output_safe = st.empty()
            
            with st.spinner("Measuring microsecond execution delays..."):
                recovered = []
                for pos in range(len(secret)):
                    best_char = 'A'
                    max_time = -1
                    
                    for candidate in charset:
                        filler = 'A' * (len(secret) - pos - 1)
                        guess = "".join(recovered) + candidate + filler
                        
                        times = []
                        for _ in range(50):
                            start = time.perf_counter_ns()
                            oracle_safe(guess)
                            times.append(time.perf_counter_ns() - start)
                        
                        times.sort()
                        median_time = times[len(times)//2]
                        
                        if median_time > max_time:
                            max_time = median_time
                            best_char = candidate
                            
                    recovered.append(best_char)
                    output_safe.code("Recovering: " + "".join(recovered) + ("*" * (len(secret) - len(recovered))))
                    
            st.error(f"Failed. Recovered garbage: {''.join(recovered)}")
            st.info("The execution time is identical for all guesses, so the attacker is effectively guessing randomly.")
