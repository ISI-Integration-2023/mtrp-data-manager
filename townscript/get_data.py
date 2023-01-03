import requests
import datetime

data_base = {
    "checkInStatus": '"All"',
    "end": f"{datetime.date.today().strftime('%Y-%m-%d')}T23:59:59.000+0530",
    "fileType": "csv",
    "start": "2011-01-04T00:00:00.000+0530",
    "status": "ALL"
}

data_offline = {
    "eventId": 310377,
    "eventName": '"Mathematics+Talent+Reward+Programme+(MTRP),+2023+(Offline+Exam)"',
    "ticketIds": '[470565,470568,470607]'
}

data_online = {
    "eventId": 310585,
    "eventName": '"Mathematics+Talent+Reward+Programme+(MTRP),+2023+(Online+Mode)"',
    "ticketIds": '[470900,470901,470902]'
}

data_primer = {
    "eventId": 310590,
    "eventName": '"Mathematics+Talent+Reward+Programme+(MTRP),+2023+Problem+Primer+(Divide+&+Conquer)"',
    "ticketIds": '[470911,470913]'
}

url = f'https://www.townscript.com/api/csvdata/registration-data'

def run():
    with open("townscript/web_token.txt") as token_file:
        token = token_file.read()

        headers = {
            "accept": "application/json, text/plain, */*",
            "Authorization": token,
        }
        with open("raw_data/offline.csv", "w") as f:
            response_offline = requests.get(url, { **data_base, **data_offline }, headers=headers)
            f.write(response_offline.text)
        with open("raw_data/online.csv", "w") as f:
            response_online = requests.get(url, { **data_base, **data_online }, headers=headers)
            f.write(response_online.text)
        with open("raw_data/primer.csv", "w") as f:
            response_primer = requests.get(url, { **data_base, **data_primer }, headers=headers)
            f.write(response_primer.text)

if __name__ == '__main__':
    run()    