import pickle
import glob
from numpy.core.fromnumeric import shape
from tqdm import tqdm
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib
import numpy
import time
import dgl
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch as th




def make_dataset(folder_name, label):
    folder_globs = glob.glob(folder_name+"/*.csv")

    graphs = []
    glabels = []

    node_idx = 0
    node_list = {}

    for f in tqdm(folder_globs, desc=folder_name):
        file_name = f.split("\\")[-1]
        if file_name == "0x0000000000000000000000000000000000000000.csv": continue
        data = pd.read_csv(f)

        NumTx = len(data)
        node_list = {file_name[:-4]: 0}
        node_idx = 1
        # if i == 100: break
        tx_index = -2
        with open(folder_name+"/"+file_name, "r") as ff:
            while True:
                tx_index += 1
                arg = ff.readline()
                if not arg: break
                if tx_index == -1: continue
                
                args = arg.split(",")
                args = args[1:]

                if args[0] == "TxHash": continue
                if not (args[3] in node_list.keys()):
                    node_list[args[3]] = node_idx
                    node_idx += 1
                if not (args[4] in node_list.keys()):
                    node_list[args[4]] = node_idx
                    node_idx += 1

        ToT = th.tensor([], dtype=torch.int32)
        FromT = th.tensor([], dtype=torch.int32)

        tx_index = -2
        with open(folder_name+"/"+file_name, "r") as ff:
            while True:
                tx_index += 1
                arg = ff.readline()
                if not arg: break
                if tx_index == -1: continue
                args = arg.split(",")
                args = args[1:]

                From = args[3]
                To = args[4]

                FromT = torch.cat((FromT, th.tensor([node_list[From], node_idx+tx_index])), 0)
                ToT = torch.cat((ToT, th.tensor([node_idx+tx_index, node_list[To]])), 0)

        graph = dgl.graph((FromT, ToT))

        graph.ndata['feature'] = th.zeros(node_idx + tx_index, 13+2)


        in_degree = th.zeros(node_idx, dtype=torch.float64)
        out_degree = th.zeros(node_idx, dtype=torch.float64)
        in_value = th.zeros(node_idx, dtype=torch.float64)
        out_value = th.zeros(node_idx, dtype=torch.float64)
        # avg_tx_gap = th.zeros(node_idx, dtype=torch.float64)
        # lifetime = th.zeros(node_idx, dtype=torch.float64)
        # balance = th.zeros(node_idx, dtype=torch.float64)
        # avg_in_value = th.zeros(node_idx, dtype=torch.float64)
        # avg_out_value = th.zeros(node_idx, dtype=torch.float64)
        # min_in_value = th.ones(node_idx, dtype=torch.float64) * 999999999
        # min_out_value = th.ones(node_idx, dtype=torch.float64) * 999999999
        # max_in_value = th.zeros(node_idx, dtype=torch.float64)
        # max_out_value = th.zeros(node_idx, dtype=torch.float64)

        Min_TS = th.ones(node_idx, dtype=torch.float64) * 999999999
        Max_TS = th.zeros(node_idx, dtype=torch.float64)
        Total_Tx = th.zeros(node_idx, dtype=torch.float64)

        tx_index = -2
        with open(folder_name+"/"+file_name, "r") as ff:

            while True:
                tx_index += 1
                arg = ff.readline()
                if not arg: 
                    break
                if tx_index == -1: continue
                args = arg.split(",")
                args = args[1:]

                From = args[3]
                To = args[4]
                TimeStamp = float(args[2]) - 1438920403
                Value = float(args[5])

                in_degree[node_list[To]] += 1 
                out_degree[node_list[From]] += 1 

                in_value[node_list[To]] += Value
                out_value[node_list[From]] += Value 

                Total_Tx[node_list[To]] += 1 
                Total_Tx[node_list[From]] += 1 

                Min_TS[node_list[To]] = min(Min_TS[node_list[To]], TimeStamp)
                Max_TS[node_list[From]] = max(Max_TS[node_list[From]], TimeStamp)

                graph.ndata['feature'][node_idx+tx_index] = th.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, TimeStamp, Value])
        
        for i in range(node_idx):
            avg_tx_gap = 0
            if Total_Tx[i]-1 != 0:
                avg_tx_gap = (Max_TS[i]-Min_TS[i])/(Total_Tx[i]-1)
            avg_in_value = 0
            if in_degree[i] != 0:
                avg_in_value = in_value[i]/in_degree[i]
            avg_out_value = 0
            if out_degree[i] != 0:
                avg_out_value = out_value[i]/out_degree[i]

            graph.ndata['feature'][i] = th.tensor([in_degree[i], out_degree[i], in_value[i], out_value[i], #in degree, out degree, in_value, out_value
                                                    avg_tx_gap, Max_TS[i]-Min_TS[i], #avg tx gap, lifetime
                                                    in_value[i]-out_value[i], avg_in_value, avg_out_value, #balance, avg in value, avg out value
                                                    min(in_value), max(in_value), min(out_value), max(out_value),  #min_in_value, max_in_value, min_out_value, max_out_value
                                                    0, 0]) # Tx features

        graph = dgl.add_self_loop(graph)
        glabel = torch.zeros(5, dtype=torch.long)
        glabel[label] = 1

        glabels.append(glabel)
        graphs.append(graph)

    return graphs, glabels

glabels=[]
graphs=[]

normal = make_dataset("Normal first-order nodes", 0)
graphs.extend(normal[0])
glabels.extend(normal[1])
print(len(normal[0]), len(graphs))
phishing = make_dataset("Phishing first-order nodes", 1)
graphs.extend(phishing[0])
glabels.extend(phishing[1])
print(len(phishing[0]), len(graphs))
ponzi = make_dataset("Ponzi first-order nodes", 2)
graphs.extend(ponzi[0])
glabels.extend(ponzi[1])
print(len(ponzi[0]), len(graphs))
scam = make_dataset("Scam first-order nodes", 3)
graphs.extend(scam[0])
glabels.extend(scam[1])
print(len(scam[0]), len(graphs))
hack = make_dataset("Hack first-order nodes", 4)
graphs.extend(hack[0])
glabels.extend(hack[1])
print(len(hack[0]), len(graphs))

print(glabels)

dgl.save_graphs('fraud_homographs.dgl', graphs, {"glabels": glabels})