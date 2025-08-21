# Definizione della classe CSP

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables # lista di variabili che devo assegnare (ad es. ['WA','NT','SA', ecc])
        self.domains = domains # dict di var -> lista di valori possibili (ad es. {'WA':['R','G','B'], ecc})
        # constraints: lista di vincoli, di tipo (constraint_variables, constraint_function)
        #   - constraint_variables: contiene i nomi delle variabili coinvolte
        #   - constraint_function: funzione che riceve i values e restituisce True/False se rispetta o no i vincoli
        self.constraints = constraints

    def is_consistent(self, variable, value, partial_assignment):
        # partial_assignment: dizionario delle variabili già assegnate
        # Provo ad aggiungere un colore all'assegnazione parziale con una regione
        # infatti value è R (rosso), mentre variable è SA
        # mentre per quanto riguarda la criptoaritmetica, variable è ad esempio S (in send more money) e value è il valore che voglio assegnargli
        partial_assignment[variable] = value

        # controllo tutti i vincoli disponibili nel CSP
        for constraint_variables, constraint_function in self.constraints:

            # controllo se il vincolo può essere valutato, e questo è possibile solo se tutte le variabili del vincolo sono assegnate,
            # perchè se ho ('WA','NT') e 'WA' = 'R' ma 'NT' ancora non è stato valutato allora non ha senso controllare il vincolo, essendo 'NT' privo di colore assegnato ancora
            # var: ad es. ('WA','NT') o ('S','E','N','D','M','O','R','Y')

            # flag che indica se tutte le variabili del vincolo sono presenti in partial_assignment
            all_assigned = True
            # contiene i valori delle variabili nello stesso ordine di constraint_variables
            values = []
            for var in constraint_variables:
                # Se trovo una variabile non ancora assegnata non posso valutare il vincolo ora
                if var not in partial_assignment:
                    all_assigned = False
                    # Esce dal loop del for e salto la valutazione di questo vincolo
                    break

                # se la variabile è assegnata prendo il suo valore e lo aggiungo alla lista
                values.append(partial_assignment[var])

            # Se almeno una variabile non è assegnata passo al vincolo successivo
            if not all_assigned:
                # Vado all'iterazione successiva senza eseguire il codice sotto
                continue

            # unpacking di constraint_function, cioè diventa constraint_function(values[0], values[1], ecc)
            # constraint_function in questo caso è il lambda color1, color2: color1 != color2
            # Se passiamo ('R','G') restituisce True, perché i colori sono diversi ed il vincolo è soddisfatto.
            # Se passiamo ('B','B') restituisce False, perché i colori coincidono e quindi il vincolo è violato essendo che avrei due regioni adiacenti con lo stesso colore.
            if not constraint_function(*values):
                # vincolo violato: rimuovo l'assegnazione parziale e ritorno False
                del partial_assignment[variable]
                return False

        # Se nessun vincolo violato tolgo l'assegnazione parziale e ritorno True
        del partial_assignment[variable]
        return True
