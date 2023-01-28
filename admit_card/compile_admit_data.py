import pandas as pd

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

col_map_printed = {
    "ID": "id",
    "Registration No.": "reg_no",
    "Name": "name",
    "dob": "dob",
    "Email Address": "email",
    "Mobile No.": "contact",
    "Alternate Mobile No.": "alt_contact",
    "category": "category",
    "Medium": "medium",
    "Preferred Exam Zone": "zone"
}

col_map_sciastra = {
    "rzp_id": "id",
    "reg_no": "reg_no",
    "full_name": "name",
    "date_of_birth": "dob",
    "email": "email",
    "phone": "contact",
    "alternate_phone_number": "alt_contact",
    "category": "category",
    "medium": "medium",
    "zone": "zone"
}

def rzp_date_processor(e):
    date, time = e.split(' ')
    date = '-'.join(reversed(date.split('/')))
    return date + ' ' + time

def run():
    data_offline = pd.read_csv("raw_data/offline.csv")
    data_offline["Attendee Name"] = (data_offline["Attendee First Name"] + " " +
                                     data_offline["Attendee Last Name"]).map(lambda e: e.replace("  ", " "))
    data_online = pd.read_csv("raw_data/online.csv")
    data_online["Attendee Name"] = (data_online["Attendee First Name"] + " " +
                                    data_online["Attendee Last Name"]).map(lambda e: e.replace("  ", " "))
    data_online["Preferred Exam Zone"] = "Online"
    data_printed = pd.read_csv("raw_data/printed.csv")
    data_printed["category"] = (data_printed["Class"] > 10).map(
        lambda e: "Senior" if e else "Junior")
    data_printed["dob"] = "Unspecified"

    data_sciastra = pd.read_csv("raw_data/sciastra.csv", dtype=str)
    data_sciastra = data_sciastra[data_sciastra['payment status'] == 'captured']
    data_sciastra['rzp_id'] = data_sciastra['payment id'].map(lambda e: e.split('_')[1])
    data_sciastra['payment date'] = data_sciastra['payment date'].map(rzp_date_processor)
    data_sciastra.sort_values('payment date', inplace=True, ignore_index=True)
    data_sciastra['reg_no'] = pd.Series(range(len(data_sciastra))).map(lambda i: f"SCI23{(i+1):05}")
    data_sciastra['full_name'] = data_sciastra['full_name'].str.strip()
    data_sciastra['phone'] = data_sciastra['phone'].map(lambda e: e if e.startswith("+") else "+91" + e)
    data_sciastra['alternate_phone_number'] = data_sciastra['alternate_phone_number'].map(lambda e: e if e.startswith("+") else "+91" + e[-10:])
    data_sciastra["medium"] = "English"
    data_sciastra["zone"] = "Online"
        
    data_combined = pd.concat([
        data_offline.rename(
            columns=col_map).filter(col_map.values()),

        data_online.rename(
            columns=col_map).filter(col_map.values()),

        data_printed.rename(
            columns=col_map_printed).filter(col_map_printed.values()),

        data_sciastra.rename(
            columns=col_map_sciastra).filter(col_map_sciastra.values()),
    ], ignore_index=True)

    data_combined["dob"] = data_combined["dob"].map(
        lambda e: '-'.join(reversed(e.replace('=', '').replace('"', '').split('-'))), na_action='ignore')

    data_combined["contact"] = data_combined["contact"].map(
        lambda e: e.replace('"', '').replace('=', '').replace(' ', ''), na_action='ignore')
    data_combined["alt_contact"] = data_combined["alt_contact"].map(
        lambda e: e.replace('"', '').replace('=', '').replace(' ', ''), na_action='ignore')

    data_combined["category"] = data_combined["category"].map(
        lambda e: "Junior" if "Junior" in e else "Senior", na_action='ignore')

    data_combined["medium"] = data_combined["medium"].map(
        lambda e: e.replace('=', '').replace('"', '').split(",")[0], na_action='ignore')

    data_combined["zone"] = data_combined["zone"].map(
        lambda e: e.replace('=', '').replace('"', '').split(",")[0], na_action='ignore')

    data_combined["id"] = data_combined["id"].map(lambda e: str(e).replace('.0', ''))

    data_combined.drop_duplicates(inplace=True, ignore_index=True)
    data_combined.to_csv("csv/unpatched/admit_data.csv", index=False)


if __name__ == '__main__':
    run()
