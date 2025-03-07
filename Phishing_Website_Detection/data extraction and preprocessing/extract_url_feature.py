import pandas as pd
import re
from urllib.parse import urlparse

def extract_features(df):
    # List of suspicious TLDs
    suspicious_tlds = {".tk", ".xyz", ".top", ".info", ".cf", ".ga", ".ml"}
    
    # List of suspicious words
    suspicious_words = {"login", "secure", "banking", "verify", "update", "account", "password"}
    
    # Extract URL features
    df['url_length'] = df['url'].apply(len)
    df['num_dots'] = df['url'].apply(lambda x: x.count('.'))
    df['num_hyphens'] = df['url'].apply(lambda x: x.count('-'))
    df['num_slashes'] = df['url'].apply(lambda x: x.count('/'))
    df['num_digits'] = df['url'].apply(lambda x: sum(c.isdigit() for c in x))
    df['num_subdomains'] = df['url'].apply(lambda x: urlparse(x).netloc.count('.'))
    df['has_https'] = df['url'].apply(lambda x: 1 if x.startswith('https') else 0)
    df['has_ip'] = df['url'].apply(lambda x: 1 if re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', x) else 0)
    
    # Extract domain and check TLD
    df['domain'] = df['url'].apply(lambda x: urlparse(x).netloc)
    df['tld'] = df['domain'].apply(lambda x: '.' + x.split('.')[-1] if '.' in x else '')
    df['suspicious_tld'] = df['tld'].apply(lambda x: 1 if x in suspicious_tlds else 0)
    
    # Check for suspicious words in URL
    df['suspicious_words'] = df['url'].apply(lambda x: 1 if any(word in x.lower() for word in suspicious_words) else 0)
    
    # Drop original URL and domain columns
    df = df.drop(columns=['url', 'domain', 'tld'])
    
    return df

def process_dataset(input_file, output_file):
    # Load dataset
    df = pd.read_csv(input_file)
    
    # Extract features
    df_processed = extract_features(df)
    
    # Save processed dataset
    df_processed.to_csv(output_file, index=False)
    print(f"Feature extracted dataset saved as '{output_file}'")

# Run function
process_dataset("final_dataset.csv", "feature_dataset.csv")
