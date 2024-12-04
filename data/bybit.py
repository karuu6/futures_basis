from datetime import datetime
import requests
import time
from .utils import _bar_map


_BASE_URL = 'https://api.bybit.com'


def download_bars(product: str, timeframe: str, symbol: str, start: datetime, end: datetime):
    url = f'{_BASE_URL}/v5/market/kline'

    # Convert datetime to timestamp
    start_timestamp = int(start.timestamp()) * 1000
    end_timestamp = (int(end.timestamp()) - 1) * 1000  # Make end exclusive

    bars = []
    while start_timestamp < end_timestamp:
        response = requests.get(url, params={
            'category': product,
            'symbol': symbol,
            'interval': timeframe,
            'start': start_timestamp,
            'end': end_timestamp,
            'limit': 1000
        })

        if response.status_code != 200:
            raise ValueError(response.status_code, response.content)

        data = response.json()['result']['list']
        bars.extend(data)

        if len(data) < 1000:
            break

        end_timestamp = int(data[-1][0]) - 1000  # Avoid duplicates
        time.sleep(0.5)  # Rate limit

    return list(map(_bar_map, reversed(bars)))


if __name__ == '__main__':
    # Example usage
    start = datetime(2021, 1, 1)
    end = datetime(2021, 1, 2)
    bars = download_bars('linear', '1', 'BTCUSD', start, end)

    from pprint import pprint
    print(bars)
