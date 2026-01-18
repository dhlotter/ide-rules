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

def get_zone_id(domain):
    url = f"{BASE_URL}/zones?name={domain}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json().get('result', [])
        if result:
            return result[0]['id']
    return None

def get_speed_summary(zone_id):
    # This endpoint provides the Synthetic Monitoring data (Observatory)
    url = f"{BASE_URL}/zones/{zone_id}/speed_api/pages"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, response.status_code, response.text
    return response.json().get('result', []), 200, None

def get_rum_metrics(zone_id):
    query = """
    query {
      viewer {
        zones(filter: { zoneTag: "%s" }) {
          rumAnalyticsAdaptiveGroups(limit: 10, filter: { datetime_gt: "%s" }) {
            avg {
              sampleInterval
            }
            sum {
              visits
            }
          }
        }
      }
    }
    """
    from datetime import datetime, timedelta
    yesterday_iso = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    formatted_query = query % (zone_id, yesterday_iso)
    
    url = f"{BASE_URL}/graphql"
    response = requests.post(url, headers=headers, json={"query": formatted_query})
    
    if response.status_code != 200:
        return None
    data = response.json().get('data', {})
    if not data or not data.get('viewer'):
        return None
    return data.get('viewer', {}).get('zones', [{}])[0].get('rumAnalyticsAdaptiveGroups', [])

def main():
    parser = argparse.ArgumentParser(description="Cloudflare Speed Observatory")
    parser.add_argument("--domain", required=True, help="The domain to check (e.g. easyentropy.com)")
    args = parser.parse_args()

    zone_id = get_zone_id(args.domain)
    if not zone_id:
        print(f"Error: Could not find zone ID for domain {args.domain}")
        return

    print(f"\n--- Speed Observatory for {args.domain} ---")
    
    # 1. Synthetic Monitoring (Observatory)
    pages, status, error = get_speed_summary(zone_id)
    
    if status == 200 and pages:
        print("\n[Synthetic Monitoring]")
        print(f"{'URL':<40} {'LCP (s)':<10} {'FID (ms)':<10} {'CLS':<10} {'Perf Score'}")
        print("-" * 90)
        for page in pages:
            url = page.get('url', 'N/A')
            metrics = page.get('latest', {}).get('lighthouse', {})
            lcp = metrics.get('largest_contentful_paint', 'N/A')
            fid = metrics.get('first_input_delay', 'N/A')
            cls = metrics.get('cumulative_layout_shift', 'N/A')
            score = page.get('latest', {}).get('performance_score', 'N/A')
            print(f"{url:<40} {str(lcp):<10} {str(fid):<10} {str(cls):<10} {str(score)}")
    elif status == 403:
        print("⚠️  Synthetic Data: Access Denied (Missing 'Zone | Speed | Read')")
    
    # 2. Real User Monitoring (RUM)
    rum_data = get_rum_metrics(zone_id)
    if rum_data:
        print("\n[Real User Monitoring (Last 24h)]")
        # Extract basic visit count for now as a proof of concept
        total_visits = sum(group.get('sum', {}).get('visits', 0) for group in rum_data)
        print(f"Total Visits: {total_visits}")
    else:
        print("\n⚠️  RUM Data: No data found or missing 'Zone | Analytics | Read'")

if __name__ == "__main__":
    main()
