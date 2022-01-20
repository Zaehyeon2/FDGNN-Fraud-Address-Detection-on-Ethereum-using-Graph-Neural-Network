# FDGNN: Fraud-Address-Detection-on-Ethereum-using-Graph-Neural-Network

### Abstract

Ethereum is a cryptocurrency platform that allows users to transact anonymously by blockchain technology. However, cryptocurrencies are used for cybercrimes that exploit anonymity. The cybercrimes using cryptocurrencies are increasing every year, a main threat to the cryptocurrency ecosystem. This paper proposes fraudulent address detection on Ethereum using a graph neural network to prevent cybercrimes using cryptocurrencies. Furthermore, we propose a novel graph structure called ATGraph to analyze blockchain transactions. We conducted experiments to detect fraud addresses on real Ethereum transaction data. The experimental results show that the proposed FDGNN achieved up to 0.24 higher f1-score than other methods.

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

