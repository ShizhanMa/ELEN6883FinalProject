import requests
import json
import argparse
import csv

# 子图访问地址（你的子图 ID）
subgraph_url = "https://gateway.thegraph.com/api/subgraphs/id/2GmLsgYGWoFoouZzKjp8biYDkfmeLTkEY3VDQyZqSJHA"
api_key = 'a18cc39bf1668aadbeb73eb0a61496c2'

# GraphQL 查询语句（组合 D：交易数据视角）
query = """
{
  trades(first: 1000) {
    id
    priceETH
    timestamp
    transactionHash
    collection {
      id
      name
    }
  }
}
"""

# 发送 GraphQL 请求
def send_graphql_query_to_subgraph(api_key, query, variables=None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    response = requests.post(subgraph_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ 请求失败:", response.text)
        return None

# 导出交易数据到 CSV 文件（组合 D）
def export_to_csv(data):
    trades = data.get('data', {}).get('trades', [])
    if trades:
        with open('graphExplorerD.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'priceETH', 'timestamp', 'transactionHash', 'collection_id', 'collection_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for t in trades:
                collection = t.get('collection', {})
                writer.writerow({
                    'id': t.get('id', ''),
                    'priceETH': t.get('priceETH', ''),
                    'timestamp': t.get('timestamp', ''),
                    'transactionHash': t.get('transactionHash', ''),
                    'collection_id': collection.get('id', ''),
                    'collection_name': collection.get('name', '')
                })
        print("✅ graphExplorerD.csv 已成功导出")
    else:
        print("⚠️ 没有获取到 trades 数据")


# 主程序入口
def main():
    parser = argparse.ArgumentParser(description='Combo D - NFT Trade Info')
    parser.add_argument('--api_key', default=api_key, help='Your Graph API Key')
    parser.add_argument('--query', default=query, help='GraphQL query string')
    parser.add_argument('--variables', help='Optional variables in JSON format')
    args = parser.parse_args()

    variables = None
    if args.variables:
        try:
            variables = json.loads(args.variables)
        except json.JSONDecodeError:
            print("❌ 无效的变量 JSON 格式")
            return

    result = send_graphql_query_to_subgraph(args.api_key, args.query, variables)
    if result:
        export_to_csv(result)

if __name__ == "__main__":
    main()
