import os
import argparse
from azure.search.documents import SearchClient
from collections import Counter
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the environment variables or provide them here directly
service_endpoint = os.getenv("SEARCH_ENDPOINT")
api_key = os.getenv("SEARCH_KEY")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Compare two Azure Search indexes.')
parser.add_argument('index1_name', type=str, help='Name of the first index')
parser.add_argument('index2_name', type=str, help='Name of the second index')
parser.add_argument('--field', type=str, default='url', help='Field to compare (default: url)')
args = parser.parse_args()

index1_name = args.index1_name
index2_name = args.index2_name
field = args.field

# Function to get URL data from an index
def get_url_data(service_endpoint, index_name, api_key, field):
    client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))
    urls = []
    batch_size = 1000
    skip = 0

    while True:
        results = client.search(search_text="", select=field, top=batch_size, skip=skip)
        batch_urls = [doc[field] for doc in results]
        if not batch_urls:
            break
        urls.extend(batch_urls)
        skip += batch_size

    return urls

# Get data from both indexes
urls_index1 = get_url_data(service_endpoint, index1_name, api_key, field)
urls_index2 = get_url_data(service_endpoint, index2_name, api_key, field)

# Count the occurrences of each URL
count_index1 = Counter(urls_index1)
count_index2 = Counter(urls_index2)

# Find URLs only in one index
only_in_index1 = set(count_index1) - set(count_index2)
only_in_index2 = set(count_index2) - set(count_index1)

# Find URLs with different numbers of rows
diff_counts = {url: (count_index1[url], count_index2[url]) for url in set(urls_index1) & set(urls_index2) if count_index1[url] != count_index2[url]}

# Print results
print(f"URLs only in {index1_name}:")
for url in only_in_index1:
    print(url)

print(f"\nURLs only in {index2_name}:")
for url in only_in_index2:
    print(url)

print("\nURLs with different numbers of rows:")
for url, counts in diff_counts.items():
    print(f"{url}: {index1_name}={counts[0]}, {index2_name}={counts[1]}")
