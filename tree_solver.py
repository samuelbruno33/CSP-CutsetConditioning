# algoritmo di backtracking su CSP ad albero

from csp import CSP

def tree_backtrack(csp: CSP, order: list):
    def backtrack(assignment, idx):
        if idx == len(order): # order è una lista di variabili in un ordine tali che risolva facilmente l’albero.
            return assignment
        var = order[idx]
        for val in csp.domains[var]:
            if csp.consistent(var, val, assignment):
                assignment[var] = val
                result = backtrack(assignment, idx + 1)
                if result is not None:
                    return result
                del assignment[var]
        return None
    return backtrack({}, 0)