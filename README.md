# Cryptanalysis / Security Analysis Project

This project demonstrates practical attacks on intentionally weak cryptographic implementations, measures their performance, and verifies standard mitigations.

## Repository Layout
- `ciphers/`: Victim implementations (Vigenère, Toy RSA, Vulnerable String Check).
- `attacks/`: Attack scripts (Frequency Analysis, Factoring, Timing).
- `experiments/`: Scripts that generate the dataset by running attacks many times.
- `plotting/`: Scripts to generate visualizations from the results.
- `data/`: Raw corpus and generated CSV results.
- `plots/`: Output plots (PNG).
- `tests/`: Pytest unit tests.
- `report/`: The final written report, summaries, and presentation outline.

## Requirements
- Python 3.10+
- `pip install -r requirements.txt`

## Running the Project
To regenerate all data, plots, and run the tests, simply execute:
```bash
python run_all.py
```
*Note: The full suite may take a significant amount of time (over 10 minutes) because the timing side-channel attack (`exp3_timing.py`) performs 20 trials with up to 5000 samples per guess to build statistical confidence across microsecond delays.*

## Demo
For a live console demonstration of the attacks and mitigations, run:
```bash
python demo.py
```
