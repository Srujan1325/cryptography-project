# Presentation Slides Outline

## Slide 1: Title
- **Cryptanalysis & Security Analysis**
- Attack and Evaluate
- Date / Presenter

## Slide 2: Objectives
- Demonstrate practical attacks on three vulnerable systems.
- Quantify the cost and success rate of attacks.
- Prove the effectiveness of standard mitigations.

## Slide 3: Vigenère Cipher (Classical)
- **Vulnerability**: Frequency analysis & Index of Coincidence.
- **Attack Demo**: Broke a 6-character key from 1000 characters of ciphertext.
- **Mitigation**: Random key as long as plaintext (OTP).

## Slide 4: Toy RSA (Asymmetric)
- **Vulnerability**: Small modulus (16-48 bits).
- **Attack Demo**: Pollard's Rho factoring in <1 second.
- **Extrapolation**: Show the exponential curve and why 2048-bit is used.

## Slide 5: Timing Side Channel (Implementation)
- **Vulnerability**: Early-exit byte-by-byte string comparison.
- **Attack Demo**: Character-by-character timing oracle attack ($36^8 \to 288 \times N$).
- **Mitigation**: Constant-time `hmac.compare_digest`.

## Slide 6: Security Quantification
- Present Summary Table from report.
- Highlight the difference between theoretical key space and effective security.

## Slide 7: Lessons Learned
- Algorithms must be mathematically sound (AES, large RSA).
- Implementations must be side-channel free.
- "Don't roll your own crypto" applies to both algorithm design and coding.

## Slide 8: Q&A
- Open floor for questions.
