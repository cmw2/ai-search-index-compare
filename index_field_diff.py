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
def get_data(service_endpoint, index_name, api_key, field):
    client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))
    values = []
    batch_size = 1000
    skip = 0

    while True:
        results = client.search(search_text="", select=field, top=batch_size, skip=skip)
        batch_values = [doc[field] for doc in results]
        if not batch_values:
            break
        values.extend(batch_values)
        skip += batch_size

    return values

# Get data from both indexes
values_index1 = get_data(service_endpoint, index1_name, api_key, field)
values_index2 = get_data(service_endpoint, index2_name, api_key, field)

# Count the occurrences of each URL
count_index1 = Counter(values_index1)
count_index2 = Counter(values_index2)

# Find URLs only in one index
only_in_index1 = set(count_index1) - set(count_index2)
only_in_index2 = set(count_index2) - set(count_index1)

# Find URLs with different numbers of rows
diff_counts = {value: (count_index1[value], count_index2[value]) for value in set(values_index1) & set(values_index2) if count_index1[value] != count_index2[value]}

# Print results
print(f"Values only in {index1_name}:")
for value in only_in_index1:
    print(value)

print(f"\nValues only in {index2_name}:")
for value in only_in_index2:
    print(value)

print("\nValues with different numbers of rows:")
for value, counts in diff_counts.items():
    print(f"{value}: {index1_name}={counts[0]}, {index2_name}={counts[1]}")
