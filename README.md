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
python dl.py binance -fum BTCUSDT futures 2024-11-01 daily market_data/
```

### Example

Fetch daily spot trades for ETHUSDT on Bybit

```bash
python dl.py bybit ETHUSDT spot 2024-10-22 daily market_data/
```