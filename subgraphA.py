import requests
import json
import argparse
import csv

# Use your own subgraph Studio endpoint
subgraph_url = "https://api.studio.thegraph.com/query/110553/blockchainfinal/version/latest"

query = """
{
  orderFulfilleds(first: 1000) {
    id
    orderHash
    offerer
    zone
    recipient
    blockNumber
    blockTimestamp
    transactionHash
  }
}
"""

def send_graphql_query_to_subgraph(query, variables=None):
    headers = {
        'Content-Type': 'application/json'
        # No Authorization needed for Studio endpoint
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
    fulfillments = data.get('data', {}).get('orderFulfilleds', [])
    if fulfillments:
        with open('order_fulfillments_comboA.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'orderHash', 'offerer', 'zone', 'recipient',
                'blockNumber', 'blockTimestamp', 'transactionHash'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for f in fulfillments:
                writer.writerow({
                    'id': f.get('id', ''),
                    'orderHash': f.get('orderHash', ''),
                    'offerer': f.get('offerer', ''),
                    'zone': f.get('zone', ''),
                    'recipient': f.get('recipient', ''),
                    'blockNumber': f.get('blockNumber', ''),
                    'blockTimestamp': f.get('blockTimestamp', ''),
                    'transactionHash': f.get('transactionHash', '')
                })
        print("✅ Data exported to order_fulfillments_comboA.csv")
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