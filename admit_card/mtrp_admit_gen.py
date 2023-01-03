import phonenumbers as ph

from popplerqt5 import Poppler
import csv

def generate_admit(data : dict):
    admit_base = None
    if data["roll_no"][1] == 'O':
        admit_base = Poppler.Document.load("admit_card/templates/MTRP Admit Card (Online, Fillable).pdf")
    else:
        admit_base = Poppler.Document.load("admit_card/templates/MTRP Admit Card (Offline, Fillable).pdf")

    for field in admit_base.page(0).formFields():
        if field.fullyQualifiedName() in data.keys():
            field.setText(data[field.fullyQualifiedName()])
            field.setReadOnly(True)

    admit_base.setTitle(f"MTRP 2023 Admit Card - {data['roll_no']}")
    admit_base.setAuthor(f"MTRP 2023 Team")
    admit_base.setCreator(f"Poppler 22.12.0 (https://poppler.freedesktop.org)")

    converter = admit_base.pdfConverter()
    converter.setOutputFileName(f"admit_card/generated/{data['roll_no']}.pdf")
    converter.setPDFOptions(Poppler.PDFConverter.PDFOption(1))
    converter.convert()

zone_venue_map = {
    "Kolkata (North)": "Indian Statistical Institute, Kolkata\n203, B.T. Road, Baranagar, Kolkata - 700108",
    "Kolkata (South)": "Ramakrishna Mission Vidyalaya\nNarendrapur, Kolkata - 700103",
    "Durgapur": "DAV Model School\nJM Sengupta Road, B-Zone, Durgapur - 713205",
    "Online": ""
}

zone_code_map = {
    "Kolkata (North)": "N",
    "Kolkata (South)": "S",
    "Durgapur": "D",
    "Online": "O"
}

def transform_data(data : dict):
    roll_no = data["category"][0] + zone_code_map[data["zone"]] + data["reg_no"].replace("ON", '').replace("RM", '')
    return {
        "roll_no": roll_no,
        "reg_no": data["reg_no"],
        "name": data["name"].upper(),
        "dob": data["dob"],
        "email": data["email"],
        "phone1": ph.format_number(ph.parse(data['contact']), ph.PhoneNumberFormat.INTERNATIONAL),
        "phone2": ph.format_number(ph.parse(data['alt_contact']), ph.PhoneNumberFormat.INTERNATIONAL) if data['alt_contact'] else '',
        "category": data["category"],
        "medium": data["medium"],
        "exam_date": "01 January 1970",
        "rep_time": "00:00",
        "exam_time": "00:00 - 23:59",
        "exam_venue": zone_venue_map[data["zone"]]
    }

def run():
    with open("csv/mtrp_admit_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            generate_admit(transform_data(row))

if __name__ == '__main__':
    run()