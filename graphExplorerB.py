import requests  # 发送 HTTP 请求的库
import json      # 处理 JSON 数据
import argparse  # 解析命令行参数
import csv       # 用于导出 CSV 文件

# Subgraph 入口 URL（带 ID）
subgraph_url = "https://gateway.thegraph.com/api/subgraphs/id/2GmLsgYGWoFoouZzKjp8biYDkfmeLTkEY3VDQyZqSJHA"

# 个人 API Key
api_key = 'a18cc39bf1668aadbeb73eb0a61496c2'

# GraphQL 查询语句（组合 B：获取 marketplace 基本信息）
query = """
{
  marketplaces(first: 1000) {
    id
    name
    network
    slug
    totalRevenueETH
    tradeCount
  }
}
"""

# 向 subgraph 发送 GraphQL 请求
def send_graphql_query_to_subgraph(api_key, query, variables=None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'  # 添加认证头
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

# 将 marketplace 数据导出为 CSV 文件
def export_to_csv(data):
    marketplaces = data.get('data', {}).get('marketplaces', [])
    if marketplaces:
        with open('graphExplorerB.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'network', 'slug', 'totalRevenueETH', 'tradeCount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for mp in marketplaces:
                writer.writerow({
                    'id': mp.get('id', ''),
                    'name': mp.get('name', ''),
                    'network': mp.get('network', ''),
                    'slug': mp.get('slug', ''),
                    'totalRevenueETH': mp.get('totalRevenueETH', ''),
                    'tradeCount': mp.get('tradeCount', '')
                })
        print("✅ 组合B数据已导出到 graphExplorerB.csv")
    else:
        print("⚠️ 响应中未包含 marketplaces 字段")


# 主程序入口
def main():
    parser = argparse.ArgumentParser(description='GraphQL CLI')
    parser.add_argument('--api_key', default=api_key,
                        help='API Key obtained in Subgraph Studio for querying a Subgraph')
    parser.add_argument('--query', default=query, help='GraphQL query to be executed')
    parser.add_argument('--variables', help='Variables JSON string')
    args = parser.parse_args()

    # 尝试解析变量参数
    variables = None
    if args.variables:
        try:
            variables = json.loads(args.variables)
        except json.JSONDecodeError:
            print("Error: Invalid JSON for variables.")
            return

    # 发送请求并导出数据
    result = send_graphql_query_to_subgraph(args.api_key, args.query, variables)
    if result:
        print(json.dumps(result, indent=100))
        export_to_csv(result)

if __name__ == "__main__":
    main()
