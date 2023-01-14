import datetime

import townscript.get_data as get_townscript_data
import gsheets.get_data as get_gsheets_data
import mtrp_contacts
import mtrp_primer_post_details
import admit_card.mtrp_admit_data as mtrp_admit_data
import admit_card.mtrp_online_gmail as mtrp_online_gmail
import admit_card.mtrp_admit_dupcheck as mtrp_admit_dupcheck
import admit_card.mtrp_admit_gen as mtrp_admit_gen
import admit_card.mtrp_admit_breakdown as mtrp_admit_breakdown
import patch_errors

def main():
    cur_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    print("="*140)
    print(f"MTRP Data Manager -- {cur_time.isoformat()}")
    print("="*140)
    get_townscript_data.run()
    get_gsheets_data.run()
    mtrp_contacts.run()
    mtrp_primer_post_details.run()
    mtrp_admit_data.run()
    mtrp_admit_dupcheck.run()
    mtrp_online_gmail.run()
    patch_errors.run()
    inp = input("Regenerate all admit cards? (y/N): ").lower()
    print("-"*140)
    if len(inp) >= 1 and inp[0] == 'y':
        mtrp_admit_gen.run()
    print("-"*140)
    mtrp_admit_breakdown.run()

if __name__ == '__main__':
    main()