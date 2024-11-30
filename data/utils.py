import csv
import gzip
import shutil
import zipfile
import requests


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
        for chunk in response.iter_content(1024 * 64):  # 64KB chunks
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


def gunzip_file(gzip_path: str, output_path: str) -> None:
    """
    Gunzip a gzip file to a specified directory.

    Args:
        gzip_path (str): The path to the gzip file.
        output_path (str): The path to extract the contents to.
    """
    with gzip.open(gzip_path, 'rb') as gzip_ref:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(gzip_ref, f_out)


def binance_resample(file: str, frequency: int):
    """
    Resamples the given CSV file containing Binance trades.

    Args:
        file (str): The path to the CSV file containing the data.
        frequency (int): The resampling frequency in seconds.

    Returns:
        generator: A generator that yields time-sampled bars as dictionaries with the following keys:
            - 'time': The start time of the resampled period.
            - 'open': The opening price of the resampled period.
            - 'high': The highest price during the resampled period.
            - 'low': The lowest price during the resampled period.
            - 'close': The closing price of the resampled period.
            - 'volume': The total volume traded during the resampled period.
            - 'buyer_aggressor_volume': The volume of trades where the buyer was the aggressor during the resampled period.

    Note:
        The input CSV file is expected to have the following columns:
            - 'time': The timestamp of the trade in milliseconds.
            - 'qty': The quantity traded.
            - 'price': The price at which the trade occurred.
            - 'is_buyer_maker': A boolean indicating if the buyer is the market maker ('true' or 'false').
    """

    t0 = None
    op = None
    hi = None
    lo = None
    cl = None
    sz = None
    ag = None

    frequency = frequency * 1000  # convert to milliseconds
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = int(row['time'])
            q = float(row['qty'])
            p = float(row['price'])
            a = 0 if row['is_buyer_maker'] == 'true' else 1

            if t0 is None:
                t0 = t - t % frequency
                op = p
                hi = p
                lo = p
                cl = p
                sz = q
                ag = q * a

            elif t > t0 + frequency:  # binance data is in milliseconds
                yield {
                    'time': t0,
                    'open': op,
                    'high': hi,
                    'low': lo,
                    'close': cl,
                    'volume': sz,
                    'buyer_aggressor_volume': ag
                }

                t0 += frequency
                op = p
                hi = p
                lo = p
                cl = p
                sz = q
                ag = q * a

            else:
                cl = p
                sz += q
                ag += q * a
                hi = max(hi, p)
                lo = min(lo, p)

        yield {
            'time': t0,
            'open': op,
            'high': hi,
            'low': lo,
            'close': cl,
            'volume': sz,
            'buyer_aggressor_volume': ag
        }


if __name__ == '__main__':
    for bar in binance_resample('market_data/BTCUSDT-trades-2024-11-11.csv', 600):
        print(bar)
        input()
