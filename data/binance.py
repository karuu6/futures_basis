from datetime import datetime
import requests
import time
from .utils import _bar_map

_BASE_UM_URL = 'https://fapi.binance.com'
_BASE_CM_URL = 'https://dapi.binance.com'
_BASE_SPOT_URL = 'https://api.binance.com'


def download_bars(product: str, timeframe: str, symbol: str, start: datetime, end: datetime):
    if product == 'spot':
        url = f'{_BASE_SPOT_URL}/api/v3/klines'
    elif product == 'cm':
        url = f'{_BASE_CM_URL}/dapi/v1/klines'
    elif product == 'um':
        url = f'{_BASE_UM_URL}/fapi/v1/klines'
    else:
        raise ValueError(f'Invalid product: {product}')

    # Convert datetime to timestamp
    start_timestamp = int(start.timestamp()) * 1000
    end_timestamp = (int(end.timestamp()) - 1) * 1000  # Make end exclusive

    bars = []
    while start_timestamp < end_timestamp:
        response = requests.get(url, params={
            'symbol': symbol,
            'interval': timeframe,
            'startTime': start_timestamp,
            'endTime': end_timestamp,
            'limit': 1000
        })

        if response.status_code != 200:
            raise ValueError(response.status_code, response.content)

        data = response.json()
        bars.extend(data)

        if len(data) < 1000:
            break

        start_timestamp = int(data[-1][0]) + 1000  # Avoid duplicates
        time.sleep(0.5)  # Rate limit
    return list(map(_bar_map, bars))


if __name__ == '__main__':
    # Example usage
    start = datetime(2021, 1, 1)
    end = datetime(2021, 1, 2)
    bars = download_bars('spot', '30m', 'BTCUSDT', start, end)

    from pprint import pprint
    pprint(bars)
