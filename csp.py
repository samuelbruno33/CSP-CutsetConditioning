# definizione della classe CSP

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # lista dei nomi delle variabili
        self.domains = domains      # dict var -> lista di valori
        self.constraints = constraints
        # constraints: lista di (vars_tuple, func),
        #   dove vars_tuple è una tupla di 1,2 o più variabili,
        #   func(*vals) restituisce True se il vincolo è soddisfatto

    def consistent(self, var, value, assignment):
        # verifica se assegnare var=value è compatibile con
        # i vincoli di ogni grado, considerando assignment parziale.
        local = assignment.copy()
        local[var] = value
        for vars_tuple, func in self.constraints:
            if all(v in local for v in vars_tuple):
                vals = [ local[v] for v in vars_tuple ]
                if not func(*vals):
                    return False
        return True

