import os
import sys
from collections import OrderedDict
from datetime import datetime
from pprint import pprint as pp

import numpy as np

from solar_calcs.common.reader import Reader
from solar_calcs.definitions import DATA_DIR


def monthly_usage(data):
    usage_map = {}
    # Create data map with monthly tally
    for row in data:
        date = datetime.strptime(row[1], '%Y-%m-%d')
        key = '-'.join([str(date.year), str(date.strftime("%b"))])
        if key in usage_map.keys():
            usage_map.update({key: {"usage": round(usage_map[key]["usage"] + float(row[-4]), 2),
                                    "cost": round(float(usage_map[key]["cost"]) + float(row[-2][1:]), 2)}}),
        else:
            usage_map.update({key: {"usage": round(float(row[-4]), 2),
                                    "cost": float(row[-2][1:])}})

    # Sort based on cost and usage
    sorted_keys = sorted(usage_map, key=lambda x: (float(usage_map[x]["cost"]), usage_map[x]['usage']), reverse=True)

    # Return entire records with sorted keys
    sorted_data = OrderedDict({key: usage_map[key] for key in sorted_keys})
    return sorted_data


def total_usage(data, return_range):
    """
    :param return_range:
    :param data: raw data from files
    :return:
            total hours, total kwh, total cost, average kwh, average cost,
            top 5 usage records, bottom 5 records
    """
    # sort data on cost and usage to  get top and bottom.
    sorted_data = sorted(data, key=lambda row: (float(row[4]), float(row[6][1:])),
                         reverse=True)  # note how '$x.xx' is treated
    # top 5 and bottom 5 usage data
    bottom_x = sorted_data[-return_range:]
    top_x = sorted_data[:return_range]
    # top_bottom = {"Top 5": sorted_data[-5:],"Bottom 5": sorted_data[:5]}

    # get sum of the cost and usage columns in one round
    # get the $ and usage columns in a float array for calculations
    usage_data = np.array(
        [[row[0], row[1], row[2], row[3], round(float(row[4]), 2), row[5], round(float(row[6][1:]), 2), row[7]] for row
         in sorted_data])

    calc_data = usage_data[:, 4:7:2].astype(np.float)
    sums = np.sum(calc_data, axis=0)
    avgs = np.average(calc_data, axis=0)

    return {'hours': len(usage_data), 'sums': sums, 'avgs': avgs, 'top_x': top_x, 'bottom_x': bottom_x}


def main():
    data = []

    for subdir, dirs, files in os.walk(DATA_DIR):
        for file in files:
            filename = subdir + os.sep + file
            data.extend(Reader(filename, 'pge_electric').read())

    if not data:
        pp('No data read from {}'.format(DATA_DIR))
        sys.exit(1)

    pp(monthly_usage(data))
    usage_stats = total_usage(data, 5)
    pp(np.delete(np.array(usage_stats['top_x']), [0, 5, 7], axis=1))
    pp(np.delete(np.array(usage_stats['bottom_x']), [0, 5, 7], axis=1))
    pp('On average used {0:.2f} kwh, costing ${1:.2f} in {2} hours.'.format(usage_stats['avgs'][0],
                                                                            usage_stats['avgs'][1],
                                                                            usage_stats['hours']))
    pp('Total usage of {0:.2f} kwh, costing ${1:.2f} in {2} hours.'.format(usage_stats['sums'][0],
                                                                           usage_stats['sums'][1],
                                                                           usage_stats['hours']))


if __name__ == '__main__':
    main()
