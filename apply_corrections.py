import csv
import json
import os

def run():
    print("Applying corrections...")
    with open("raw_data/corrections.json") as corrections_file:
        corrections = json.load(corrections_file)
        def patch_row(row):
            if corrections_row := corrections.get(row["id"], None):
                print(f"PATCH: Found corrections for ID {row['id']} --", end=' ')
                if corrections_row.get("apply", True):
                    print("Applied.")
                    row.update({k : v for k, v in corrections_row.items() if k in row})
                else:
                    print("Skipped.")
            return row

        for filename in os.listdir("csv/unpatched", ):
            if not filename.endswith("csv"):
                continue
            with open(f"csv/unpatched/{filename}") as read_file:
                with open(f"csv/{filename}", "w") as write_file:
                    reader = csv.DictReader(read_file)
                    row1 = next(reader)
                    writer = csv.DictWriter(write_file, row1.keys())
                    writer.writeheader()
                    if row1["id"] in corrections and corrections[row1["id"]].get("exclude", False):
                        print(f"PATCH: Excluding ID {row1['id']}.")
                    else:
                        writer.writerow(patch_row(row1))
                    for row in reader:
                        if row["id"] in corrections and corrections[row["id"]].get("exclude", False):
                            print(f"PATCH: Excluding ID {row['id']}.")
                            continue
                        writer.writerow(patch_row(row))
    print("-"*140)

if __name__ == "__main__":
    run()