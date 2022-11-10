import json
import os
import sys

from falconroute.odds.compute_odds import generate_complete_routes
from falconroute.odds.universe import build_universe


def get_falcon_info(millenium_path):
    file_path = os.path.dirname(
        os.path.abspath(__file__)) + '/' + millenium_path
    f = open(file_path)
    falcon_dict = json.load(f)

    universe = build_universe(falcon_dict['routes_db'])

    paths = universe.get_all_paths(falcon_dict['departure'],
                                   falcon_dict['arrival'])

    return paths, falcon_dict['autonomy']


def compute_final_odds(millenium_path, empire_path):
    # Construct graph of universe and get falcon info
    paths, autonomy = get_falcon_info(millenium_path)

    # Load empire info
    file_path = os.path.dirname(
        os.path.abspath(__file__)) + '/' + empire_path
    f = open(file_path)
    empire_dict = json.load(f)

    countdown = empire_dict['countdown']
    bounty_hunters = empire_dict['bounty_hunters']
    all_routes = generate_complete_routes(paths, countdown)
    odds = 0
    for route in all_routes:
        route_odds = route.get_odds(autonomy, bounty_hunters)
        if route_odds > odds:
            odds = route_odds
    return odds


if __name__ == "__main__":
    millenium_path = sys.argv[1]
    empire_path = sys.argv[2]
    print(millenium_path, empire_path)
    print(compute_final_odds(millenium_path, empire_path))