import argparse
import os
import csv
from data import binance, bybit
from datetime import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download historical data from exchanges')

    # Required arguments at the top level
    parser.add_argument('symbol', type=str, help='trading symbol')
    parser.add_argument('start', type=str, help='start date')
    parser.add_argument('end', type=str, help='end date')
    parser.add_argument('output', type=str, help='output directory')

    # Top-level subparsers for exchanges
    subparsers = parser.add_subparsers(
        dest='exchange', help='choose exchange', required=True)

    # 'binance' subcommand
    binance_parser = subparsers.add_parser('binance')
    binance_parser.add_argument('timeframe',  help='bars timeframe', type=str, choices=[
                                '1s', '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'])

    binance_subparsers = binance_parser.add_subparsers(
        dest='product', required=True)

    # 'spot' under 'binance'
    binance_subparsers.add_parser('spot')

    # 'futures' under 'binance'
    futures_parser = binance_subparsers.add_parser('futures')
    futures_parser.add_argument(
        '--type', choices=['cm', 'um'], required=True, help='futures type (cm or um)')

    # 'bybit' subcommand
    bybit_parser = subparsers.add_parser('bybit')
    bybit_parser.add_argument('timeframe',  help='bars timeframe', type=str, choices=[
                              '1', '3', '5', '15', '30', '60', '120', '240', '360', '720', 'D', 'M', 'W'])

    bybit_subparsers = bybit_parser.add_subparsers(
        dest='product', required=True)

    # Market types for 'bybit'
    bybit_subparsers.add_parser('spot')
    bybit_subparsers.add_parser('linear', help='linear futures')
    bybit_subparsers.add_parser('inverse', help='inverse futures')

    # Parse arguments
    args = parser.parse_args()

    try:
        start = datetime.strptime(args.start, '%Y-%m-%d')
        end = datetime.strptime(args.end, '%Y-%m-%d')
    except:
        parser.error('Invalid date format. Use YYYY-MM-DD')

    if args.exchange == 'binance':
        if args.product == 'futures':
            product = args.type
        else:
            product = args.product

        try:
            bars = binance.download_bars(
                product=product,
                timeframe=args.timeframe,
                symbol=args.symbol,
                start=start,
                end=end
            )
        except Exception as e:
            parser.error(f'Failed to download bars: {e}')

    elif args.exchange == 'bybit':
        try:
            bars = bybit.download_bars(
                product=args.product,
                timeframe=args.timeframe,
                symbol=args.symbol,
                start=start,
                end=end
            )
        except Exception as e:
            parser.error(f'Failed to download bars: {e}')

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    file = f'{args.exchange}-{args.product}-{args.symbol}-{args.timeframe}.csv'
    file = os.path.join(args.output, file)

    with open(file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=bars[0].keys())
        writer.writeheader()
        writer.writerows(bars)
