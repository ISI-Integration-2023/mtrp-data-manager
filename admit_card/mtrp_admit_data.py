import pandas as pd

def run():
    data_offline = pd.read_csv("raw_data/offline.csv")
    data_offline["Attendee Name"] = (data_offline["Attendee First Name"] + " " + \
        data_offline["Attendee Last Name"]).map(lambda e: e.replace("  ", " "))
    data_online = pd.read_csv("raw_data/online.csv")
    data_online["Attendee Name"] = (data_online["Attendee First Name"] + " " + \
        data_online["Attendee Last Name"]).map(lambda e: e.replace("  ", " "))

    data_online["Preferred Exam Zone"] = "Online"

    col_map = {
        "Registration Id": "id",
        "Sequence Value": "reg_no",
        "Attendee Name": "name",
        "Date of Birth": "dob",
        "Attendee Email": "email",
        "Contact Number": "contact",
        "Alternate Contact Number": "alt_contact",
        "Category (see Rules & Regulations*)": "category",
        "Preferred Medium": "medium",
        "Preferred Exam Zone": "zone"
    }

    data_combined = pd.concat([
        data_offline.rename(
            columns=col_map).filter(col_map.values()),

        data_online.rename(
            columns=col_map).filter(col_map.values()),
    ], ignore_index=True)

    data_combined["dob"] = data_combined["dob"].map(
        lambda e: '-'.join(reversed(e.replace('=', '').replace('"', '').split('-'))))

    data_combined["contact"] = data_combined["contact"].map(
        lambda e: e.replace('"', '').replace('=', ''))
    data_combined["alt_contact"] = data_combined["alt_contact"].map(
        lambda e: e.replace('"', '').replace('=', ''), na_action = 'ignore')

    data_combined["category"] = data_combined["category"].map(
        lambda e: "Junior" if "Junior" in e else "Senior")

    data_combined["medium"] = data_combined["medium"].map(
        lambda e: e.replace('=', '').replace('"', '').split(",")[0])

    data_combined["zone"] = data_combined["zone"].map(
        lambda e: e.replace('=', '').replace('"', '').split(",")[0])

    data_combined.to_csv("csv/unpatched/mtrp_admit_data.csv", index=False)

if __name__ == '__main__':
    run()