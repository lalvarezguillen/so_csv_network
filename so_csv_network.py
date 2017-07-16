from collections import OrderedDict
import pandas as pd


def open_network_tsv(filepath):
    """
    Read the tsv file, returning every line split by tabs
    """
    with open(filepath) as network_file:
        for line in network_file.readlines():
            line_columns = line.strip().split('\t')
            yield line_columns

def get_connections(potential_conns):
    """
    Get the connections of a particular line, grouped
    in interactor:score pairs
    """
    for idx, val in enumerate(potential_conns):
        if not idx % 2:
            if len(potential_conns) >= idx + 2:
                yield val, potential_conns[idx+1]


def create_connections_df(filepath):
    """
    Build the desired dataframe
    """
    connections = OrderedDict({
        'uniq_id': [],
        'alias': [],
        'interactor': [],
        'score': []
    })
    for line in open_network_tsv(filepath):
        uniq_id, alias, *potential_conns = line
        for connection in get_connections(potential_conns):
            connections['uniq_id'].append(uniq_id)
            connections['alias'].append(alias)
            connections['interactor'].append(connection[0])
            connections['score'].append(connection[1])
    return pd.DataFrame(connections)
