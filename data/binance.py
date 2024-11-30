from datetime import datetime


_BASE_URL = 'https://data.binance.vision/data'


def generate_url(pair: str, pair_type: str, date: datetime, period: str, futures_type: str = 'um') -> str:
    """
    Generate the URL for downloading Binance market data.

    Args:
        period (str): The data period ('daily' or 'monthly').
        pair (str): The trading pair.
        pair_type (str): The type of pair ('spot' or 'futures').
        date (datetime): The date for the data.
        futures_type (str): The type of futures ('cm' or 'um', defaults to 'um').

    Returns:
        str: The generated URL.
    """
    ret = f'{_BASE_URL}/{pair_type}/'
    if pair_type == 'futures':
        ret += f'{futures_type}/'

    if period == 'daily':
        date_str = date.strftime('%Y-%m-%d')
    else:
        date_str = date.strftime('%Y-%m')

    ret += f'{period}/trades/{pair}/{pair}-trades-{date_str}.zip'

    return ret
