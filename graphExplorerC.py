import requests  # 用于发送 HTTP 请求
import json      # 用于处理 JSON 数据
import argparse  # 用于解析命令行参数
import csv       # 用于导出 CSV 文件

# The Graph 子图 API 入口（使用子图 ID 构造）
subgraph_url = "https://gateway.thegraph.com/api/subgraphs/id/2GmLsgYGWoFoouZzKjp8biYDkfmeLTkEY3VDQyZqSJHA"

# 你的 Graph Studio API Key
api_key = 'a18cc39bf1668aadbeb73eb0a61496c2'

# GraphQL 查询语句 - 组合 C：查询 NFT collections 的收益视角数据
query = """
{
  collections(first: 1000) {
    id
    name
    symbol
    totalSupply
    tradeCount
    creatorRevenueETH
    totalRevenueETH
  }
}
"""

# 发送 GraphQL 请求并返回 JSON 结果
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

# 将 collections 数据导出为 CSV（组合 C 专用）
def export_to_csv(data):
    collections = data.get('data', {}).get('collections', [])
    if collections:
        with open('graphExplorerC.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'symbol', 'totalSupply', 'tradeCount', 'creatorRevenueETH', 'totalRevenueETH']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for col in collections:
                writer.writerow({
                    'id': col.get('id', ''),
                    'name': col.get('name', ''),
                    'symbol': col.get('symbol', ''),
                    'totalSupply': col.get('totalSupply', ''),
                    'tradeCount': col.get('tradeCount', ''),
                    'creatorRevenueETH': col.get('creatorRevenueETH', ''),
                    'totalRevenueETH': col.get('totalRevenueETH', '')
                })
        print("✅ 组合C数据已导出到 graphExplorerC.csv")
    else:
        print("⚠️ 响应中未包含 collections 字段")


# 主函数入口
def main():
    parser = argparse.ArgumentParser(description='GraphQL CLI')
    parser.add_argument('--api_key', default=api_key,
                        help='API Key obtained in Subgraph Studio for querying a Subgraph')
    parser.add_argument('--query', default=query, help='GraphQL query to be executed')
    parser.add_argument('--variables', help='Variables JSON string')
    args = parser.parse_args()

    # 解析可选变量
    variables = None
    if args.variables:
        try:
            variables = json.loads(args.variables)
        except json.JSONDecodeError:
            print("Error: Invalid JSON for variables.")
            return

    # 执行查询并导出 CSV
    result = send_graphql_query_to_subgraph(args.api_key, args.query, variables)
    if result:
        print(json.dumps(result, indent=100))
        export_to_csv(result)

# 程序运行入口
if __name__ == "__main__":
    main()
