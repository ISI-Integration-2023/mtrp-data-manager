import os
import csv

from multiprocessing import Pool

from email import message_from_binary_file
from email.headerregistry import Address
import smtplib

msg = message_from_binary_file(open(f"brochure_mailer/msg_to_schools.eml", "rb"))

def send_email(name : str, email_id : str):
    name.replace(',', ' ').replace('\n', ' ')
    with smtplib.SMTP("mail.isical.ac.in", 500) as smtp:
        msg['To'] = f"{name} <{email_id}>"
        smtp.send_message(msg)
        print(f"BROCHURE MAILER: Sent brochure to {name} <{email_id}>.")
        with open("brochure_mailer/sent.txt", "a") as sent:
            sent.write(email_id + "\n")

def run(N=50):
    sent = [email.strip() for email in open("brochure_mailer/sent.txt").readlines()]
    with open("brochure_mailer/schools.csv") as f:
        reader = csv.DictReader(f)
        data = [(row["name"], row["email"]) for row in reader if row["name"] and row["email"] and row["email"] not in sent][:N]
        print(f"BROCHURE MAILER: Sending for the following adresses... ({len(data)})")
        print("-"*140)
        for name, email in data:
            name.replace(',', ' ').replace('\n', ' ')
            print(f"{name:30} <{email}>")
        print("-"*140)
        inp = input("Proceed? (y/N): ").lower()
        print("-"*140)
        if len(inp) >= 1 and inp[0] == 'y':
            with Pool(10) as pool:
                pool.starmap(send_email, data)