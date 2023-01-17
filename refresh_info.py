import datetime

import townscript.get_data as get_townscript_data
import gsheets.get_data as get_gsheets_data
import compile_contacts
import compile_primer_post_details
import admit_card.compile_admit_data as compile_admit_data
import admit_card.gmail_check as gmail_check
import admit_card.duplication_check as duplication_check
import admit_card.generate_admits as generate_admits
import admit_card.print_breakdown as print_breakdown
import apply_corrections

def main():
    cur_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    print("="*140)
    print(f"MTRP Data Manager -- {cur_time.isoformat()}")
    print("="*140)
    get_townscript_data.run()
    get_gsheets_data.run()
    compile_contacts.run()
    compile_primer_post_details.run()
    compile_admit_data.run()
    apply_corrections.run()
    duplication_check.run()
    gmail_check.run()
    inp = input("Regenerate all admit cards? (y/N): ").lower()
    print("-"*140)
    if len(inp) >= 1 and inp[0] == 'y':
        generate_admits.run()
    print("-"*140)
    print_breakdown.run()

if __name__ == '__main__':
    main()