# definizione della classe CSP

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables  = variables    # lista di variabili che devo assegnare
        self.domains    = domains      # uno dei possibili valori del dominio
        self.constraints = constraints # lista di vincoli del tipo (vars_tuple, func)

    def consistent(self, var, val, assignment):
        # assignment: dict parziale delle variabili già assegnate
        # Provo ad aggiungere var=val all'assegnazione parziale
        # -> ad es. val è R (colore rosso), mentre var è SA (regione mappa Australia)
        assignment[var] = val
        # Controllo tutti i vincoli di qualunque numero di variabili
        for vars_tuple, func in self.constraints:
            ready = True
            vals = []
            # Controllo solo se tutte le variabili del vincolo sono in assignment
            # vars_tuple: es. ('WA','NT') o ('S','E','N','D','M','O','R','Y')
            for v in vars_tuple:
                if v not in assignment:
                    ready = False
                    break
                vals.append(assignment[v])
            if not ready:
                continue
            # func: funzione che prende len(vars_tuple) valori e ritorna True/False
            # unpacking: func(*vals) equivale a func(vals[0], vals[1], ecc ecc)
            if not func(*vals):
                # se il vincolo fallisce, tolgo var e restituisco Fals
                del assignment[var]
                return False
        #Se nessun vincolo è stato violato, tolgo var e restituisco True
        del assignment[var]
        return True
