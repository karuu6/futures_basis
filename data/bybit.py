from datetime import datetime


_BASE_URL = 'https://public.bybit.com'


def generate_url(pair: str, pair_type: str, date: datetime, period: str) -> str:
    """
    Generate the URL for downloading Bybit market data.

    Args:
        pair (str): The trading pair.
        date (str): The date for the data.
        pair_type (str): The type of pair ('spot' or 'futures').
        period (str): The data period ('daily' or 'monthly').

    Returns:
        str: The generated URL.
    """

    n_pair_type = 'spot' if pair_type == 'spot' else 'trading'
    ret = f'{_BASE_URL}/{n_pair_type}/{pair}/{pair}'

    date_str = date.strftime(
        '%Y-%m-%d') if period == 'daily' else date.strftime('%Y-%m')

    if pair_type == 'futures':
        ret += f'{date_str}.csv.gz'
    else:
        ret += f'_{date_str}.csv.gz'

    return ret
