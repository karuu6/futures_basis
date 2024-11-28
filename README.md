# Futures Basis Analysis

This repository contains tools and scripts for fetching and analyzing the cryptocurrency basis effect.

## Usage

### Prerequisites

Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

### Fetching Data

To fetch data from Binance, use the `binance_data.py` script. Below is an example of how to use the script to fetch monthly futures trades:

```bash
python binance_data.py data/ 2024-10-22 BTCUSDT monthly -f -t um
```

### Example

Fetch daily spot trades for ETHUSDT

```bash
python binance_data.py data/ 2024-10-22 BTCUSDT monthly -f -t um
```

### Output

The script will store the CSV data in specified directory.
