import os
import time
import logging
from dotenv import load_dotenv
import shopify

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Shopify API credentials loaded from .env file
API_KEY = os.getenv('SHOPIFY_API_KEY')
PASSWORD = os.getenv('SHOPIFY_API_PASSWORD')
STORE_NAME = os.getenv('SHOPIFY_STORE_NAME')
API_VERSION = os.getenv('SHOPIFY_API_VERSION')

# Expected structure of the .env file:
# SHOPIFY_API_KEY=your_api_key
# SHOPIFY_API_PASSWORD=your_api_password
# SHOPIFY_STORE_NAME=your_store_name
# SHOPIFY_API_VERSION=your_api_version

def setup_shopify_session():
    """Set up the Shopify API session."""
    try:
        shop_url = f"https://{API_KEY}:{PASSWORD}@{STORE_NAME}.myshopify.com/admin/api/{API_VERSION}"
        shopify.ShopifyResource.set_site(shop_url)
        logging.info("Successfully connected to Shopify store.")
    except Exception as e:
        logging.error(f"Failed to connect to Shopify: {e}")
        raise

def get_all_variants():
    """Fetch all product variants from the Shopify store."""
    variants = []
    try:
        page = 1
        while True:
            products = shopify.Product.find(limit=250, page=page)
            if not products:
                break
            for product in products:
                variants.extend(product.variants)
            page += 1
            time.sleep(0.5)  # Respect API rate limits
        logging.info(f"Fetched {len(variants)} variants from the store.")
    except Exception as e:
        logging.error(f"Error fetching variants: {e}")
        raise
    return variants

def calculate_new_price(cost):
    """Calculate the new price based on the cost."""
    try:
        if cost is None or not isinstance(cost, (int, float)) or cost <= 0:
            return None
        # Placeholder for custom pricing logic
        new_price = cost * 2.0  # Example formula: double the cost
        return round(new_price, 2)
    except Exception as e:
        logging.error(f"Error calculating new price: {e}")
        return None

def process_and_update_variants(variants):
    """Process each variant and update its price if necessary."""
    for variant in variants:
        try:
            cost = getattr(variant, 'cost', None)
            if cost is None:
                logging.warning(f"Variant {variant.id} skipped: missing cost.")
                continue

            new_price = calculate_new_price(cost)
            if new_price is None:
                logging.warning(f"Variant {variant.id} skipped: invalid cost.")
                continue

            if float(variant.price) != new_price:
                variant.price = new_price
                variant.save()
                logging.info(f"Updated variant {variant.id}: new price set to {new_price}.")
                time.sleep(0.5)  # Respect API rate limits
            else:
                logging.info(f"Variant {variant.id}: price unchanged.")
        except Exception as e:
            logging.error(f"Error processing variant {variant.id}: {e}")

if __name__ == "__main__":
    logging.info("Script started.")
    try:
        setup_shopify_session()
        variants = get_all_variants()
        process_and_update_variants(variants)
    except Exception as e:
        logging.error(f"Script terminated with an error: {e}")
    logging.info("Script finished.")