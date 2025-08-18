# Implementazione del Cutset Conditioning

from itertools import product
from csp import CSP
from tree_solver import tree_backtrack

def make_unary_from_binary(binary_constraint, residual_variable, fixed_value):
    """
    Trasforma un vincolo binario binary_constraint(x, y) in un
    vincolo unario su y fissando x = fixed_value.
    Restituisce ((y,), lambda y_val: binary_constraint(fixed_value, y_val))
    """
    return (
        (residual_variable,),
        lambda y_val: binary_constraint(fixed_value, y_val)
    )

"""
    Individua un cycle-cutset con euristica greedy:
    1) costruisco grafo di adiacenza per i vincoli binari
    2) finché esiste un ciclo rimuovo la variabile di grado massimo
    """
def find_cycle_cutset(csp_instance):
    # 1) costruisco grafo di adiacenza
    adjacency_dict = {v: set() for v in csp_instance.variables}
    for constraint_variables, _ in csp_instance.constraints:
        if len(constraint_variables) == 2:
            v1, v2 = constraint_variables
            adjacency_dict[v1].add(v2)
            adjacency_dict[v2].add(v1)

    # DFS per rilevare un ciclo partendo da node
    def dfs_detect_cycle(node, visited_set, parent):
        visited_set.add(node)
        for neighbor in adjacency_dict[node]:
            if neighbor == parent:
                continue
            if neighbor in visited_set or dfs_detect_cycle(neighbor, visited_set, node):
                return True
        return False

    def graph_contains_cycle():
        visited_all = set()
        for var in csp_instance.variables:
            if var not in visited_all:
                if dfs_detect_cycle(var, visited_all, None):
                    return True
        return False

    cutset_vars = []
    # 2) rimuovo variabili finché il grafo contiene un ciclo
    while graph_contains_cycle():
        # seleziono la variabile con più vicini
        var_to_remove = max(adjacency_dict, key=lambda v: len(adjacency_dict[v]))
        cutset_vars.append(var_to_remove)
        # la rimuovo completamente dal grafo
        for nbr in adjacency_dict[var_to_remove]:
            adjacency_dict[nbr].remove(var_to_remove)
        adjacency_dict[var_to_remove].clear()

    return cutset_vars

def solve_with_cutset(csp_instance):
    """
    Applica la tecnica del Cutset Conditioning:
    1) Calcola C = find_cycle_cutset(csp_instance)
    2) Per ogni combinazione di valori in C:
       a) Verifica i vincoli che coinvolgono solo C
       b) Costruisce il CSP residuo su V \\ C
       c) Risolve il residuo con tree_backtrack
       d) Se trova una soluzione completa, la restituisce
    """
    print("Variabili CSP:", csp_instance.variables)
    cutset_variables = find_cycle_cutset(csp_instance)
    print("Variabili del cutset:", cutset_variables)

    # 2) ciclo su tutte le assegnazioni possibili a cutset_variables
    for combo in product(*[csp_instance.domains[v] for v in cutset_variables]):
        partial_assignment = dict(zip(cutset_variables, combo))
        print("\nProvo assegnazione parziale: ", partial_assignment)

        # 2a) controllo tutti i vincoli su C
        partial_ok = True
        for constraint_variables, constraint_function in csp_instance.constraints:
            if all(v in partial_assignment for v in constraint_variables):
                valori = [partial_assignment[v] for v in constraint_variables]
                if not constraint_function(*valori):
                    print("Violato vincolo su: ", constraint_variables)
                    partial_ok = False
                    break
        if not partial_ok:
            continue

        # 2b) costruisco il CSP residuo per le altre variabili
        residual_variables = [v for v in csp_instance.variables if v not in cutset_variables]
        residual_constraints = []

        for constraint_variables, constraint_function in csp_instance.constraints:
            # Caso A: vincolo completamente su residual_variables
            if all(v in residual_variables for v in constraint_variables):
                residual_constraints.append((constraint_variables, constraint_function))

            # Caso B: vincolo binario che connette C e R
            elif (len(constraint_variables) == 2
                  and any(v in cutset_variables for v in constraint_variables)
                  and any(v in residual_variables for v in constraint_variables)):
                # identifichiamo quali sono cut_var e res_var
                cut_var = constraint_variables[0] if constraint_variables[0] in cutset_variables else constraint_variables[1]
                res_var = constraint_variables[1] if cut_var == constraint_variables[0] else constraint_variables[0]
                fixed_value = partial_assignment[cut_var]
                residual_constraints.append(
                    make_unary_from_binary(constraint_function, res_var, fixed_value)
                )
            # altri vincoli (n-ari misti) li saltiamo qui

        # 3) risolvo il CSP residuo con backtracking ad albero
        solution_residual = tree_backtrack( CSP(residual_variables, csp_instance.domains, residual_constraints),residual_variables )

        if solution_residual is not None:
            # 4) unisco partial_assignment + solution_residual
            complete_solution = {}
            complete_solution.update(partial_assignment)
            complete_solution.update(solution_residual)
            print("==> Soluzione completa trovata: ", complete_solution)
            return complete_solution
        else:
            print("Fallita la parte residua, passo alla prossima assegnazione.")

    print("---NESSUNA SOLUZIONE TROVATA---")
    return None
