# Implementazione del Cutset Conditioning

from itertools import product
from csp import CSP
from tree_solver import tree_backtrack

def find_cycle_cutset(csp_instance):
    # costruisco grafo di adiacenza per i vincoli binari
    adj_graph = {v: set() for v in csp_instance.variables}
    # uso _ come valore usa e getta anziche scrivere constraint_function perchè tanto non la uso
    for constraint_variables, _ in csp_instance.constraints:
        if len(constraint_variables) == 2:
            v1, v2 = constraint_variables
            adj_graph[v1].add(v2)
            adj_graph[v2].add(v1)

    # DFS per rilevare un ciclo partendo da node
    def dfs_visit(node, visited, parent):
        # lo segno come visitato
        visited.add(node)
        for neighbor in adj_graph[node]:
            # ignoro l'arco se è il padre e passo alla prossima iterazione
            if neighbor == parent:
                continue
            # prima controllo se il vicino è già stato visitato
            if neighbor in visited:
                return True
            # se non era stato visitato, esploro ricorsivamente
            if dfs_visit(neighbor, visited, node):
                return True # c'è un ciclo
        return False # non c'è un ciclo

    def graph_contains_cycle():
        visited_nodes = set()

        # controllo ogni variabile, perché il grafo può non essere connesso
        for var in csp_instance.variables:
            if var not in visited_nodes:
                # lancio una DFS da questa variabile
                if dfs_visit(var, visited_nodes, None):
                    # se dfs_visit trova un ciclo, ritorno subito True
                    return True

        # nessun ciclo trovato
        return False

    cutset_vars = []
    # rimuovo le variabili finché il grafo contiene un ciclo
    while graph_contains_cycle():
        # seleziono la variabile con più vicini (ovvero con grado massimo)
        def degree(v):
            return len(adj_graph[v])
        # la funzione max itera dentro il grafo ed estrae, in base al grado della variabile, quella con grado maggiore
        var_to_remove = max(adj_graph, key=degree)
        cutset_vars.append(var_to_remove)
        # cancello dai suoi vicini la variabile di grado max completamente dal grafo
        for i in adj_graph[var_to_remove]:
            adj_graph[i].remove(var_to_remove)
        adj_graph[var_to_remove].clear()

    return cutset_vars


def make_unary_from_binary(binary_constraint, residual_variable_name, fixed_cutset_value):
    # creo un vincolo unario dal vincolo binario, fissando il valore della variabile del cutset
    def unary_constraint(residual_variable_value):
        return binary_constraint(fixed_cutset_value, residual_variable_value)
    return (residual_variable_name,), unary_constraint


def solve_with_cutset(csp_instance):
    print("Variabili CSP:", csp_instance.variables)
    cutset_variables = find_cycle_cutset(csp_instance)
    print("Variabili del cutset:", cutset_variables)

    # prendo i domini del cutset e li metto in una lista
    cutset_domains_list = []
    for var in cutset_variables:
        cutset_domains_list.append(csp_instance.domains[var])

    # ciclo su tutte le combinazioni di valori del cutset, per la mappa dell'australia
    # il primo tentativo sarebbe {'SA': 'R'} che si trova dentro partial_cutset_assignment
    # se non dovesse andare bene partirebbe poi con {'SA': 'G'} e cosi via
    for cutset_values_combo in product(*cutset_domains_list):
        partial_cutset_assignment = {}
        for i in range(len(cutset_variables)):
            partial_cutset_assignment[cutset_variables[i]] = cutset_values_combo[i]

        print("\nProvo assegnazione parziale:", partial_cutset_assignment)

        # controllo vincoli interni al cutset
        # per le mappe possono essere, se ad es il cutset è ['SA','NT'] ed è presente il vincolo ('NT','SA'), allroa questo non va bene
        # quello è l'unico caso per le mappe perchè le regioni non presentano di per sè dei vincoli unari
        # per le critpoaritmetiche invece vengono controllati anche i vincoli unari, quindi ad esempio che le prime lettere di ogni parola sia diverso da 0
        # oppure i vincoli n-ari 
        partial_assignment_satisfies_constraints = True
        for constraint_variables, constraint_function in csp_instance.constraints:
            # controllo solo se il vincolo è interamente dentro il cutset
            all_variables_in_cutset = True
            for var in constraint_variables:
                if var not in partial_cutset_assignment:
                    all_variables_in_cutset = False
                    break

            if all_variables_in_cutset:
                assigned_values_for_constraint = []
                for var in constraint_variables:
                    assigned_values_for_constraint.append(partial_cutset_assignment[var])

                if not constraint_function(*assigned_values_for_constraint):
                    print("Violato vincolo su:", constraint_variables)
                    partial_assignment_satisfies_constraints = False
                    break

        if not partial_assignment_satisfies_constraints:
            continue

        # costruisco variabili residue ovvero variabili non nel cutset
        residual_variables = []
        for var in csp_instance.variables:
            if var not in cutset_variables:
                residual_variables.append(var)

        residual_constraints = []

        # adesso trasformo i vincoli per il residuo
        for constraint_variables, constraint_function in csp_instance.constraints:
            # Caso 1: tutti nel residuo
            all_variables_in_residual = True
            for var in constraint_variables:
                if var not in residual_variables:
                    all_variables_in_residual = False
                    break

            if all_variables_in_residual:
                residual_constraints.append((constraint_variables, constraint_function))
                continue

            # Caso 2: vincolo binario misto (cutset + residuo)
            if len(constraint_variables) == 2:
                first_var, second_var = constraint_variables[0], constraint_variables[1]

                if (first_var in cutset_variables and second_var in residual_variables) or \
                   (second_var in cutset_variables and first_var in residual_variables):

                    if first_var in cutset_variables:
                        cutset_variable_name, residual_variable_name = first_var, second_var
                    else:
                        cutset_variable_name, residual_variable_name = second_var, first_var

                    fixed_value_for_cutset_variable = partial_cutset_assignment[cutset_variable_name]
                    unary_constraint_for_residual = make_unary_from_binary(
                        constraint_function,
                        residual_variable_name,
                        fixed_value_for_cutset_variable
                    )
                    residual_constraints.append(unary_constraint_for_residual)

        # creo il CSP residuo e lo risolvo
        residual_csp_instance = CSP(residual_variables, csp_instance.domains, residual_constraints)
        solution_for_residual_csp = tree_backtrack(residual_csp_instance, residual_variables)

        if solution_for_residual_csp is not None:
            complete_solution = {}
            complete_solution.update(partial_cutset_assignment)
            complete_solution.update(solution_for_residual_csp)
            print("==> Soluzione completa trovata:", complete_solution)
            return complete_solution
        else:
            print("Fallita la parte residua, passo alla prossima assegnazione.")

    print("---NESSUNA SOLUZIONE TROVATA---")
    return None


