import os
import program


def load():
    filepath = get_filepath()
    known_series = []
    if os.path.exists(filepath):
        print("Loading from {}".format(filepath))
        with open(filepath) as fin:
            for entry in fin.readlines():
                series = program.Series(entry.split(',')[0], entry.split(',')[1],
                                        entry.split(',')[2], entry.split(',')[3],
                                        entry.split(',')[4])
                known_series.append(series)
    return known_series


def save(known_series):
    filepath = get_filepath()
    print("Saving to {}".format(filepath))
    with open(filepath, 'w') as fout:
        for entry in known_series:
            fout.write('{},{},{},{},{}\n'.format(entry.actual_name, entry.display_name, entry.id,
                                                 entry.network, entry.year.strip()))
    return


def get_episodes_in_directory(base_dir):
    files = []
    for root, directories, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith(".mp4"):
                print(os.path.join(root, filename))
                files.append([root, filename])
    return files


def rename_file(old_path, new_path, old_name, new_name):
    old_path = os.path.abspath(os.path.join(old_path, old_name))
    new_path = os.path.abspath(os.path.join(new_path, new_name))
    os.rename(old_path, new_path)


def get_filepath():
    filepath = os.path.abspath(os.path.join('.', 'data', 'series' + '.txt'))
    return filepath


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def add_entry(entry, jnal):
    jnal.append(entry)
    return
