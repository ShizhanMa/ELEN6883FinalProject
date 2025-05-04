import requests  # 发送 HTTP 请求的库
import json       # 处理 JSON 数据
import argparse   # 命令行参数解析
import csv        # 用于导出 CSV 文件

# GraphQL 查询地址（包含 Subgraph ID）
subgraph_url = "https://gateway.thegraph.com/api/subgraphs/id/2GmLsgYGWoFoouZzKjp8biYDkfmeLTkEY3VDQyZqSJHA"

# 个人 API Key
api_key = 'a18cc39bf1668aadbeb73eb0a61496c2'

# GraphQL 查询语句：获取 orderFulfillments 中包含的交易数据
query = """
{
  orderFulfillments(first: 1000) {
    id
    trade {
      priceETH
      timestamp
      buyer
      seller
      tokenId
      transactionHash
      collection {
        id
        name
      }
    }
  }
}
"""

# 发送 GraphQL 查询请求函数
def send_graphql_query_to_subgraph(api_key, query, variables=None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'  # 授权头
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

# 导出组合A结果为 CSV 文件
def export_to_csv(data):
    fulfillments = data.get('data', {}).get('orderFulfillments', [])
    if fulfillments:
        with open('graphExplorerA.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'fulfillment_id', 'priceETH', 'timestamp',
                'buyer', 'seller', 'tokenId', 'transactionHash',
                'collection_id', 'collection_name'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for f in fulfillments:
                trade = f.get('trade', {})
                collection = trade.get('collection', {})
                writer.writerow({
                    'fulfillment_id': f.get('id', ''),
                    'priceETH': trade.get('priceETH', ''),
                    'timestamp': trade.get('timestamp', ''),
                    'buyer': trade.get('buyer', ''),
                    'seller': trade.get('seller', ''),
                    'tokenId': trade.get('tokenId', ''),
                    'transactionHash': trade.get('transactionHash', ''),
                    'collection_id': collection.get('id', ''),
                    'collection_name': collection.get('name', '')
                })
        print("✅ 数据已导出到 graphExplorerA.csv")
    else:
        print("⚠️ 响应中未包含 orderFulfillments 字段")

# 程序主入口
def main():
    parser = argparse.ArgumentParser(description='GraphQL CLI')
    parser.add_argument('--api_key', default=api_key,
                        help='API Key obtained in Subgraph Studio for querying a Subgraph')
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

    result = send_graphql_query_to_subgraph(args.api_key, args.query, variables)
    if result:
        print(json.dumps(result, indent=100))  # 打印 JSON 数据（可选）
        export_to_csv(result)  # 导出 CSV

if __name__ == "__main__":
    main()
