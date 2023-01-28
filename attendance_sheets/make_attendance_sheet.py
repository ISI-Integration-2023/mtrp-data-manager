import pandas as pd

def run():
    data = pd.read_csv("csv/admit_data.csv", dtype=str).dropna(
        subset=['email', 'category', 'zone', 'medium']
    ).sort_values(by=['zone', 'category', 'medium', 'reg_no']).groupby(['zone', 'category'])
    with pd.ExcelWriter("attendance_sheets/attendance_sheet.xlsx") as writer:
        data.get_group(("Kolkata (North)", "Junior")).to_excel(writer, sheet_name="JN", index=False)
        data.get_group(("Kolkata (North)", "Senior")).to_excel(writer, sheet_name="SN", index=False)
        data.get_group(("Kolkata (South)", "Junior")).to_excel(writer, sheet_name="JS", index=False)
        data.get_group(("Kolkata (South)", "Senior")).to_excel(writer, sheet_name="SS", index=False)
        data.get_group(("Durgapur", "Junior")).to_excel(writer, sheet_name="JD", index=False)
        data.get_group(("Durgapur", "Senior")).to_excel(writer, sheet_name="SD", index=False)
        data.get_group(("Online", "Junior")).to_excel(writer, sheet_name="JO", index=False)
        data.get_group(("Online", "Senior")).to_excel(writer, sheet_name="SO", index=False)

if __name__ == '__main__':
    run()