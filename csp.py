# Definizione della classe CSP

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables # lista di variabili che devo assegnare (ad es. ['WA','NT','SA', ecc])
        self.domains = domains # dict di var -> lista di valori possibili (ad es. {'WA':['R','G','B'],ecc})
        # constraints: lista di vincoli, ognuno è (constraint_variables, constraint_function)
        #   - constraint_variables: tupla di nomi di variabili coinvolte
        #   - constraint_function: funzione che riceve i values e restituisce True/False se rispetta o no i vincoli
        self.constraints = constraints

    def consistent(self, variable, value, partial_assignment):
        # partial_assignment: dict parziale delle variabili già assegnate
        # Provo ad aggiungere var=val all'assegnazione parziale
        # -> ad es. val è R (colore rosso), mentre var è SA (regione mappa Australia)
        partial_assignment[variable] = value

        # controllo tutti i vincoli definiti
        for constraint_variables, constraint_function in self.constraints:
            # controllo solo se tutte le variabili del vincolo sono assegnate
            # var: ad es. ('WA','NT') o ('S','E','N','D','M','O','R','Y')
            all_assigned = True
            values = []
            for var in constraint_variables:
                if var not in partial_assignment:
                    all_assigned = False
                    break
                values.append(partial_assignment[var])
            if not all_assigned:
                continue

            # se il vincolo completo è assegnato, chiamo la funzione
            # unpacking di constraint_function, cioè diventa constraint_function(values[0], values[1], ..)
            # constraint_function è il lambda color1, color2: color1 != color2
            # Se passiamo ('R','G') restituisce True, perché i colori sono diversi (vincolo soddisfatto).
            # Se passiamo ('B','B') restituisce False, perché i colori coincidono (vincolo violato).
            if not constraint_function(*values):
                # vincolo violato: rimuovo l'assegnazione parziale e ritorno False
                del partial_assignment[variable]
                return False

        # Se nessun vincolo violato tolgo l'assegnazione parziale e ritorno True
        del partial_assignment[variable]
        return True
