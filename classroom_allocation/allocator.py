import csv
import random
import re

email_re = re.compile(open("admit_card/email_re.txt").read())

classrooms_cat_map = {
    "Junior": 8,
    "Senior": 3
}

def allocate():
    data = {}
    try:
        with open("classroom_allocation/allocation.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row["email"]] = row["classroom"]
    except FileNotFoundError:
        pass

    with open("csv/admit_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["zone"] != "Online":
                continue
            if not row["email"] or not row["zone"] or not row["category"] or not row["medium"] or not row["contact"]:
                continue
            row["email"] = row["email"].lower()
            if not email_re.match(row["email"]) or not row["email"].endswith("@gmail.com"):
                continue
            if row["email"] not in data:
                data[row["email"]] = row["category"][0] + str(1 + random.choice(range(classrooms_cat_map[row["category"]])))

    with open("classroom_allocation/allocation.csv", "w") as f:
        writer = csv.DictWriter(f, ["email", "classroom"])
        writer.writeheader()
        writer.writerows(
            { "email": k, "classroom": v } for k, v in data.items()
        )