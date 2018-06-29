import collections
import file_io
import rest_calls


Series = collections.namedtuple('Series', 'actual_name display_name id network year')
known_series = []


def get_token():
    resp_json = rest_calls.post_login()
    if resp_json:
        return resp_json["token"]


def search_series(bearer_token, series_name):
    resp_json = rest_calls.get_search_series(bearer_token, series_name)
    if resp_json:
        results = []
        choice = 1
        for data in resp_json['data']:
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
    resp_json = rest_calls.get_series_id(bearer_token, series_id)
    if resp_json:
        new_series = Series(resp_json['data']['seriesName'], resp_json['data']['seriesName'].split(" (")[0],
                            resp_json['data']['id'], resp_json['data']['network'],
                            resp_json['data']['firstAired'].split("-")[0])
        add_to_known_shows(new_series)


def get_episode(bearer_token, series_id, season_num, episode_num):
    resp_json = rest_calls.get_series_id_episodes_query(bearer_token, series_id, season_num, episode_num)

    if resp_json:
        print(resp_json)


def get_id_from_name(series_name):
    for series in known_series:
        if series_name.lower() == series.display_name.lower() or series_name.lower() == series.actual_name.lower():
            return series.id
        else:
            return 0


def load_favourites(bearer_token):
    resp_json = rest_calls.get_user_favorites(bearer_token)

    for series_id in resp_json["data"]["favorites"]:
        if not [item for item in known_series if series_id in item]:
            get_series(bearer_token, series_id)


def add_to_known_shows(new_series):
    known_series.append(new_series)


def parse_title():
    pass


def main():
    temp = file_io.load()
    for element in temp:
        known_series.append(element)

    bearer_token = get_token()
    load_favourites(bearer_token)
    # series_name = input('Series Name: ')
    # search_series(bearer_token, series_name)
    # for series in known_series:
    #     print(series.display_name)
    # get_series(bearer_token, known_series[0].id)
    # get_episode(bearer_token, known_series[0].id, 5, 7)
    file_io.save(known_series)


if __name__ == '__main__':
    main()
