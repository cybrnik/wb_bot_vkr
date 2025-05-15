import requests

API_KEY = ''

def get_auto_campaign_bid_type_status(advert_id, api_key=API_KEY):
    url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'

    data = [advert_id]

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()[0]
        campaign_type = response_json['type']
        cpm = response_json['autoParams']['cpm']
        status = response_json['status']
        return cpm, campaign_type, status
    else:
        return 0, 0, 0


def get_search_campaign_bid_type_status(advert_id, api_key=API_KEY):
    url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'

    data = [advert_id]

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()[0]
        campaign_type = response_json['type']
        cpm = response_json['unitedParams'][0]['searchCPM']
        status = response_json['status']
        return cpm, campaign_type, status
    else:
        return 0, 0, 0


def change_campaign_bid(advert_id, campaign_type, cpm, param=1410, api_key=API_KEY):
    url = 'https://advert-api.wildberries.ru/adv/v0/cpm'

    data = {
        'advertId': advert_id,
        'type': campaign_type,
        'cpm': cpm,
        'param': param
    }
    if campaign_type == 9:
        data['instrument'] = 6

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return 'Ставка успешно изменена'
    elif response.status_code == 422:
        return 'Bid amount not changed: the bid is below the allowable minimum or another constraint was violated.'
    else:
        return f'Failed to change bid: {response.status_code} {response.text}'
