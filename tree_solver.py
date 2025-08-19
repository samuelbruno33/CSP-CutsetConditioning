# Algoritmo di backtracking su CSP ad albero

def tree_backtrack(csp_instance, variable_order):
    def backtrack(partial_assignment, i):
        # Se ho assegnato tutte le variabili, ho una soluzione
        if i == len(variable_order):
            return partial_assignment.copy()

        current_var = variable_order[i]
        # provo ogni valore possibile nel dominio
        for possible_value in csp_instance.domains[current_var]:
            # uso is_consistent per verificare current_var=possibe_val rispetto ad assignment
            if csp_instance.is_consistent(current_var, possible_value, partial_assignment):
                # aggiungo current_var = possible_value nel dizionario
                partial_assignment[current_var] = possible_value
                result = backtrack(partial_assignment, i + 1)
                if result is not None:
                    return result
        # nessun valore ha funzionato, backtrack
        if current_var in partial_assignment:
            del partial_assignment[current_var]
        return None

    # inizio con assegnazione vuota e inidice 0
    return backtrack({}, 0)
