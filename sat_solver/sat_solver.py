import dimacs
from time import time

def simplify_clause(clause: list[int], valuation: dict[int, int]) -> list | None:
    new_clause = []
    for variable in clause:
        if variable in valuation and valuation[variable] == 1:
            return None
        elif variable not in valuation:
            new_clause.append(variable)
    return new_clause

def simplify_cnf(cnf: list[list[int]], valuation: dict[int, int]) -> list[list[int]] | None:
    new_cnf = []
    for clause in cnf:
        if (clause_simplified := simplify_clause(clause, valuation)) == []:
            return None
        elif clause_simplified is not None:
            new_cnf.append(clause_simplified)
    return new_cnf

def solve_basic(cnf: list[list[int]]) -> tuple[dict[int, int] | str, int]:
    recursive_calls = 0

    def solve_internal(cnf: list[list[int]], valuation: dict[int, int]) -> dict[int, int] | str:
        nonlocal recursive_calls

        if valuation is None:
            valuation = {}

        cnf_evaluated = simplify_cnf(cnf, valuation)

        if cnf_evaluated is None:
            return "UNSAT"
        elif not cnf_evaluated:
            return valuation

        next_variable = cnf_evaluated[0][0]

        valuation_false = valuation.copy()
        valuation_false[next_variable] = -1
        valuation_false[-next_variable] = 1

        valuation_true = valuation.copy()
        valuation_true[next_variable] = 1
        valuation_true[-next_variable] = -1

        recursive_calls += 1
        if (new_valuation := solve_internal(cnf_evaluated, valuation_false)) != "UNSAT":
            return new_valuation

        recursive_calls += 1
        if (new_valuation := solve_internal(cnf_evaluated, valuation_true)) != "UNSAT":
            return new_valuation

        return "UNSAT"

    solution = solve_internal(cnf, {})
    if type(solution) == dict:
        solution = {k: v for k, v in solution.items() if k > 0}
        solution = {k: v for k, v in sorted(solution.items(), key=lambda item: abs(item[0]))}

    return solution, recursive_calls

def unit_propagate(cnf: list[list[int]], valuation: dict[int, int]) -> tuple[list[list[int]], dict[int, int]] | None:
    new_cnf = cnf.copy()
    any_changes = True
    while any_changes:
        any_changes = False
        for clause in cnf:
            if len(clause) == 1:
                any_changes = True
                if clause[0] in valuation and valuation[clause[0]] == -1:
                    return None
                valuation[clause[0]] = 1
                valuation[-clause[0]] = -1

                new_cnf = simplify_cnf(new_cnf, valuation)
                if new_cnf is None:
                    return None
        cnf = new_cnf
    return new_cnf, valuation

def solve_DPLL(cnf: list[list[int]]) -> tuple[dict[int, int] | str, int]:
    recursive_calls = 0

    def solve_internal_dpll(cnf: list[list[int]], valuation: dict[int, int]) -> dict[int, int] | str:
        nonlocal recursive_calls

        if valuation is None:
            valuation = {}

        cnf_evaluated = simplify_cnf(cnf, valuation)

        if cnf_evaluated is None:
            return "UNSAT"
        elif not cnf_evaluated:
            return valuation

        res = unit_propagate(cnf_evaluated, valuation)
        if res is None:
            return "UNSAT"
        cnf_evaluated, valuation = res
        if not cnf_evaluated:
            return valuation

        next_variable = cnf_evaluated[0][0]

        valuation_false = valuation.copy()
        valuation_false[next_variable] = -1
        valuation_false[-next_variable] = 1

        valuation_true = valuation.copy()
        valuation_true[next_variable] = 1
        valuation_true[-next_variable] = -1

        recursive_calls += 1
        if (new_valuation := solve_internal_dpll(cnf_evaluated, valuation_false)) != "UNSAT":
            return new_valuation

        recursive_calls += 1
        if (new_valuation := solve_internal_dpll(cnf_evaluated, valuation_true)) != "UNSAT":
            return new_valuation

        return "UNSAT"


    solution = solve_internal_dpll(cnf, {})
    if type(solution) == dict:
        solution = {k: v for k, v in solution.items() if k > 0}
        solution = {k: v for k, v in sorted(solution.items(), key=lambda item: abs(item[0]))}

    return solution, recursive_calls

file_name = input("Enter file name: ")
cnf = dimacs.loadCNF(f"example_sat\\{file_name}")[1]

start = time()
solution_basic = solve_basic(cnf.copy())
print(f"Basic:\nRunning time (s): {time() - start}\nRecursive calls: {solution_basic[1]}\nSolution: {solution_basic[0]}")
start = time()
solution_dpll = solve_DPLL(cnf)
print(f"DPLL:\nRunning time (s): {time() - start}\nRecursive calls: {solution_dpll[1]}\nSolution: {solution_dpll[0]}")

if solution_basic[0] != solution_dpll[0]:
    print("WARNING: different solutions")
