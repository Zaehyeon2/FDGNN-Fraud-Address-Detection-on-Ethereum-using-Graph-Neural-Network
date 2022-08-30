# FDGNN: Fraud Address Detection using Graph Neural Network on Ethereum

### Abstract

Cybercrimes that exploit the anonymity of blockchain are increasing in the Ethereum network. Cybercrimes that exploit Ethereum steal users’ assets and cause sudden price volatility, destabilizing the Ethereum network. To prevent cybercrimes in the Ethereum network, node classification-based studies have been conducted to detect cybercriminal accounts. However, the actual role of most Ethereum nodes is unknown owing to the anonymity of the blockchain. This leads to an incomplete label problem in the node-classification-based detection model. In this paper, we propose a graph neural network-based cybercriminal account detection method that considers the incomplete label problem. We perform graph classification rather than node classification to address the incomplete label problem. Moreover, we design an account-transaction graph, which is a directed graph of Ethereum transactions, for graph classification. The experimental results show that the proposed method outperforms the node classification-based method by 0.07 with respect to the F1 score.

![overview](overall.png)

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

