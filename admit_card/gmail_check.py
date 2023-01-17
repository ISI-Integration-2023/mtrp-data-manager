import pandas as pd

def run():
    print("ADMIT CARD: Checking for non-Gmail online applications...")
    print("-"*140)

    df = pd.read_csv("csv/admit_data.csv")
    df["email"] = df["email"].str.strip().str.lower()
    s = df["email"].str.endswith("@gmail.com").astype(bool)
    data = df.loc[(~s) & df["zone"].eq("Online")]     \
            .sort_values("name")                      \
            .filter(["id", "reg_no", "name", "contact", "alt_contact", "category", "medium", "email"])
    print(data)
    print("-"*140)


if __name__ == '__main__':
    run()
