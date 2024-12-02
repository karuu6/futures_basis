def _bar_map(row: list):
    return {
        'time': int(row[0]),
        'open': float(row[1]),
        'high': float(row[2]),
        'low': float(row[3]),
        'close': float(row[4]),
        'volume': float(row[5])
    }
