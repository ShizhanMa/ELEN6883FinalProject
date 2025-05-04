import requests
import json
import argparse
import csv

# Use your Graph Studio subgraph endpoint
subgraph_url = "https://api.studio.thegraph.com/query/110553/blockchainfinal/version/latest"

# Updated query for your subgraph's schema
query = """
{
  orderFulfilleds(first: 1000) {
    id
    offerer
    recipient
    transactionHash
    blockNumber
  }
}
"""

def send_graphql_query_to_subgraph(query, variables=None):
    headers = {
        'Content-Type': 'application/json'
        # No API key needed for Studio endpoint
    }
    payload = {'query': query}
    if variables:
        payload['variables'] = variables

    response = requests.post(subgraph_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None

def export_to_csv(data):
    orders = data.get('data', {}).get('orderFulfilleds', [])
    if orders:
        with open('comboB_orders.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'offerer', 'recipient', 'transactionHash', 'blockNumber']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for o in orders:
                writer.writerow({
                    'id': o.get('id', ''),
                    'offerer': o.get('offerer', ''),
                    'recipient': o.get('recipient', ''),
                    'transactionHash': o.get('transactionHash', ''),
                    'blockNumber': o.get('blockNumber', '')
                })
        print("✅ ComboB data exported to comboB_orders.csv")
    else:
        print("⚠️ No 'orderFulfilleds' data found.")

def main():
    parser = argparse.ArgumentParser(description='GraphQL CLI')
    parser.add_argument('--query', default=query, help='GraphQL query to be executed')
    parser.add_argument('--variables', help='Variables JSON string')
    args = parser.parse_args()

    variables = None
    if args.variables:
        try:
            variables = json.loads(args.variables)
        except json.JSONDecodeError:
            print("Error: Invalid JSON for variables.")
            return

    result = send_graphql_query_to_subgraph(args.query, variables)
    if result:
        print(json.dumps(result, indent=2))
        export_to_csv(result)

if __name__ == "__main__":
    main()