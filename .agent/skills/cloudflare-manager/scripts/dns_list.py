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

def list_zones():
    url = f"{BASE_URL}/zones"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching zones: {response.status_code} - {response.text}")
        return []
    return response.json().get('result', [])

def list_dns_records(zone_id):
    url = f"{BASE_URL}/zones/{zone_id}/dns_records"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching DNS records: {response.status_code} - {response.text}")
        return []
    return response.json().get('result', [])

def main():
    parser = argparse.ArgumentParser(description="Cloudflare DNS Record List")
    parser.add_argument("--zone-name", help="Filter by zone name (e.g., example.com)")
    args = parser.parse_args()

    zones = list_zones()
    
    if not zones:
        print("No zones found or authentication failed.")
        return

    for zone in zones:
        if args.zone_name and args.zone_name not in zone['name']:
            continue
            
        print(f"\n--- Zone: {zone['name']} (ID: {zone['id']}) ---")
        records = list_dns_records(zone['id'])
        
        if not records:
            print("  No DNS records found.")
            continue

        print(f"{'Type':<10} {'Name':<30} {'Content':<40} {'Proxied':<10}")
        print("-" * 90)
        for r in records:
            content = r['content']
            if len(content) > 37:
                content = content[:37] + "..."
            print(f"{r['type']:<10} {r['name']:<30} {content:<40} {str(r['proxied']):<10}")

if __name__ == "__main__":
    main()
