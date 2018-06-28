import requests


def get_token():
    task = {"apikey": "GMF7D81TXRBLW3EX", "userkey": "6MD4CVDHE6HKZC6H", "username": "cian12493r1f"}
    resp = requests.post('https://api.thetvdb.com/login', json=task)

    print('Created task. Token: {}'.format(resp.json()["token"]))
    return resp.json()["token"]


def search_series(bearer_token):
    series_name = input('Series Name: ')
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    payload = {"name": series_name}
    resp = requests.get('https://api.thetvdb.com/search/series', headers=headers, params=payload)

    print(resp.status_code)
    # print(resp.json()["data"])
    for data in resp.json()["data"]:
        print('Name: {}'.format(data["seriesName"]))


def main():
    bearer_token = get_token()
    search_series(bearer_token)


if __name__ == '__main__':
    main()
