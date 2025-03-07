import pandas as pd

def reduce_dataset(input_file, output_file, sample_size=100000):
    # Load dataset
    df = pd.read_csv(input_file)
    
    # Ensure we don't sample more than available rows
    sample_size = min(sample_size, len(df))
    
    # Randomly sample the dataset
    df_sampled = df.sample(n=sample_size, random_state=42)
    
    # Save reduced dataset
    df_sampled.to_csv(output_file, index=False)
    print(f"Reduced dataset saved as '{output_file}' with {sample_size} rows.")

# Run function
reduce_dataset("final_dataset.csv", "reduced_dataset.csv")
