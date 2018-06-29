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
            fout.write('{},{},{},{},{}'.format(entry.actual_name, entry.display_name, entry.id,
                                                 entry.network, entry.year))
    return


def get_filepath():
    filepath = os.path.abspath(os.path.join('.', 'data', 'series' + '.txt'))
    return filepath


def add_entry(entry, jnal):
    jnal.append(entry)
    return
