import os
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file in the skill directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')

BASE_URL = "https://api.cloudflare.com/client/v4"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

def get_security_insights():
    url = f"{BASE_URL}/accounts/{ACCOUNT_ID}/security-center/insights"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching security insights: {response.status_code} - {response.text}")
        return []
    data = response.json()
    # print(f"DEBUG: {data}") # Uncomment if needed
    return data.get('result', [])

def main():
    parser = argparse.ArgumentParser(description="Cloudflare Security Insights")
    parser.add_argument("--severity", help="Filter by severity (low, medium, high, critical)")
    args = parser.parse_args()

    print(f"\n--- Security Insights (Account: {ACCOUNT_ID}) ---")
    insights = get_security_insights()
    
    if not insights:
        print("No security insights found or API access limited.")
        return

    # Filter by severity if requested
    if args.severity:
        insights = [i for i in insights if i.get('severity', '').lower() == args.severity.lower()]

    if not insights:
        print(f"No insights found with severity '{args.severity}'.")
        return

    print(f"{'Severity':<10} {'Type':<20} {'Product':<15} {'Message'}")
    print("-" * 100)
    for insight in insights:
        if not isinstance(insight, dict):
            continue
        severity = insight.get('severity', 'N/A').upper()
        type_ = insight.get('issue_type', 'N/A')
        product = insight.get('product', 'N/A')
        message = insight.get('message', 'N/A')
        
        # Truncate message if too long for one line
        if len(message) > 50:
            message = message[:47] + "..."
            
        print(f"{severity:<10} {type_:<20} {product:<15} {message}")

if __name__ == "__main__":
    main()
