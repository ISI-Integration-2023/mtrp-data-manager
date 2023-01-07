import townscript.get_data as get_townscript_data
import gsheets.get_data as get_gsheets_data
import mtrp_contacts
import mtrp_primer_post_details
import admit_card.mtrp_admit_data as mtrp_admit_data
import admit_card.mtrp_admit_gen as mtrp_admit_gen
import patch_errors

def main():
    get_townscript_data.run()
    get_gsheets_data.run()
    mtrp_contacts.run()
    mtrp_primer_post_details.run()
    mtrp_admit_data.run()
    patch_errors.run()
    inp = input("Regenerate all admit cards? (y/N): ").lower()
    if len(inp) >= 1 and inp[0] == 'y':
        mtrp_admit_gen.run()

if __name__ == '__main__':
    main()