# FDGNN: Fraud Address Detection using Graph Neural Network on Ethereum

### Abstract

Recently, cybercrimes that exploit the anonymity of blockchain are increasing. They steal blockchain users' assets, threaten the network's reliability, and destabilize the blockchain network. Therefore, it is necessary to detect blockchain cybercriminal accounts to protect users' assets and sustain the blockchain ecosystem. Many studies have been conducted to detect cybercriminal accounts in the blockchain network. They represented blockchain transaction records as homogeneous transaction graphs that have multi-edge. They also adopted graph learning algorithms to analyze transaction graphs. However, most graph learning algorithms are not efficient in multi-edge graphs, and homogeneous graphs ignore the heterogeneity of the blockchain network. In this paper, we propose a novel heterogeneous graph structure called an account-transaction graph, ATGraph. ATGraph represents multi-edge as single edges by considering transactions as nodes. It allows graph learning more efficiently by eliminating multi-edges. Moreover, we compare the performance of ATGraph with homogeneous transaction graphs in various graph learning algorithms. The experimental results show that the detection performance using ATGraph as input outperforms that using homogeneous graphs as input by up to 0.2 AUROC.

![overview](overall2.png)

### Requirements

The codebase is implemented in Python 3.9.7.
```

torch         1.10.0
dgl-cu111     0.7.2
scikit-learn  0.23.2
tqdm          4.50.2

```

### Dataset

We collect labeled Ethereum addresses from various sources, including normal, phishing, Ponzi, scam, and hack. We collect 1,660 verified phishing addresses and 1,700 normal addresses from [XBlock](https://xblock.pro/), one of the blockchain data platforms. We use a dataset collected in the paper that proposed Ponzi scheme Detection. The dataset includes 200 Ponzi addresses. We also choose 1,189 addresses providing scam from [CryptoScamDB](https://cryptoscamdb.org/scams/). The 826 addresses of hackers who attacked exchanges such as Upbit, Bitpoint, EtherDelta, and Lendf.me were collected from Label Word Cloud at [Etherscan](https://etherscan.io/). Then, we crawl transaction data for each address using the API provided by Etherscan according to the collected addresses. Table I shows a summary of the collected data.

![The Summary of Collected Data](data.png)

### Results

![Results](result.png)
