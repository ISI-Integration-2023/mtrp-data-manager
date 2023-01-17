import os

import pandas as pd

def run():
    print("ADMIT CARD: Current breakdown:")
    print("-"*140)

    data = pd.Series(os.listdir("admit_card/generated")).map(lambda a: a[0:2]).value_counts()
    print(f"Junior Online:   {data['JO']}")
    print(f"Junior North:    {data['JN']}")
    print(f"Junior South:    {data['JS']}")
    print(f"Junior Durgapur: {data['JD']}")
    print(f"Senior Online:   {data['SO']}")
    print(f"Senior North:    {data['SN']}")
    print(f"Senior South:    {data['SS']}")
    print(f"Senior Durgapur: {data['SD']}")
    print("-"*140)

if __name__ == '__main__':
    run()
