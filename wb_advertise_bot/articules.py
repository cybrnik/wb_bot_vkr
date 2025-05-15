import requests

def get_nomenclature_list(api_key, locale='ru'):

    url = 'https://content-api.wildberries.ru/content/v2/get/cards/list'

    data = {
        "settings": {
            "cursor": {
                "limit": 100
            },
            "filter": {
                "withPhoto": -1
            }
        }
    }

    headers = {
        'Authorization': f'{api_key}',
        'Content-Type': 'application/json',
        'locale': locale
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return f'Failed to retrieve data: {response.status_code} {response.text}'

api_key = ''
nomenclatures = get_nomenclature_list(api_key)
print(nomenclatures)
