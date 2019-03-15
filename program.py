import collections
import re
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


def get_episode_name(bearer_token, series_id, season_num, episode_num):
    resp_json = rest_calls.get_series_id_episodes_query(bearer_token, series_id, season_num, episode_num)

    if resp_json:
        episode_name = resp_json['data'][0]['episodeName']
        return episode_name


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


def parse_title(orig_title):
    series_name = ''
    season_num = 0
    episode_num = 0
    split_title = re.split('[. ]', orig_title.lower())
    filetype = split_title[-1]
    for word in split_title:
        print(word)
        word_list = list(word)
        if word != '' and not check_if_number(word):
            if episode_num != 0:
                break
            elif word_list[0] == 's':
                if check_if_number(word_list[1]):
                    season_num = int(word_list[1] + word_list[2])
                    if len(word_list) > 3:
                        episode_num = int(word_list[4] + word_list[5])
                else:
                    series_name = series_name + ' ' + word
            elif season_num != 0:
                if check_if_number(word_list[1]):
                    episode_num = int(word_list[1] + word_list[2])
            else:
                series_name = series_name + ' ' + word

    return series_name.strip(), season_num, episode_num, filetype


def check_if_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_if_series_exists(series_name):
    regex = re.compile("[.']")
    for series in known_series:
        actual_name = regex.sub('', series.actual_name)
        display_name = regex.sub('', series.display_name)
        if series_name == actual_name.lower():
            return series.id, series.display_name
        elif series_name == display_name.lower():
            return series.id, series.display_name


def rename_episode(bearer_token):
    files = file_io.get_episodes_in_directory("D:\\Video\\TV Shows\\Watched")
    for episode_info in files:
        series_name, season_num, episode_num, filetype = parse_title(episode_info[1])
        if season_num != 0:
            print('Series Name: {}\nSeries Number: {}\nEpisode Number: {}'.format(series_name, season_num, episode_num))
            series_id, series_name = check_if_series_exists(series_name)

            episode_name = get_episode_name(bearer_token, series_id, season_num, episode_num)
            episode_name = re.sub('[!@#$:*?]', '', episode_name)

            filename = "{} S{}E{} {}".format(series_name, str(season_num).zfill(2), str(episode_num).zfill(2), episode_name)
            filename = '{}.{}'.format(filename, filetype)
            new_directory = "D:\\Video\\TV Shows\\Done\\Watched\\{}\\Season {}".format(series_name, season_num)
            file_io.create_directory(new_directory)
            file_io.rename_file(episode_info[0], new_directory, episode_info[1], filename)
            print("Copied {}".format(filename))


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
    rename_episode(bearer_token)
    file_io.save(known_series)


if __name__ == '__main__':
    main()
