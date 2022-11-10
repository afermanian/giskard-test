from collections import defaultdict
from django.conf import settings
import json
import os
import sqlite3


class Graph:
    def __init__(self, list_edges):
        self.graph = defaultdict(list)
        for edge in list_edges:
            a, b = edge[0], edge[1]

            # Creating the graph as adjacency list with weights
            self.graph[a].append((b, edge[2]))
            self.graph[b].append((a, edge[2]))

        self.vertices = list(self.graph.keys())
        self.V = len(self.vertices)  #Number of vertices of the graph

    def get_all_paths(self, departure, arrival, path=[], travel_times=[]):
        # Recursive exploration of the graph to obtain all possible paths
        # between departure and arrival points
        path = path + [departure]
        if departure == arrival:
            return [{'planets': path, 'travel_times': travel_times}]
        paths = []
        for weighted_edge in self.graph[departure]:
            if weighted_edge[0] not in path:
                newpaths = self.get_all_paths(
                    weighted_edge[0], arrival, path=path,
                    travel_times=travel_times+[weighted_edge[1]])
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


def build_universe(database):
    # Read database
    # database_path = settings.BASE_DIR / 'odds/files/universe.db'
    database_path = os.path.dirname(
        os.path.abspath(__file__)) + '/files/universe.db'

    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(database_path)

    cur = con.cursor()

    # Each row of the database is an edge of the graph of the universe, where
    # the weight corresponds to the travel time between the two planets
    # (vertices of the graph)
    weighted_edges = []
    for row in cur.execute('SELECT * FROM routes;'):
        weighted_edges.append(row)

    # Be sure to close the connection
    con.close()

    universe = Graph(weighted_edges)

    return universe


def get_falcon_info():
    # Load information on the millenium falcon
    file_path = settings.BASE_DIR / 'odds/files/millennium-falcon.json'
    f = open(file_path)
    falcon_dict = json.load(f)

    # Create graph of the universe
    universe = build_universe(falcon_dict['routes_db'])

    # Get all possible paths between the departure and arrival points of the
    # millenium falcon
    paths = universe.get_all_paths(falcon_dict['departure'], 
                                   falcon_dict['arrival'])

    return paths, falcon_dict['autonomy']

