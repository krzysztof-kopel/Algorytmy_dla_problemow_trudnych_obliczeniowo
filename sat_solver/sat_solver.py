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
    new_cnf = cnf
    any_changes = True
    while any_changes:
        any_changes = False
        for clause in new_cnf:
            if len(clause) == 1:
                any_changes = True
                if clause[0] in valuation and valuation[clause[0]] == -1:
                    return None
                valuation[clause[0]] = 1
                valuation[-clause[0]] = -1

                new_cnf = simplify_cnf(new_cnf, valuation)
                if new_cnf is None:
                    return None
    return new_cnf, valuation

def solve_DPLL(cnf: list[list[int]]) -> tuple[dict[int, int] | str, int]:
    recursive_calls = 0

    def solve_internal_dpll(cnf: list[list[int]], valuation: dict[int, int]) -> dict[int, int] | str:
        nonlocal recursive_calls

        if valuation is None:
            valuation = {}

        only_positives = set()
        only_negatives = set()
        all_vars = set()

        next_valuation = valuation.copy()

        for clause in cnf:
            for variable in clause:
                if variable > 0 and variable in only_negatives:
                    only_negatives.remove(variable)
                    continue
                elif variable < 0 and -variable in only_positives:
                    only_positives.remove(-variable)
                    continue

                if variable > 0 and variable not in all_vars:
                    only_positives.add(variable)
                    all_vars.add(variable)
                elif variable < 0 and -variable not in all_vars:
                    only_negatives.add(-variable)
                    all_vars.add(-variable)

        for var in only_positives:
            next_valuation[var] = 1

        for var in only_negatives:
            next_valuation[var] = -1

        cnf_evaluated = simplify_cnf(cnf, next_valuation)

        if cnf_evaluated is None:
            return "UNSAT"
        elif not cnf_evaluated:
            return next_valuation

        res = unit_propagate(cnf_evaluated, next_valuation)
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
solution_dpll = solve_DPLL(cnf)
print(f"DPLL:\nRunning time (s): {time() - start}\nRecursive calls: {solution_dpll[1]}\nSolution: {solution_dpll[0]}")
start = time()
solution_basic = solve_basic(cnf.copy())
print(f"Basic:\nRunning time (s): {time() - start}\nRecursive calls: {solution_basic[1]}\nSolution: {solution_basic[0]}")

if solution_basic[0] != solution_dpll[0]:
    print("WARNING: different solutions")
