import os
import requests
import argparse
from datetime import datetime
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

def get_registrar_domains():
    # Registrar domains are often listed under the account
    url = f"{BASE_URL}/accounts/{ACCOUNT_ID}/registrar/domains"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching registrar domains: {response.status_code} - {response.text}")
        return []
    return response.json().get('result', [])

def main():
    print(f"\n--- Registrar Status (Account: {ACCOUNT_ID}) ---")
    domains = get_registrar_domains()
    
    if not domains:
        print("No registrar domains found or API access limited.")
        return

    print(f"{'Domain':<30} {'Status':<15} {'Expires':<15} {'Auto-Renew':<10}")
    print("-" * 75)
    for d in domains:
        expires = d.get('expires_at', 'N/A')
        if expires != 'N/A':
            expires = expires.split('T')[0]
        
        print(f"{d['name']:<30} {d['status']:<15} {expires:<15} {str(d.get('auto_renew', False)):<10}")

if __name__ == "__main__":
    main()
