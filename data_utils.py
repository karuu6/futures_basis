import csv


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
    for bar in binance_resample('data/ETHUSDT-trades-2024-11-11.csv', 600):
        print(bar)
        input()
