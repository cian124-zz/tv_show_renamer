import requests
import collections
import file_io


Series = collections.namedtuple('Series', 'actual_name display_name id network year')
known_series = []


def get_token():
    task = {"apikey": "GMF7D81TXRBLW3EX", "userkey": "6MD4CVDHE6HKZC6H", "username": "cian12493r1f"}
    resp = requests.post('https://api.thetvdb.com/login', json=task)

    print('Created task. Token: {}'.format(resp.json()["token"]))
    return resp.json()["token"]


def search_series(bearer_token, series_name):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    payload = {"name": series_name}
    resp = requests.get('https://api.thetvdb.com/search/series', headers=headers, params=payload)

    if resp.status_code == 200 or resp.status_code == 201:
        results = []
        choice = 1
        for data in resp.json()['data']:
            result = Series(data['seriesName'], data['seriesName'].split(" (")[0],
                            data['id'], data['network'], data['firstAired'].split("-")[0])
            results.append(result)
        if len(results) > 1:
            for i, entry in enumerate(results):
                print('{}: {}, which started airing on {} in {}'.format(i+1, entry.display_name,
                                                                        entry.network, entry.year))

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


def get_episode(bearer_token, series_id, season_num, episode_num):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    payload = {"id": series_id, "airedSeason": season_num, "airedEpisode": episode_num}
    resp = requests.get('https://api.thetvdb.com/series/{}/episodes/query'.format(series_id),
                        headers=headers, params=payload)

    print(resp.json())


def get_id_from_name(series_name):
    for series in known_series:
        if series_name.lower() == series.display_name.lower() or series_name.lower() == series.actual_name.lower():
            return series.id
        else:
            return 0


def add_to_known_shows(new_series):
    known_series.append(new_series)


def parse_title():
    pass


def main():
    temp = file_io.load()
    for element in temp:
        known_series.append(element)

    bearer_token = get_token()
    # series_name = input('Series Name: ')
    # search_series(bearer_token, series_name)
    # for series in known_series:
    #     print(series.display_name)
    # get_series(bearer_token, known_series[0].id)
    get_episode(bearer_token, known_series[0].id, 5, 7)
    file_io.save(known_series)


if __name__ == '__main__':
    main()
