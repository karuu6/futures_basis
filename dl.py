from data.bybit import generate_url as generate_bybit_url
from data.binance import generate_url as generate_binance_url

import os
import argparse
import tempfile
from datetime import datetime
from data.utils import unzip_file, gunzip_file, download_file

if __name__ == '__main__':
    """
    Main entry point for the script. Parses arguments and downloads/unzips/untars market data.
    """
    parser = argparse.ArgumentParser(
        prog='Market Data Utility',
        description='Download crypto market data',
    )
    subparsers = parser.add_subparsers(dest='exchange', help='choose exchange')

    parser.add_argument('pair', help='ticker')
    parser.add_argument('type', help='spot or futures',
                        choices=['spot', 'futures'])
    parser.add_argument('date', help='date YYYY-MM-DD')
    parser.add_argument('period', help='data period',
                        choices=['daily', 'monthly'])
    parser.add_argument('output', help='output directory')

    bybit = subparsers.add_parser('bybit', help='Bybit exchange')
    binance = subparsers.add_parser('binance', help='Binance exchange')
    binance.add_argument('-f', help='futures type',
                         choices=['cm', 'um'], required=False)

    args = parser.parse_args()

    try:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    except:
        parser.error('Eror parsing date, use YYYY-MM-DD')

    if args.exchange == 'binance':
        if args.type == 'futures' and args.f is None:
            parser.error('Futures type required for Binance futures data')

        url = generate_binance_url(
            pair=args.pair.upper(),
            pair_type=args.type,
            date=date,
            period=args.period,
            futures_type=args.f
        )

        with tempfile.NamedTemporaryFile() as tmp:
            try:
                download_file(url, tmp.name)
                unzip_file(tmp.name, args.output)
            except Exception as e:
                parser.error(e)

    elif args.exchange == 'bybit':
        if args.type == 'futures' and args.period == 'monthly':
            parser.error('Bybit does not support monthly futures data')

        url = generate_bybit_url(
            pair=args.pair.upper(),
            pair_type=args.type,
            date=date,
            period=args.period
        )

        name = url.split('/')[-1][:-3]

        with tempfile.NamedTemporaryFile() as tmp:
            try:
                download_file(url, tmp.name)
                gunzip_file(tmp.name, os.path.join(args.output, name))
            except Exception as e:
                parser.error(e)
