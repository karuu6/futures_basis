import zipfile
import requests
import argparse
import tempfile
from enum import Enum
from typing import Optional
from datetime import datetime


class PairType(Enum):
    """Enumeration for pair types."""
    SPOT = 'spot'
    FUTURES = 'futures'


class FuturesType(Enum):
    """Enumeration for futures types."""
    COINM = 'cm'
    USDM = 'um'


class Period(Enum):
    """Enumeration for data periods."""
    DAILY = 'daily'
    MONTHLY = 'monthly'


BASE_URL = 'https://data.binance.vision/data'


def generate_url(period: Period, pair: str, pair_type: PairType, date: datetime | str, futures_type: Optional[FuturesType]) -> str:
    """
    Generate the URL for downloading Binance market data.

    Args:
        period (Period): The data period (daily or monthly).
        pair (str): The trading pair.
        pair_type (PairType): The type of pair (spot or futures).
        date (datetime | str): The date for the data.
        futures_type (Optional[FuturesType]): The type of futures (required if pair_type is FUTURES).

    Returns:
        str: The generated URL.
    """
    if pair_type == PairType.FUTURES and futures_type is None:
        raise ValueError('futures_type is required for `FUTURES` pair type')

    ret = f'{BASE_URL}/{pair_type.value}/'
    if pair_type == PairType.FUTURES:
        ret += f'{futures_type.value}/'

    date_str = date.strftime(
        "%Y-%m-%d") if period == Period.DAILY else date.strftime("%Y-%m")
    ret += f'{period.value}/trades/{pair}/{pair}-trades-{date_str}.zip'
    return ret


def download_file(url: str, output_path: str) -> None:
    """
    Download a file from a URL.

    Args:
        url (str): The URL to download the file from.
        output_path (str): The path to save the downloaded file.
    """
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise ValueError(
            'Error downloading file, status code: ', response.status_code)

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(4096):  # 4KB chunks
            f.write(chunk)


def unzip_file(zip_path: str, output_dir: str) -> None:
    """
    Unzip a zip file to a specified directory.

    Args:
        zip_path (str): The path to the zip file.
        output_dir (str): The directory to extract the contents to.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


if __name__ == '__main__':
    """
    Main entry point for the script. Parses arguments and downloads/unzips Binance market data.
    """
    parser = argparse.ArgumentParser(
        prog='Binance Market Data Utility',
        description='Download Binance market data',
    )

    parser.add_argument('output', help='output directory')
    parser.add_argument('date', help='date YYYY-MM-DD')
    parser.add_argument('pair', help='binance ticker')
    parser.add_argument('period', help='data period',
                        choices=['daily', 'monthly'])
    parser.add_argument('-f', '--futures',
                        help='download futures data', action='store_true')
    parser.add_argument('-t', '--type', help='futures type',
                        choices=['cm', 'um'], required=False)

    args = parser.parse_args()
    if args.futures and args.type is None:
        parser.error('--type is required for futures data')

    try:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    except:
        parser.error('Eror parsing date, use YYYY-MM-DD')

    period = Period.DAILY if args.period == 'daily' else Period.MONTHLY
    pair_type = PairType.SPOT if args.futures else PairType.FUTURES
    futures_type = FuturesType.COINM if args.type == 'cm' else FuturesType.USDM

    url = generate_url(
        period=period,
        pair=args.pair.upper(),
        pair_type=pair_type,
        date=date,
        futures_type=futures_type
    )

    with tempfile.NamedTemporaryFile() as tmp:
        try:
            download_file(url, tmp.name)
            unzip_file(tmp.name, args.output)
        except Exception as e:
            parser.error(f'Error downloading file: {e}')
