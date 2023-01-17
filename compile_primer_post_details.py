import pandas as pd

def run():
    data_offline = pd.read_csv("raw_data/offline.csv")
    data_offline["Attendee Name"] = data_offline["Attendee First Name"] + " " + \
        data_offline["Attendee Last Name"]
    data_online = pd.read_csv("raw_data/online.csv")
    data_online["Attendee Name"] = data_online["Attendee First Name"] + " " + \
        data_online["Attendee Last Name"]
    data_primer = pd.read_csv("raw_data/primer.csv")


    s = "MTRP Problem Primer (@ 33% Discount!!)             (Rs. 200 + Rs. 70 Delivery to your Doorstep)"

    map_base = {
        "Registration Id": "id",
        "Attendee Name": "name",
        "Attendee Email": "email",
        "Contact Number": "contact",
        "Alternate Contact Number": "alt_contact",
        "Address": "address",
        "City": "city",
        "State (India)": "state",
        "Pincode/Zipcode/Postcode": "pincode"
    }

    map1 = {
        **map_base,
        "Category (see Rules & Regulations*)": "category"
    }

    map2 = {
        **map_base,
        "Which Category Book do you want? (see Rules & Regulations*)": "category"
    }

    data_combined = pd.concat([
        data_offline.where(data_offline[s].str.contains("Yes")).dropna(how='all').rename(
            columns=map1).filter(map1.values()),

        data_online.where(data_online[s].str.contains("Yes")).dropna(how='all').rename(
            columns=map1).filter(map1.values()),

        data_primer.rename(columns=map2).filter(
            map2.values())
    ], ignore_index=True)

    data_combined["contact"] = data_combined["contact"].map(
        lambda e: e.replace('"', '').replace('=', ''))
    data_combined["alt_contact"] = data_combined["alt_contact"].map(
        lambda e: e.replace('"', '').replace('=', ''), na_action = 'ignore')

    data_combined["category"] = data_combined["category"].map(
        lambda e: "Junior" if "Junior" in e else "Senior")
    data_combined["state"] = data_combined["state"].map(
        lambda e: e.replace('"', '').replace('=', ''))

    data_combined.sort_values(by=["pincode", "category", "id"], ignore_index=True, inplace=True)

    data_combined.to_csv("csv/unpatched/primer_post_details.csv", index=False)

if __name__ == '__main__':
    run()