# Definizione della classe CSP

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables # lista di variabili che devo assegnare (ad es. ['WA','NT','SA', ecc])
        self.domains = domains # dict di var -> lista di valori possibili (ad es. {'WA':['R','G','B'], ecc})
        # constraints: lista di vincoli, di tipo (constraint_variables, constraint_function)
        #   - constraint_variables: contiene i nomi delle variabili coinvolte
        #   - constraint_function: funzione che riceve i values e restituisce True/False se rispetta o no i vincoli
        self.constraints = constraints

    def is_consistent(self, color, region, partial_assignment):
        # partial_assignment: dizionario delle variabili già assegnate
        # Provo ad aggiungere un colore all'assegnazione parziale con una regione
        # infatti color è R (rosso), mentre region è SA
        partial_assignment[color] = region

        # controllo tutti i vincoli definiti
        for constraint_variables, constraint_function in self.constraints:
            # controllo solo se tutte le variabili del vincolo sono assegnate
            # var: ad es. ('WA','NT') o ('S','E','N','D','M','O','R','Y')
            all_assigned = True
            # contiene i valori delle variabili
            values = []
            for var in constraint_variables:
                if var not in partial_assignment:
                    all_assigned = False
                    # Esce dal loop del for
                    break
                values.append(partial_assignment[var])
            if not all_assigned:
                # Vado all'iterazione successiva senza eseguire il codice sotto
                continue


            # unpacking di constraint_function, cioè diventa constraint_function(values[0], values[1], ecc)
            # constraint_function in questo caso è il lambda color1, color2: color1 != color2
            # Se passiamo ('R','G') restituisce True, perché i colori sono diversi ed il vincolo è soddisfatto.
            # Se passiamo ('B','B') restituisce False, perché i colori coincidono e quindi il vincolo è violato essendo che avrei due regioni adiacenti con lo stesso colore.
            if not constraint_function(*values):
                # vincolo violato: rimuovo l'assegnazione parziale e ritorno False
                del partial_assignment[color]
                return False

        # Se nessun vincolo violato tolgo l'assegnazione parziale e ritorno True
        del partial_assignment[color]
        return True
