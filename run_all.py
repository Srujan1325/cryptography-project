import os
import subprocess
import sys

def run(cmd):
    print(f"\n--- Running: {cmd} ---")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(1)

def main():
    print("=======================================")
    print(" RUNNING ALL EXPERIMENTS AND TESTS ")
    print("=======================================")
    
    run("pytest tests/")
    run("python3 experiments/exp1_vigenere.py")
    run("python3 experiments/exp2_rsa.py")
    run("python3 experiments/exp3_timing.py")
    run("python3 experiments/exp4_mitigations.py")
    run("python3 plotting/make_plots.py")
    run("python3 demo.py")
    
    print("\n=======================================")
    print(" ALL DONE SUCCESSFULLY ")
    print("=======================================")

if __name__ == '__main__':
    main()
