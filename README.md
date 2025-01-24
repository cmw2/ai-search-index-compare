# Index Field Value Diff

This script compares the counts of unique values for a specific field between two Azure Search indexes.

## Prerequisites

- Python 3.x
- Azure Search service

## Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/cmw2/ai-search-index-compare.git
   cd ai-search-index-compare
   ```

   Adjust the URL if you have forked the repo.

1. **Create a Python virtual environment**

   ```sh
   python -m venv venv
   ```

1. **Activate the virtual environment**

   - On Windows:

     ```sh
     .\venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```sh
     source venv/bin/activate
     ```

1. **Install the required packages**

   ```sh
   pip install -r requirements.txt
   ```

1. **Copy and modify the `.env.sample` file**

   - On Windows (Command Prompt or PowerShell):

     ```sh
     copy .env.sample .env
     ```

   - On macOS/Linux:

     ```sh
     cp .env.sample .env
     ```

   Edit the `.env` file to include your Azure Search service endpoint and API key:

    ```env
    SEARCH_ENDPOINT=https://yoursearch.search.windows.net
    SEARCH_KEY=yourkey
    ```

## Running the Script

To run the script, use the following command:

```sh
python index_field_value_diff.py <index1_name> <index2_name> [--field <field_name>]
```

- `<index1_name>`: Name of the first index
- `<index2_name>`: Name of the second index
- `--field <field_name>`: (Optional) Field to compare (default: `url`)

### Example

```sh
python index_field_value_diff.py index1 index2 --field custom_field
```

This will compare the counts of unique values for the specified field between the two indexes.