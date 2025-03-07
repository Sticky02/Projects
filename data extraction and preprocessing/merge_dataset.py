import pandas as pd
from sklearn.utils import resample

def merge_datasets(phishing_file, legit_file, output_file):
    # Load datasets
    df_phishing = pd.read_csv(phishing_file)
    df_legit = pd.read_csv(legit_file)
    
    # Ensure both datasets have only the 'url' column
    df_phishing = df_phishing[['url']]
    df_legit = df_legit[['url']]
    
    # Assign labels
    df_phishing['label'] = 1
    df_legit['label'] = 0
    
    # Determine the minority class size
    min_size = min(len(df_phishing), len(df_legit))
    
    # Downsample both classes to the same size
    df_phishing_balanced = resample(df_phishing, replace=False, n_samples=min_size, random_state=42)
    df_legit_balanced = resample(df_legit, replace=False, n_samples=min_size, random_state=42)
    
    # Merge balanced datasets
    df_combined = pd.concat([df_phishing_balanced, df_legit_balanced], ignore_index=True)
    
    # Shuffle dataset
    df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save merged dataset
    df_combined.to_csv(output_file, index=False)
    print(f"Merged dataset saved as '{output_file}' with {len(df_combined)} rows.")

# Run the merge function
merge_datasets("verified_online.csv", "legitimate_urls.csv", "final_dataset.csv")
