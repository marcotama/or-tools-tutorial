from ortools.linear_solver import pywraplp

UNITS = [
    '🗡️Swordsmen',
    '🛡️Men-at-arms',
    '🏹Bowmen',
    '❌Crossbowmen',
    '🔫Handcannoneers',
    '🐎Horsemen',
    '♞Knights',
    '🐏Battering rams',
    '🎯Springalds',
    '🪨Mangonels',
]

HEALTH = 0
ATTACK = 1
POWER_DATA = [
    [6, 70],
    [12, 155],
    [5, 70],
    [12, 80],
    [35, 150],
    [9, 125],
    [24, 230],
    [200, 700],
    [30, 200],
    [12*3, 240]
]

FOOD = 0
WOOD = 1
GOLD = 2
COST_DATA = [
    [60, 20, 0],
    [100, 0, 20],
    [30, 50, 0],
    [80, 0, 40],
    [120, 0, 120],
    [100, 20, 0],
    [140, 0, 100],
    [0, 300, 0],
    [0, 250, 250],
    [0, 400, 200]
]

RESOURCES = [183000, 90512, 80150]

RESOURCE_VALUES = [1, 2, 8]


def solve_army(unit_names, cost_data, power_data, resource_limits, resource_values):
    # Create the linear solver using the CBC backend
    solver = pywraplp.Solver('Minimize resource consumption', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # 1. Create the variables we want to optimize
    units = [solver.IntVar(0, solver.infinity(), unit) for unit in unit_names]

    # 2. Add constraints for each resource
    solver.Add(sum((10 * power_data[u][HEALTH] + power_data[u][ATTACK]) * units[u] for u, _ in enumerate(units)) >= 1000001)

    # Old constraints for limited resources
    for r, _ in enumerate(resource_limits):
        solver.Add(sum(cost_data[u][r] * units[u] for u, _ in enumerate(units)) <= resource_limits[r])

    # 3. Minimize the objective function
    target_fn = 0
    for u, _ in enumerate(units):
        for r, _ in enumerate(resource_values):
            target_fn += cost_data[u][r] * resource_values[r] * units[u]
    solver.Minimize(target_fn)

    # Solve problem
    status = solver.Solve()

    # If an optimal solution has been found, print results
    if status == pywraplp.Solver.OPTIMAL:
        print('================= Solution =================')
        print(f'Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations')
        print()

        power = sum((10 * power_data[u][HEALTH] + power_data[u][ATTACK]) * units[u].solution_value() for u, _ in enumerate(units))
        print(f'Optimal value = {solver.Objective().Value()} 🌾🪵🪙 food-equivalent resources')
        print(f'Power = 💪{power}')
        print('Army:')
        for u, _ in enumerate(units):
            print(f' - {units[u].name()} = {units[u].solution_value()}')
        print()

        food = sum((cost_data[u][FOOD]) * units[u].solution_value() for u, _ in enumerate(units))
        wood = sum((cost_data[u][WOOD]) * units[u].solution_value() for u, _ in enumerate(units))
        gold = sum((cost_data[u][GOLD]) * units[u].solution_value() for u, _ in enumerate(units))
        print('Resources:')
        print(f' - 🌾Food = {food}')
        print(f' - 🪵Wood = {wood}')
        print(f' - 🪙Gold = {gold}')
    else:
        print('The solver could not find an optimal solution.')


solve_army(UNITS, COST_DATA, POWER_DATA, RESOURCES, RESOURCE_VALUES)