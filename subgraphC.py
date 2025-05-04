import requests
import json
import argparse
import csv

# ✅ Your Graph Studio subgraph endpoint
subgraph_url = "https://api.studio.thegraph.com/query/110553/blockchainfinal/version/latest"

# ✅ Updated GraphQL query to match your schema
query = """
{
  orderFulfilleds(first: 1000) {
    id
    orderHash
    offerer
    recipient
    blockNumber
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
        print("Error:", response.text)
        return None

# ✅ Export data to CSV for Combo C
def export_to_csv(data):
    records = data.get('data', {}).get('orderFulfilleds', [])
    if records:
        with open('collections_comboC.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'orderHash', 'offerer', 'recipient', 'blockNumber', 'blockTimestamp', 'transactionHash']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for rec in records:
                writer.writerow({
                    'id': rec.get('id', ''),
                    'orderHash': rec.get('orderHash', ''),
                    'offerer': rec.get('offerer', ''),
                    'recipient': rec.get('recipient', ''),
                    'blockNumber': rec.get('blockNumber', ''),
                    'blockTimestamp': rec.get('blockTimestamp', ''),
                    'transactionHash': rec.get('transactionHash', '')
                })
        print("✅ ComboC data exported to collections_comboC.csv")
    else:
        print("⚠️ No 'orderFulfilleds' data found.")

# ✅ Entry point
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
