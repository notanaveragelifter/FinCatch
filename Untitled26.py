#!/usr/bin/env python
# coding: utf-8

# In[25]:


#Q1 Extractor
#Implement a Extractor that processes URLs from a given CSV file and extracts relevant information
import pandas as pd


# In[26]:


# Function to extract URLs from the CSV file
def extract_urls(csv_file_path):
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)
    
    # Assuming the CSV file has a column 'URL' for the URLs
    urls = df['URL'].tolist()
    
    # Return the list of URLs
    return urls

# Main function to demonstrate URL extraction
def main():
    # Path to the CSV file containing URLs (update with your actual file path)
    csv_file_path = r"C:\Users\LENOVO\Downloads\FinCatch_Sources_Medium.csv"
    
    # Extract URLs from the CSV file
    urls = extract_urls(csv_file_path)

    # Print the extracted URLs
    print("Extracted URLs:")
    for url in urls:
        print(url)

# Execute the main function
if __name__ == "__main__":
    main()


# In[27]:


pip install networkx python-louvain matplotlib


# In[36]:


# Q2 Causal Relationship Visualizer
# Design a system to visualize the causal relationships between the financial knowledge using a graph database.
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests
from neo4j import GraphDatabase


# In[37]:


# Example data (stock prices and interest rates)
stock_prices = pd.Series([100, 102, 104, 103, 107], index=pd.date_range('2024-01-01', periods=5))
interest_rate = pd.Series([1.5, 1.6, 1.7, 1.8, 1.9], index=pd.date_range('2024-01-01', periods=5))

# Granger Causality Test
result = grangercausalitytests(pd.concat([stock_prices, interest_rate], axis=1), maxlag=1)

# Assuming result shows a causal relationship
if result[1][0]['ssr_chi2test'][1] < 0.05:
    print("Causal Relationship Detected: Stock Prices affect Interest Rate")

# Connect to Neo4j and create a relationship
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_causal_relationship(tx, source, target):
    query = (
        f"MATCH (s:{source}), (t:{target}) "
        "CREATE (s)-[:AFFECTS]->(t)"
    )
    tx.run(query)

with driver.session() as session:
    session.write_transaction(create_causal_relationship, "StockPrice", "EconomicIndicator")


# In[40]:


# Q3 Clustering Module
# Develop a module to cluster financial knowledge into reasonable classes based on their content and relationships.
import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt


# In[41]:


# Create a sample graph (replace with actual causal relationships)
G = nx.Graph()
G.add_edges_from([
    ('CompanyA', 'Sector1'),
    ('CompanyB', 'Sector1'),
    ('CompanyC', 'Sector2'),
    ('StockPrice1', 'InterestRate'),
    ('StockPrice2', 'InterestRate')
])

# Apply the Louvain method for community detection
partition = community_louvain.best_partition(G)

# Visualize the graph with community colors
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G)
cmap = plt.cm.get_cmap('Set3', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=300, cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=10)
plt.title("Causal Graph with Detected Communities")
plt.show()

# The `partition` dictionary shows the community for each node.





