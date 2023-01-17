import json

import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from email.policy import SMTPUTF8

import popplerqt5

email_offline_txt  = open("admit_mailer/message_templates/email_offline.txt").read()
email_offline_html = open("admit_mailer/message_templates/email_offline.html").read()

email_online_txt   = open("admit_mailer/message_templates/email_online.txt").read()
email_online_html  = open("admit_mailer/message_templates/email_online.html").read()

def send_email(roll_no : str):
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
    msg['From'] = Address("MTRP 2023 Core Team", "integration", "isical.ac.in")
    msg['To'] = Address(data['name'], *(data['email'].split('@')))
    if roll_no[1] == 'O':
        msg.set_content(email_online_txt.format_map(data))
        msg.add_alternative(email_online_html.format_map(data), subtype='html')
    else:
        msg.set_content(email_offline_txt.format_map(data))
        msg.add_alternative(email_offline_html.format_map(data), subtype='html')

    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=f'MTRP 2023 Admit Card - {roll_no}.pdf')

    with open(f"admit_mailer/emails/{roll_no}.eml", "wb") as fp:
        fp.write(msg.as_bytes(policy=SMTPUTF8))
