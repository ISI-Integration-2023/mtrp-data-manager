import os
import pandas as pd

from multiprocessing import Pool

import email
import smtplib

creds = json.load(open("admit_mailer/credentials.json"))
msg = email.message_from_binary_file(open(f"brochure_mailer/msg_to_schools.eml", "rb"))

def send_email(name : str, email : str):
    with smtplib.SMTP("mail.isical.ac.in", 500) as smtp:
        msg["To"] = email.headerregistry.Address(name, *(email.lower().split('@')[:2]))
        smtp.send_message(msg)
        print(f"BROCHURE MAILER: Sent brochure to {name} <{email}>.")
        with open("brochure_mailer/sent.txt", "a") as sent:
            sent.write(email + "\n")

def run():
    sent = [email.strip() for email in open("brochure_mailer/sent.txt").readlines()]
    data = [(name, email) for name, email in pd.read_csv("brochure_mailer/schools.csv").dropna(how='any').to_dict().items() if email not in sent][:50]
    print(f"BROCHURE MAILER: Sending for the following adresses... ({len(data)})")
    print("-"*140)
    for name, email in data:
        print(f"{name} \t\t<{email}>")
    print("-"*140)
    inp = input("Proceed? (y/N): ").lower()
    print("-"*140)
    if len(inp) >= 1 and inp[0] == 'y':
        with Pool(10) as pool:
            pool.starmap(send_email, data)