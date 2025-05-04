import requests
import json
import argparse
import csv

# ✅ Your deployed subgraph URL (Studio endpoint, no API key needed)
subgraph_url = "https://api.studio.thegraph.com/query/110553/blockchainfinal/version/latest"

# ✅ GraphQL query (adapted from your OrderFulfilled structure)
query = """
{
  orderFulfilleds(first: 1000) {
    id
    orderHash
    offerer
    recipient
    blockTimestamp
    transactionHash
  }
}
"""

# ✅ No API key needed
def send_graphql_query_to_subgraph(query, variables=None):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    response = requests.post(subgraph_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Request failed:", response.text)
        return None

# ✅ Export OrderFulfilled as trade-like rows
def export_to_csv(data):
    orders = data.get('data', {}).get('orderFulfilleds', [])
    if orders:
        with open('comboD_trades.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'orderHash', 'offerer', 'recipient', 'blockTimestamp', 'transactionHash']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for o in orders:
                writer.writerow({
                    'id': o.get('id', ''),
                    'orderHash': o.get('orderHash', ''),
                    'offerer': o.get('offerer', ''),
                    'recipient': o.get('recipient', ''),
                    'blockTimestamp': o.get('blockTimestamp', ''),
                    'transactionHash': o.get('transactionHash', '')
                })
        print("✅ comboD_trades.csv exported successfully")
    else:
        print("⚠️ No 'orderFulfilleds' data found")

# ✅ CLI Entry
def main():
    parser = argparse.ArgumentParser(description='Combo D - Seaport Trade Info')
    parser.add_argument('--query', default=query, help='GraphQL query string')
    parser.add_argument('--variables', help='Optional variables in JSON format')
    args = parser.parse_args()

    variables = None
    if args.variables:
        try:
            variables = json.loads(args.variables)
        except json.JSONDecodeError:
            print("❌ Invalid JSON format for variables.")
            return

    result = send_graphql_query_to_subgraph(args.query, variables)
    if result:
        export_to_csv(result)

if __name__ == "__main__":
    main()
