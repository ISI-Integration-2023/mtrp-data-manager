from __future__ import print_function

import os.path

import csv
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def run():
    creds = None
    if os.path.exists('gsheets/token.json'):
        creds = Credentials.from_authorized_user_file('gsheets/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gsheets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('gsheets/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    with open("gsheets/sheet_details.json") as sheet_details_file:
        sheet_details = json.load(sheet_details_file)
        result = sheet.values().get(spreadsheetId=sheet_details["spreadsheet"],
                                    range=sheet_details["range"]).execute()
        values = result.get('values', [])
        with open("raw_data/printed.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(row for row in values if row[0])

if __name__ == '__main__':
    run()