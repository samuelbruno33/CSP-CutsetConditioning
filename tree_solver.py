# algoritmo di backtracking su CSP ad albero

def tree_backtrack(csp, order):
    def backtrack(assignment, i):
        if i == len(order):
            return assignment.copy()
        var = order[i]
        for val in csp.domains[var]:
            # uso consistent per verificare var=val rispetto a assignment
            if csp.consistent(var, val, assignment):
                assignment[var] = val
                sol = backtrack(assignment, i+1)
                if sol:
                    return sol
        # backtrack: nessun valore ha funzionato
        if var in assignment:
            del assignment[var]
        return None

    return backtrack({}, 0)
