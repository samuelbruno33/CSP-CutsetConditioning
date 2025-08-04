# Algoritmo di backtracking su CSP ad albero

def tree_backtrack(csp_instance, variable_order):
    def backtrack(partial_assignment, i):
        # Se ho assegnato tutte le variabili, ho una soluzione
        if i == len(variable_order):
            return partial_assignment.copy()

        current_var = variable_order[i]
        # provo ogni possibile valore nel dominio
        for candidate_value in csp_instance.domains[current_var]:
            # uso consistent per verificare var=val rispetto a assignment
            if csp_instance.consistent(current_var, candidate_value, partial_assignment):
                # aggiungo current_var=candidate_value
                partial_assignment[current_var] = candidate_value
                result = backtrack(partial_assignment, i + 1)
                if result is not None:
                    return result
        # nessun valore ha funzionato, backtrack
        if current_var in partial_assignment:
            del partial_assignment[current_var]
        return None

    # inizio con assegnazione vuota e inidice 0
    return backtrack({}, 0)
