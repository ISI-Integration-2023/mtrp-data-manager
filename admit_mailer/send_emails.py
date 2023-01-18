import os
import json

from multiprocessing import Pool

import email
import smtplib

creds = json.load(open("admit_mailer/credentials.json"))

def roll_check(roll_no : str):
    # Block all printed forms, SciAstra, online forms.
    return (int(roll_no[4:6]) < 20) and (roll_no[1] != 'O')

def send_email(roll_no : str):
    with smtplib.SMTP("mail.isical.ac.in", 500) as smtp:
        try:
            with open(f"admit_mailer/emails/{roll_no}.eml", "rb") as fp:
                #smtp.login(user=creds['username'], password=creds['password'])
                msg = email.message_from_binary_file(fp)
                smtp.send_message(msg)
            print(f"ADMIT MAILER: Sent admit card for {roll_no}.")
            with open("admit_mailer/sent.txt", "a") as sent:
                sent.write(roll_no + "\n")
        except FileNotFoundError:
            return None

def run():
    sent = [roll_no.strip() for roll_no in open("admit_mailer/sent.txt").readlines()]
    roll_nos = (filename.replace('.eml', '') for filename in os.listdir("admit_mailer/emails") if 'eml' in filename)
    roll_nos = [roll_no for roll_no in roll_nos if roll_no not in sent and roll_check(roll_no)]
    roll_nos = roll_nos[:30]
    print(f"ADMIT MAILER: Sending for the following roll numbers... ({len(roll_nos)})")
    print("-"*140)
    print(roll_nos)
    print("-"*140)
    inp = input("Proceed? (y/N): ").lower()
    print("-"*140)
    if len(inp) >= 1 and inp[0] == 'y':
        with Pool(10) as pool:
            pool.map(send_email, roll_nos)