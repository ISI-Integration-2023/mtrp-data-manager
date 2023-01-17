import os
from collections import defaultdict

import pandas as pd

from admit_card.generate_admits import zone_code_map


def generate_prefix_code(data):
    return data["category"][0] + zone_code_map[data["zone"]] + data["medium"][0]


def run():
    data = pd.read_csv("csv/admit_data.csv").dropna(
        subset=['email', 'category', 'zone', 'medium']
    ).apply(generate_prefix_code, axis=1).value_counts()

    print(f"ADMIT CARD: Current breakdown -- {data.sum()} candidates with generatable admits:")
    print("-"*140)

    data = defaultdict(int) | data.to_dict()

    print(f"Junior Online:   {data['JOE']:>3} (EN) + {data['JOB']:>3} (BN)")
    print(f"Junior North:    {data['JNE']:>3} (EN) + {data['JNB']:>3} (BN)")
    print(f"Junior South:    {data['JSE']:>3} (EN) + {data['JSB']:>3} (BN)")
    print(f"Junior Durgapur: {data['JDE']:>3} (EN) + {data['JDB']:>3} (BN)")

    print(f"Senior Online:   {data['SOE']:>3} (EN) + {data['SOB']:>3} (BN)")
    print(f"Senior North:    {data['SNE']:>3} (EN) + {data['SNB']:>3} (BN)")
    print(f"Senior South:    {data['SSE']:>3} (EN) + {data['SSB']:>3} (BN)")
    print(f"Senior Durgapur: {data['SDE']:>3} (EN) + {data['SDB']:>3} (BN)")
    print("-"*140)


if __name__ == '__main__':
    run()
