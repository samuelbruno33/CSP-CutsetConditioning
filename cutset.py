
from itertools import product
from csp import CSP
from tree_solver import tree_backtrack

def make_unary_from_binary(binary_constraint, residual_var, fixed_value):
    """
    Dato un vincolo binario binary_constraint(x, y),
    restituisce un vincolo unario su residual_var che fissa x = fixed_value:
        y -> binary_constraint(fixed_value, y)
    """
    return (
        (residual_var,),
        lambda y: binary_constraint(fixed_value, y)
    )

def find_cycle_cutset(csp_instance):
    """
    Individua un cycle‐cutset via euristica greedy:
      rimuove iterativamente la variabile di massimo grado
      finché il grafo (dei vincoli binari) non è aciclico.
    """
    # Costruisco grafo di adiacenza per i soli vincoli binari
    adjacency = {v: set() for v in csp_instance.variables}
    for vars_tuple, _ in csp_instance.constraints:
        if len(vars_tuple) == 2:
            v1, v2 = vars_tuple
            adjacency[v1].add(v2)
            adjacency[v2].add(v1)

    def dfs_has_cycle(current, visited, parent):
        visited.add(current)
        for neighbor in adjacency[current]:
            if neighbor == parent:
                continue
            if neighbor in visited or dfs_has_cycle(neighbor, visited, current):
                return True
        return False

    def graph_has_cycle():
        visited = set()
        for var in csp_instance.variables:
            if var not in visited and dfs_has_cycle(var, visited, None):
                return True
        return False

    cutset_vars = []
    while graph_has_cycle():
        # seleziono la variabile col grado massimo
        var_to_remove = max(adjacency, key=lambda v: len(adjacency[v]))
        cutset_vars.append(var_to_remove)
        # la rimuovo dal grafo
        for nbr in adjacency[var_to_remove]:
            adjacency[nbr].remove(var_to_remove)
        adjacency[var_to_remove].clear()

    return cutset_vars

def solve_with_cutset(csp_instance):
    """
    Applica il Cutset Conditioning:
      1) Trova cycle‐cutset C
      2) Per ogni assegnazione a C:
         a) Controlla i vincoli che coinvolgono solo C
         b) Costruisce il CSP residuo su V \\ C (mantiene vincoli interni e trasforma binari C↔R)
         c) Risolve il residuo con tree_backtrack
         d) Se trova soluzione, unisce partial + residual e restituisce
    """
    print("Variables:", csp_instance.variables)
    cutset_vars = find_cycle_cutset(csp_instance)
    print("Cutset:", cutset_vars)

    # 1) Provo ogni combinazione di valori per le variabili del cutset
    for combo in product(*[csp_instance.domains[v] for v in cutset_vars]):
        partial_assignment = dict(zip(cutset_vars, combo))
        print("\nTrying partial assignment:", partial_assignment)

        # 2a) Verifico subito i vincoli che coinvolgono solo variabili in C
        partial_ok = True
        for vars_tuple, constraint_func in csp_instance.constraints:
            if all(v in partial_assignment for v in vars_tuple):
                values = [partial_assignment[v] for v in vars_tuple]
                if not constraint_func(*values):
                    print("Violates constraint on", vars_tuple)
                    partial_ok = False
                    break
        if not partial_ok:
            continue

        # 2b) Costruisco il CSP residuo su R = V \\ C
        residual_vars = [v for v in csp_instance.variables if v not in cutset_vars]
        residual_constraints = []

        for vars_tuple, constraint_func in csp_instance.constraints:
            # Caso A: vincolo completamente interno a R
            if all(v in residual_vars for v in vars_tuple):
                residual_constraints.append((vars_tuple, constraint_func))

            # Caso B: binario che connette C e R → trasformo in unario su R
            elif (len(vars_tuple) == 2
                  and any(v in cutset_vars for v in vars_tuple)
                  and any(v in residual_vars for v in vars_tuple)):

                cut_v = vars_tuple[0] if vars_tuple[0] in cutset_vars else vars_tuple[1]
                res_v = vars_tuple[1] if cut_v == vars_tuple[0] else vars_tuple[0]
                fixed_val = partial_assignment[cut_v]

                unary = make_unary_from_binary(
                    constraint_func,
                    res_v,
                    fixed_val
                )
                residual_constraints.append(unary)

            # Altri vincoli (n-ari misti) vengono saltati qui
            # saranno verificati implicitamente nel backtracking completo

        # 3) Risolvo il CSP residuo con algoritmo ad albero
        solution_residual = tree_backtrack(
            CSP(residual_vars, csp_instance.domains, residual_constraints),
            residual_vars
        )

        if solution_residual is not None:
            # 4) Unisco partial + residual → soluzione completa
            complete_solution = {}
            complete_solution.update(partial_assignment)
            complete_solution.update(solution_residual)
            print("==> Found complete solution:", complete_solution)
            return complete_solution
        else:
            print("Residual solve failed, continuing...")

    print("No solution found")
    return None
