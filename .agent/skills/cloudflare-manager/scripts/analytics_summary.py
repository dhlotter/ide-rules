import os
import requests
import argparse
from datetime import datetime, timedelta
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

def get_zone_id(domain):
    url = f"{BASE_URL}/zones?name={domain}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json().get('result', [])
        if result:
            return result[0]['id']
    return None

def get_analytics(zone_id):
    # GraphQL query for last 24 hours of data
    query = """
    query {
      viewer {
        zones(filter: { zoneTag: "%s" }) {
          httpRequests1dGroups(limit: 1, filter: { date: "%s" }) {
            sum {
              requests
              bytes
              cachedRequests
              cachedBytes
            }
          }
        }
      }
    }
    """
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    formatted_query = query % (zone_id, yesterday)
    
    url = f"{BASE_URL}/graphql"
    response = requests.post(url, headers=headers, json={"query": formatted_query})
    
    if response.status_code != 200:
        print(f"GraphQL Error Output: {response.text}")
        return None
    
    result = response.json()
    if 'errors' in result and result['errors']:
        print(f"GraphQL Errors: {result['errors']}")
        return None
        
    data = result.get('data', {}).get('viewer', {}).get('zones', [])
    if not data:
        return None
        
    return data[0]

def main():
    parser = argparse.ArgumentParser(description="Cloudflare 24h Pulse")
    parser.add_argument("--domain", required=True, help="The domain to check (e.g. easyentropy.io)")
    args = parser.parse_args()

    zone_id = get_zone_id(args.domain)
    if not zone_id:
        print(f"Error: Could not find zone ID for domain {args.domain}")
        return

    data = get_analytics(zone_id)
    if not data:
        print("Error: Could not fetch analytics data.")
        return

    stats = data.get('httpRequests1dGroups', [{}])[0].get('sum', {})

    print(f"\n--- 24h Pulse for {args.domain} ---")
    print(f"Total Requests:   {stats.get('requests', 0):,}")
    print(f"Bandwidth:        {stats.get('bytes', 0) / (1024*1024):.2f} MB")
    print(f"Cache Ratio:      {(stats.get('cachedRequests', 0) / max(stats.get('requests', 1), 1)) * 100:.1f}%")

if __name__ == "__main__":
    main()
