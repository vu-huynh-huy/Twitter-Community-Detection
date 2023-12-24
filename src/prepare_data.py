import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from random import randint

tw = pd.read_csv(
    "data/twitter_combined.txt.gz",
    compression="gzip",
    sep=" ",
    names=["start_node", "end_node"],
)
tw = tw.head(10000)

map_node = {}
node_id = 0
for node in tw['start_node'].unique():
    map_node[node] = node_id
    node_id += 1
tw['start_node'] = tw['start_node'].map(map_node)
tw['end_node'] = tw['end_node'].map(map_node)
tw.dropna(inplace=True)
tw['end_node'] = tw['end_node'].astype(int)
tw.to_csv('data/twitter_10000.csv', index=False)