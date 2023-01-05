import csv
import json
import os

def run():
    with open("raw_data/patches.json") as patch_file:
        patches = json.load(patch_file)
        def patch_row(row):
            row["id"] = int(float(row["id"]))
            if corrections := patches.get(str(row["id"]), None):
                row.update({k : v for k, v in corrections.items() if k in row})
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
                    writer.writerow(patch_row(row1))
                    writer.writerows(patch_row(row) for row in reader)

if __name__ == "__main__":
    run()