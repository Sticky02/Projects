import pandas as pd
import requests

def download_tranco_top_sites():
    url = "https://tranco-list.eu/top-1m.csv"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open("tranco_top_1m.csv", "wb") as file:
            file.write(response.content)
        print("Downloaded Tranco Top 1M dataset.")
    else:
        print("Failed to download dataset.")

def process_tranco_dataset():
    file_path = "tranco.csv"
    df = pd.read_csv(file_path, names=["rank", "domain"], header=None)
    df["url"] = "https://" + df["domain"]
    df_legit = df[["url"]]
    df_legit.to_csv("legitimate_urls.csv", index=False)
    print("Processed legitimate URLs and saved as 'legitimate_urls.csv'.")

# Run functions
#download_tranco_top_sites()
process_tranco_dataset()
