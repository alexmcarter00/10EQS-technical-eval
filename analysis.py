import csv
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# load data from CSV
def load_data(csv_path):
    products = []
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row)
    return products

# fetch market price from an external API
def fetch_market_price(product_name):
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API Key is missing. Please add it to your .env file.")

    # Replace with your actual API endpoint for fetching market prices
    url = f"https://api.example.com/get-price?product={product_name}"
    
    # Make the API request
    try:
        response = requests.get(url, headers={"API-Key": api_key})
        response.raise_for_status()
        data = response.json()
        
        # Assuming the response contains the market price
        return data.get("market_price")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {product_name}: {e}")
        return None

# compare business price with market price and generate insights
def compare_prices(products):
    insights = []
    for product in products:
        # Get the market price for the product
        market_price = fetch_market_price(product["product_name"])
        
        if market_price:
            # Compare prices (convert to float for comparison)
            our_price = float(product["our_price"].replace('$', '').replace(',', ''))
            market_price = float(market_price.replace('$', '').replace(',', ''))

            price_diff = our_price - market_price
            
            if price_diff > 2:
                insights.append(f"{product['product_name']} is overpriced by ${price_diff:.2f}")
            elif price_diff < -2:
                insights.append(f"{product['product_name']} is underpriced by ${-price_diff:.2f}")
            else:
                insights.append(f"{product['product_name']} is priced competitively.")
        else:
            insights.append(f"Market price for {product['product_name']} could not be fetched.")

    return insights

# generate the analysis report
def generate_report(insights):
    with open("report.md", mode='w') as report_file:
        report_file.write("# Product Pricing Report\n\n")
        
        if insights:
            report_file.write("## Key Insights\n")
            for insight in insights:
                report_file.write(f"- {insight}\n")
        else:
            report_file.write("No pricing insights available.\n")

# Main function to orchestrate the analysis
def main(csv_path):
    # Load product data from CSV
    products = load_data(csv_path)
    
    # Compare prices and generate insights
    insights = compare_prices(products)
    
    # Generate the report
    generate_report(insights)
    print("Analysis complete. Report generated as 'report.md'.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python src/analysis.py <path_to_products_csv>")
    else:
        main(sys.argv[1])
