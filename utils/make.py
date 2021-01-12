from secrets import IMGFLIP_URL, IMGFLIP_USERNAME, IMGFLIP_PASSWORD
import requests

def make(memeid, text):

    data = {
        'username':IMGFLIP_USERNAME,
        'password':IMGFLIP_PASSWORD,
        'template_id': memeid,
    }

    i = 0

    for eachtext in text:
        eachtext = eachtext.strip()
        data[f'boxes[{i}][text]'] = eachtext
        i += 1

    response = requests.request('POST', IMGFLIP_URL, params=data).json()

    return response['data']['url']
