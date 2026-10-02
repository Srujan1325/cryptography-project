import urllib.request
import string
import os

URLS = [
    "https://www.gutenberg.org/cache/epub/1342/pg1342.txt", # Pride and Prejudice
    "https://www.gutenberg.org/cache/epub/84/pg84.txt",    # Frankenstein
    "https://www.gutenberg.org/cache/epub/11/pg11.txt"     # Alice in Wonderland
]

def download_and_clean():
    all_text = ""
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for url in URLS:
        print(f"Downloading {url}...")
        try:
            response = urllib.request.urlopen(url, context=ctx)
            text = response.read().decode('utf-8', errors='ignore')
            # Very rough header/footer strip
            start_idx = text.find("*** START OF THE PROJECT GUTENBERG")
            end_idx = text.find("*** END OF THE PROJECT GUTENBERG")
            if start_idx != -1 and end_idx != -1:
                text = text[start_idx:end_idx]
            all_text += text
        except Exception as e:
            print(f"Failed to download {url}: {e}")
    
    print("Cleaning text...")
    cleaned = ''.join(c for c in all_text.upper() if c in string.ascii_uppercase)
    
    os.makedirs('/Users/sunkavallisrujan/.gemini/antigravity/scratch/crypto-analysis/data/corpus', exist_ok=True)
    
    with open('/Users/sunkavallisrujan/.gemini/antigravity/scratch/crypto-analysis/data/corpus/cleaned_english.txt', 'w') as f:
        f.write(cleaned)
    
    # Save samples
    sizes = [100, 300, 500, 1000, 3000]
    for size in sizes:
        with open(f'/Users/sunkavallisrujan/.gemini/antigravity/scratch/crypto-analysis/data/corpus/sample_{size}.txt', 'w') as f:
            f.write(cleaned[:size])
    
    print("Done. Cleaned length:", len(cleaned))

if __name__ == '__main__':
    download_and_clean()
