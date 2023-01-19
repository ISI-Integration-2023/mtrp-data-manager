import json
import os
import glob
import subprocess

from multiprocessing import Pool

from email.message import EmailMessage
from email.headerregistry import Address
from email.policy import SMTPUTF8

import popplerqt5

email_offline_txt = open(
    "admit_mailer/message_templates/email_offline.txt").read()
email_offline_html = open(
    "admit_mailer/message_templates/email_offline.html").read()

email_online_txt = open(
    "admit_mailer/message_templates/email_online.txt").read()
email_online_html = open(
    "admit_mailer/message_templates/email_online.html").read()


def make_email(roll_no: str):
    pdf_data = None
    try:
        with open(f"admit_card/generated/{roll_no}.pdf", "rb") as f:
            pdf_data = f.read()
    except FileNotFoundError:
        return None

    doc = popplerqt5.Poppler.Document.loadFromData(pdf_data)
    data = json.loads(doc.info("admit_data"))
    data['exam_venue'] = data['exam_venue'].replace('\n', ', ')

    msg = EmailMessage()
    msg['Subject'] = f"MTRP 2023 Admit Card - {roll_no}"
    msg['From'] = Address("Integration 2023 Automailer",
                          "integration", "isical.ac.in")
    msg['Reply-To'] = Address("MTRP 2023 Core Team",
                              "mtrp.isi.kol", "gmail.com")
    msg['To'] = Address(data['name'], *(data['email'].lower().split('@')[:2]))
    msg['CC'] = Address("MTRP 2023 Core Team", "mtrp.isi.kol", "gmail.com")

    if roll_no[1] == 'O':
        msg.set_content(email_online_txt.format_map(data))
        msg.add_alternative(email_online_html.format_map(data), subtype='html')
    else:
        msg.set_content(email_offline_txt.format_map(data))
        msg.add_alternative(
            email_offline_html.format_map(data), subtype='html')

    result = subprocess.run([
        "gs", "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH", "-sOutputFile=%stdout", "-"
    ], capture_output=True, input=pdf_data)
    pdf_data_compressed = result.stdout

    msg.add_attachment(pdf_data_compressed, maintype='application', subtype='pdf',
                       filename=f'MTRP 2023 Admit Card - {roll_no}.pdf')

    with open(f"admit_mailer/emails/{roll_no}.eml", "wb") as fp:
        fp.write(msg.as_bytes(policy=SMTPUTF8))

def run():
    print(f"ADMIT CARD: Deleting old draft emails...")
    files = glob.glob("admit_mailer/emails/*.eml")
    print(f"ADMIT CARD: Deleted old draft emails!")
    for f in files:
        os.remove(f)
    sent = [roll_no.strip() for roll_no in open("admit_mailer/sent.txt").readlines()]
    sent = [roll_no.strip() for roll_no in open("admit_mailer/revoked.txt").readlines()]
    roll_nos = (filename.replace('.pdf', '') for filename in os.listdir("admit_card/generated") if 'pdf' in filename)
    roll_nos = [roll_no for roll_no in roll_nos if (roll_no not in sent) and (roll_no not in revoked)]
    with Pool(10) as pool:
        pool.map(make_email, roll_nos)