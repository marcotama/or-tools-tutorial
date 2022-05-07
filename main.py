from ortools.linear_solver import pywraplp

UNITS = ['🗡️Swordsmen', '🏹Bowmen', '🐎Horsemen']

DATA = [[60, 20, 0, 70],
        [80, 10, 40, 95],
        [140, 0, 100, 230]]

RESOURCES = [1200, 800, 600]


def solve_army(UNITS, DATA, RESOURCES):
  # Create the linear solver using the CBC backend
  solver = pywraplp.Solver('Maximize army power', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  # 1. Create the variables we want to optimize
  units = [solver.IntVar(0, solver.infinity(), unit) for unit in UNITS]

  # 2. Add constraints for each resource
  for r, _ in enumerate(RESOURCES):
    solver.Add(sum(DATA[u][r] * units[u] for u, _ in enumerate(units)) <= RESOURCES[r])

  # 3. Maximize the objective function
  solver.Maximize(sum(DATA[u][-1] * units[u] for u, _ in enumerate(units)))

  # Solve problem
  status = solver.Solve()

  # If an optimal solution has been found, print results
  if status == pywraplp.Solver.OPTIMAL:
    print('================= Solution =================')
    print(f'Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations')
    print()
    print(f'Optimal value = {solver.Objective().Value()} 💪power')
    print('Army:')
    for u, _ in enumerate(units):
      print(f' - {units[u].name()} = {units[u].solution_value()}')
  else:
    print('The solver could not find an optimal solution.')


solve_army(UNITS, DATA, RESOURCES)