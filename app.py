import streamlit as st
import time
import string

# Import existing project modules
from ciphers.vigenere import encrypt as vig_enc, decrypt as vig_dec
from attacks.vig_attack import break_vigenere
from ciphers.toy_rsa import gen_keys, encrypt as rsa_enc, decrypt as rsa_dec
from attacks.factor import pollard_rho
from ciphers.vulnerable_check import check, safe_check
from attacks.timing import recover_secret

# Configure the Streamlit page
st.set_page_config(page_title="Cryptanalysis Project", layout="centered")

st.title("Cryptanalysis & Security Evaluation")
st.markdown("A practical demonstration of cryptographic vulnerabilities and their mitigations.")

# Use tabs for minimal design
tab1, tab2, tab3 = st.tabs(["Vigenère Cipher", "Toy RSA", "Timing Side-Channel"])

# --- TAB 1: VIGENÈRE CIPHER ---
with tab1:
    st.header("Vigenère Cipher (Classical)")
    st.markdown("The Vigenère cipher is vulnerable to frequency analysis (Index of Coincidence and Kasiski examination).")
    
    col1, col2 = st.columns(2)
    with col1:
        plaintext = st.text_area("Plaintext", value="THIS IS A SECRET MESSAGE THAT NEEDS TO BE ENCRYPTED AND WE NEED IT LONG ENOUGH FOR FREQUENCY ANALYSIS TO WORK PROPERLY SO HERE ARE EXTRA WORDS")
        key = st.text_input("Encryption Key", value="HACK")
    
    with col2:
        if st.button("Encrypt & Attack"):
            # Clean plaintext (assuming simple A-Z)
            pt_clean = "".join(c.upper() for c in plaintext if c.isalpha())
            key_clean = "".join(c.upper() for c in key if c.isalpha())
            
            if not pt_clean or not key_clean:
                st.error("Please provide valid alphabetic text and key.")
            else:
                ct = vig_enc(pt_clean, key_clean)
                st.text_area("Ciphertext", value=ct, height=100)
                
                st.subheader("Attacker's View")
                with st.spinner("Analyzing ciphertext frequencies..."):
                    result = break_vigenere(ct)
                    
                st.success(f"**Recovered Key:** {result['key']}")
                st.info(f"**Key Length Guessed:** {result['key_length']} (via {result['method_used']})")
                st.text_area("Recovered Plaintext", value=result['plaintext'], height=100)
                
                if result['key'] == key_clean:
                    st.success("Attack Successful!")
                else:
                    st.warning("Attack Failed. The ciphertext might be too short for reliable frequency analysis.")

# --- TAB 2: TOY RSA ---
with tab2:
    st.header("Toy RSA Factoring (Asymmetric)")
    st.markdown("Small RSA moduli can be factored rapidly using algorithms like Pollard's Rho.")
    
    bits = st.slider("RSA Modulus Size (bits)", min_value=16, max_value=48, value=32, step=4)
    
    if st.button("Generate Keys & Factor"):
        with st.spinner(f"Generating {bits}-bit RSA keys..."):
            pub, priv = gen_keys(bits)
            n, e = pub
            n, d = priv
            
        st.code(f"Public Modulus (N): {n}\nPublic Exponent (e): {e}")
        
        st.subheader("Attacker's View")
        st.markdown(f"Attempting to factor $N = {n}$ using Pollard's Rho...")
        
        start_time = time.time()
        with st.spinner("Factoring..."):
            res = pollard_rho(n)
        elapsed = time.time() - start_time
        
        if res:
            p, q, iters, _ = res
            st.success(f"**Factored successfully in {elapsed:.4f} seconds!**")
            st.code(f"p = {p}\nq = {q}\nIterations: {iters}")
        else:
            st.error("Failed to factor (timeout).")

# --- TAB 3: TIMING SIDE-CHANNEL ---
with tab3:
    st.header("Timing Side-Channel (Implementation)")
    st.markdown("An early-exit string comparison leaks the secret character-by-character through execution time.")
    
    secret = st.text_input("Secret String (4-6 chars recommended for demo)", value="PASS", max_chars=8)
    secret = secret.upper()
    
    if st.button("Launch Timing Attack"):
        charset = string.ascii_uppercase
        
        st.subheader("Attack on Vulnerable Function")
        st.markdown("The attacker only has access to a function that returns True/False. They are measuring the time it takes to return.")
        
        # We use a small N for the web demo so it doesn't block forever
        N = 10 
        
        # Placeholder for dynamic output
        output = st.empty()
        
        def demo_oracle(guess):
            return check(guess, secret)
            
        with st.spinner(f"Running Timing Attack (N={N} samples per guess)..."):
            # We will rewrite the timing loop here slightly to update the UI
            recovered = []
            for pos in range(len(secret)):
                best_char = 'A'
                max_time = -1
                
                for candidate in charset:
                    filler = 'A' * (len(secret) - pos - 1)
                    guess = "".join(recovered) + candidate + filler
                    
                    # Take N samples
                    times = []
                    for _ in range(N):
                        start = time.perf_counter_ns()
                        demo_oracle(guess)
                        times.append(time.perf_counter_ns() - start)
                    
                    # Use median
                    times.sort()
                    median_time = times[len(times)//2]
                    
                    if median_time > max_time:
                        max_time = median_time
                        best_char = candidate
                        
                recovered.append(best_char)
                output.code("Recovering: " + "".join(recovered) + ("*" * (len(secret) - len(recovered))))
                
        if "".join(recovered) == secret:
            st.success(f"Successfully recovered the secret: **{''.join(recovered)}**")
        else:
            st.error(f"Failed. Recovered: {''.join(recovered)}")
            
        st.divider()
        st.subheader("Mitigation: Constant-Time Comparison")
        st.markdown("If we swap to a constant-time check (`hmac.compare_digest`), the timing leak vanishes.")
        st.info("Run `python3 experiments/exp4_mitigations.py` in the terminal to see the statistical proof over thousands of trials!")
