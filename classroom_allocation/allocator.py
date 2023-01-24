import pandas as pd
import numpy as np
import re

email_re = re.compile(open("admit_card/email_re.txt").read())

JUNIOR_CLASSROOMS = 8
SENIOR_CLASSROOMS = 6

def allocate():
    df = pd.read_csv("csv/admit_data.csv")
    existing = pd.read_csv("classroom_allocation/allocation.csv")
    e_list = existing["email"].to_list()
    df["zone"] = df["zone"].map(lambda e: e if e == "Online" else None)
    df["email"] = df["email"].str.lower().map(lambda e: e if email_re.match(e) and e.endswith("@gmail.com") else None)
    df["email"] = df["email"][~ df["email"].isin(e_list)]
    df = df.dropna(subset=["email", "zone", "category", "medium", "contact"]).sample(frac=1)
    df_junior = df[df["category"] == "Junior"]
    df_senior = df[df["category"] == "Senior"]
    dfs_junior = np.array_split(df_junior, JUNIOR_CLASSROOMS)
    dfs_senior = np.array_split(df_senior, SENIOR_CLASSROOMS)
    for i, j in enumerate(dfs_junior):
        j["classroom"] = f"J{(i+1):02}"
    for i, s in enumerate(dfs_senior):
        s["classroom"] = f"S{(i+1):02}"
    df = pd.concat([existing] + dfs_junior + dfs_senior, ignore_index=True).filter(["email", "classroom"])
    df.to_csv("classroom_allocation/allocation.csv", index=False)