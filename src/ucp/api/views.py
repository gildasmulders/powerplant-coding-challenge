from django.views.decorators.http import require_POST
from django.http.response import JsonResponse
import itertools
import json

FUEL_NAMES = [
    "gas(euro/MWh)",
    "kerosine(euro/MWh)",
    "co2(euro/ton)",
    "wind(%)"
]
POWERPLANT_KEYS = {
    "name",
    "type",
    "efficiency",
    "pmin",
    "pmax"
}


@require_POST
def production_plan(request):
    try:
        data = json.loads(request.body)
        load, fuels, plants = check_payload_validity(data)
        plants = prepare_plants(fuels, plants)
        best_option = compute_optimal_solution(load, plants)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400, safe=False)

    return JsonResponse(best_option, safe=False)


def check_payload_validity(payload):
    """
    Converts all relevant types from decoded JSON, raises ValueError if the received payload is not valid
    :param payload:
    :return: load, fuels, plants -> with converted types
    """
    try:
        load = float(payload["load"])
        fuels = {}
        for fuel_name in FUEL_NAMES:
            fuels[fuel_name] = float(payload["fuels"][fuel_name])
        plants = payload["powerplants"]
        for plant in plants:
            assert set(plant.keys()) == POWERPLANT_KEYS
            plant["efficiency"] = float(plant["efficiency"])
            plant["pmin"] = float(plant["pmin"])
            plant["pmax"] = float(plant["pmax"])

    except Exception:
        raise ValueError("Invalid payload")

    return load, fuels, plants


def prepare_plants(fuels, plants):
    """
    Inserts cost information (adapted based on efficiency) in powerplants definitions
    :param fuels:
    :param plants:
    :return: powerplants, with costs
    """
    for plant in plants:
        efficiency = plant["efficiency"]
        if plant["type"] == "gasfired":
            plant["cost"] = fuels["gas(euro/MWh)"] / efficiency
        elif plant["type"] == "turbojet":
            plant["cost"] = fuels["kerosine(euro/MWh)"] / efficiency
        elif plant["type"] == "windturbine":
            wind_p = round((fuels["wind(%)"]/100) * plant["pmax"], 1)
            plant["pmin"] = wind_p
            plant["pmax"] = wind_p
            plant["cost"] = 0.0
        else:
            raise ValueError(f"Invalid payload - unknown powerplant type: '{plant['type']}'")
    return plants


def compute_optimal_solution(load, plants):
    """
    :param load: demand in energy
    :param plants: available powerplants (list of dicts)
    :return: optimal combination of plants to meet the load
    """
    plants_by_name = {plant["name"]: plant for plant in plants}
    plant_names = sorted(
        list(plants_by_name.keys()),
        key=lambda plant_name: plants_by_name[plant_name]["cost"]
    )
    plants_combinations = []
    for number_of_items in range(1, len(plant_names) + 1):
        plants_combinations += itertools.combinations(plant_names, number_of_items)
    best_cost = None
    best_combination = None
    for plant_combination in plants_combinations:
        plants = [plants_by_name[plant_name] for plant_name in plant_combination]
        min_prod = sum(plant["pmin"] for plant in plants)
        max_prod = sum(plant["pmax"] for plant in plants)

        if min_prod <= load <= max_prod:
            combination_cost, combination_sol = compute_plants_combination(load, plants, min_prod)
            if best_cost is None or combination_cost < best_cost:
                best_cost = combination_cost
                best_combination = combination_sol
    if best_combination is None:
        raise ValueError("No solution found for given load and available plants.")
    return best_combination


def compute_plants_combination(load, plants, min_p):
    """
    :param load: energy demand
    :param plants: selected energy sources
    :param min_p: minimum production of selected energy sources
    :return: tuple with cost and list of dicts containing the powerplant names and productions
    """
    plants_solution = []
    current_prod = min_p
    total_cost = 0
    for plant in plants:
        to_add = round(min(load - current_prod, plant["pmax"] - plant["pmin"]), 1)
        current_prod += to_add
        plant_p = plant["pmin"] + to_add
        plants_solution.append({
            "name": plant["name"],
            "p": plant_p
        })
        total_cost += plant_p * plant["cost"]
    return total_cost, plants_solution
