# Shopify Price Update Script

This Python script automates the process of updating product prices on a Shopify store based on their 'cost per item'.

## Features
- Securely connects to a Shopify store using the Admin API.
- Fetches all product variants, handling pagination and respecting API rate limits.
- Reads the 'cost per item' for each variant and calculates a new price using a customizable formula.
- Updates the price in Shopify if the calculated price differs from the current price.
- Includes robust error handling and informative logging.

## Requirements
- Python 3.x
- Libraries: `shopify_python_api`, `python-dotenv`

## Setup

1. **Install Dependencies**:
   ```bash
   pip install shopify python-dotenv
   ```

2. **Create a `.env` File**:
   Place a `.env` file in the same directory as the script with the following structure:
   ```env
   SHOPIFY_API_KEY=your_api_key
   SHOPIFY_API_PASSWORD=your_api_password
   SHOPIFY_STORE_NAME=your_store_name
   SHOPIFY_API_VERSION=your_api_version
   ```

3. **Customize Pricing Logic**:
   Open the script and modify the `calculate_new_price` function to implement your specific pricing formula. The default formula doubles the cost:
   ```python
   new_price = cost * 2.0
   ```

## Usage

1. Run the script:
   ```bash
   python update_prices.py
   ```

2. The script will:
   - Connect to your Shopify store.
   - Fetch all product variants.
   - Calculate new prices based on the cost.
   - Update prices in Shopify if necessary.

## Logging
The script logs its progress and any errors encountered. Logs include:
- Script start and end.
- Connection success or failure.
- Number of variants fetched.
- Details of each variant processed (e.g., ID, calculated price, update status).
- Warnings for skipped variants (e.g., missing cost).

## Notes
- Ensure your Shopify Private App has the necessary permissions to read and write product data.
- Respect Shopify API rate limits by keeping the `time.sleep` calls in the script.

## License
This script is provided "as is" without warranty of any kind. Use at your own risk.