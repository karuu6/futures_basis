# Futures Basis Analysis

This repository contains tools and scripts for fetching and analyzing the cryptocurrency basis effect.

## Usage

### Prerequisites

Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

### Fetching Data

To download market data, use the `dl.py` script. Below is an example of how to use the script to fetch monthly futures trades from Binance:

```bash
python dl.py BTCUSDT 2024-11-01 2024-11-03 market_data binance 5m futures --type=um
```

### Example

Fetch daily spot trades for ETHUSDT on Bybit

```bash
python dl.py ETHUSDT 2024-11-01 2024-11-03 market_data bybit 5m spot 
```

Note that Bybit requires VPN for U.S. users
