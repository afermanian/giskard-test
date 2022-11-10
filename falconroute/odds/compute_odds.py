import numpy as np

from .universe import get_falcon_info
from .utils import lists_sum


class CompleteRoute():
    def __init__(self, path: dict, stop_route: list, fuel_schedule: np.ndarray):
        """ The route taken by the millenium falcon, including information of
        the planets visited, where it stops and where it refuels

        :param path: dictionary with list of planets and their corresponding
        travel times
        :param stop_route: array of same length as the planets with the number
        of days waited on each planet
        :param fuel_schedule: array specifying whether it refuels on each
        planet. It it refuels, the number corresponds to the day on which it
        refuels.
        """
        self.planets = path['planets']
        self.travel_times = path['travel_times']
        self.stop_route = stop_route
        self.fuel_schedule = fuel_schedule

    def is_feasible(self, autonomy: int, verbose: bool = False):
        # Checks whether the route is feasible given an autonomy. Loop over the
        # planets visited, update the fuel status and check wheter we run out.
        state_fuel = autonomy
        for i in range(len(self.planets) - 1):
            # Beware that order matters a lot here!
            state_fuel -= self.travel_times[i]
            if state_fuel < 0:
                return False
            if self.fuel_schedule[i + 1] != 0:
                state_fuel = autonomy
            if verbose:
                print(state_fuel)
        return True

    def get_odds(self, autonomy: int, bounty_hunters: list):
        # Compute the probability of not being catch by bounty hunters along
        # this route. If we run out of fuel, the probability is 0.
        if not self.is_feasible(autonomy):
            return 0
        else:
            day = 0
            n_encounters = 0
            for i in range(len(self.planets)):
                if is_bounty_present(self.planets[i], day, bounty_hunters):
                    n_encounters += 1
                for wait_time in range(self.stop_route[i]):
                    day += 1
                    if is_bounty_present(self.planets[i], day, bounty_hunters):
                        n_encounters += 1
                if i < len(self.planets) - 1:
                    day += self.travel_times[i]
            return 100 * (1 - compute_capture_probability(n_encounters))


def generate_fuel_schedules(stop_route: list):
    # Helper function which generates all possibilities of refuel from a stop
    # route.
    fuel_schedules = []
    total_stops = sum(stop_route)
    if total_stops == 0:
        fuel_schedules.append([0] * len(stop_route))
    else:
        stop_route = np.array(stop_route)
        non_zeros = stop_route[stop_route != 0]
        for i in range(total_stops + 1):
            fuel_combinations = lists_sum(len(non_zeros), i)
            for combination in fuel_combinations:
                fuel_schedule = np.array([0] * len(stop_route))
                fuel_schedule[stop_route != 0] = np.array(combination)
                # Remove combinations unfeasible
                if np.all(fuel_schedule <= stop_route):
                    fuel_schedules.append(fuel_schedule)
    return fuel_schedules


def generate_complete_routes(paths: list, countdown: int):
    # Given a countdown and a list of paths between departure and arrival,
    # generate a list of all possible routes (with stops and refuel schedules)
    # which respect this countdown.
    all_routes = []
    for path in paths:
        total_time = sum(path['travel_times'])
        n_planets = len(path['planets'])
        # If travel time longer than the countdown, no route is possible
        if total_time <= countdown:
            for total_waiting_time in range(countdown - total_time + 1):
                stop_routes = lists_sum(n_planets, total_waiting_time)
                for stop_route in stop_routes:
                    all_fuel_schedules = generate_fuel_schedules(stop_route)
                    for fuel_schedule in all_fuel_schedules:
                        all_routes.append(
                            CompleteRoute(path, stop_route, fuel_schedule))
    return all_routes


def compute_capture_probability(n_encounters: int):
    # Returns probability of being captured given a number of encounters
    # between millenium falcon and bounty hunters
    prob = 0
    for i in range(n_encounters):
        prob += 9 ** i / 10 ** (i + 1)
    return prob


def is_bounty_present(planet: str, day: int, bounty_hunters: list):
    # Helper function which checks if a pair of planet and day is present in
    # the list of bounty hunters positions
    for bounty_dict in bounty_hunters:
        if bounty_dict["planet"] == planet and bounty_dict["day"] == day:
            return True
    return False


def compute_final_odds(empire_dict: dict):
    # Compute the odds of saving the galaxy: loop over all possible routes,
    # compute the odds of each route and output the maximal odds.
    paths, autonomy = get_falcon_info()
    countdown = empire_dict['countdown']
    bounty_hunters = empire_dict['bounty_hunters']
    all_routes = generate_complete_routes(paths, countdown)
    odds = 0
    for route in all_routes:
        route_odds = route.get_odds(autonomy, bounty_hunters)
        if route_odds > odds:
            odds = route_odds
    return odds


