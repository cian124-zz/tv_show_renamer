import requests
import collections


Series = collections.namedtuple('Series', 'actual_name display_name id overview network year')
known_series = []


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

    if resp.status_code == 200 or resp.status_code == 201:
        results = []
        choice = 1
        for data in resp.json()['data']:
            result = Series(data['seriesName'], data['seriesName'].split(" (")[0],
                            data['id'], data['overview'], data['network'], data['firstAired'].split("-")[0])
            results.append(result)
        if len(results) > 1:
            for i, entry in enumerate(results):
                print('{}: {}, which started airing on {} in {}'.format(i+1, entry.display_name, entry.network, entry.year))

            choice = input('Which of these series did you mean? (Choose number) ')
            choice = int(choice)

        confirmation = input('Is {}, which started airing on {} in {}, '
                             'the correct show? (y/n) '.format(results[choice - 1].display_name,
                                                              results[choice - 1].network,
                                                              results[choice - 1].year)).lower()
        if confirmation == 'y':
            add_to_known_shows(results[choice-1])
    else:
        print('No results found')


def get_series(bearer_token, series_id):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    resp = requests.get('https://api.thetvdb.com/series/{}'.format(series_id), headers=headers)

    print(resp.json())


def get_id_from_name(series_name):
    for series in known_series:
        if series_name.lower() == series.display_name.lower() or series_name.lower() == series.actual_name.lower():
            return series.id
        else:
            return 0


def add_to_known_shows(new_series):
    known_series.append(new_series)


def main():
    bearer_token = get_token()
    search_series(bearer_token)
    get_series(bearer_token, known_series[0].id)


if __name__ == '__main__':
    main()
