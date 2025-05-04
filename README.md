# ELEN6883 Final Project – Seaport Smart Contract Data Analysis
This is the final project for Columbia University's course **ELEN E6883: Blockchain**.

## 👥 Team Members

| Name         | UNI     |
|--------------|---------|
| Shizhan Ma   | sm5754  |
| Linlin Fang  | lf2838  |
| Donglin Li   | dl3745  |
| Yu Pan       | yp2742  |


## 🔍 Project Overview

This project focuses on extracting and analyzing on-chain transaction data from the [Seaport smart contract](https://etherscan.io/address/0x00000000006c3852cbEf3e08E8dF289169EdE581), which powers the OpenSea NFT marketplace. All datasets generated are derived directly from Seaport’s event logs.

We adopted **two different approaches** for querying and analyzing the data:
1. **Subgraph-based approach** – using custom subgraph structures deployed via The Graph
2. **GraphQL explorer + Python scripts** – using Python to directly query Graph-hosted subgraphs


## 📁 Repository Structure
All code and output files are organized as follows:

### 🔹 Python Scripts
| File | Description |
|------|-------------|
| `subgraphA.py` ~ `subgraphD.py` | Scripts for generating and configuring subgraphs |
| `graphExplorerA.py` ~ `graphExplorerD.py` | Python scripts for querying data via The Graph’s hosted API |

### 🔹 Output CSVs

| File | Description |
|------|-------------|
| `order_fulfillments_comboA.csv` | Detailed fulfillment-level order data |
| `comboB_orders.csv` | Simplified view of core order information |
| `collections_comboC.csv` | Aggregated statistics by NFT collection |
| `comboD_trades.csv` | Trade-level data including transaction hashes, buyer/seller info |
| `graphExplorerA.csv` ~ `graphExplorerD.csv` | There will be an overlap with the data of the file above |

