"""
This code is used to calculate the speedup for CICDDoS2019 trace
   - Run this command `./tcpdump-stats SAT-01-12-2018_* -t 1 2>&1 | tee statistics` in 
     `/euler/CICDDoS2019/data` to generate `statistics`
   - python calc_speedup.py /euler/CICDDoS2019/data/statistics
"""
from shutil import ExecError
import pandas as pd
import numpy as np
import sys


TARGET_THPT_IN_GPS = 100

if __name__ == "__main__":
    name = sys.argv[1]

    with open(name) as f:
        lines = f.readlines()
        lines = list(filter(lambda x: "truncated" not in x, lines))
        thpt_list = []
        for i in range(0, len(lines), 3):
            thpt_line = lines[i+2]
            tokens = thpt_line.split()
            val = float(tokens[-2])
            unit = tokens[-1]
            if unit == "Kbps":
                thpt_list.append(val * (10 ** 3))
            elif unit == "Mbps":
                thpt_list.append(val * (10 ** 6))
            else:
                raise Exception("Not valid unit")

        speedup = int((TARGET_THPT_IN_GPS * (10 ** 9)) / max(thpt_list))
        print("Needs {}X speedup".format(speedup))


