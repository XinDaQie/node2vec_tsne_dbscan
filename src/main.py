import networkx as nx
import argparse
import pandas as pd
import json
from tqdm import tqdm
from node2vec import node2vec


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', type=float, default=1, help='return parameter')
    parser.add_argument('--q', type=float, default=0.5, help='in-out parameter')
    parser.add_argument('--d', type=int, default=64, help='dimension')  # 64维
    parser.add_argument('--r', type=int, default=10, help='walks per node')
    parser.add_argument('--l', type=int, default=80, help='walk length')
    parser.add_argument('--k', type=float, default=10, help='window size')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = args_parser()
    data = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2017.json')
    G = nx.DiGraph()
    G.add_nodes_from([i for i in data.index])

    for i in tqdm(range(data.shape[0])):
        for j in range(data.shape[1]):
            G.add_edges_from([(data.index[i], data.columns[j], {'weight': data.iloc[i, j]})])

    vec = node2vec(args, G)
    embeddings = vec.learning_features()
    embeddings = {k: v.tolist() for k, v in embeddings.items()}

    with open('./data/embeddings_2017_64v.json', 'w') as json_file:
        json.dump(embeddings, json_file)

    # print(embeddings)
