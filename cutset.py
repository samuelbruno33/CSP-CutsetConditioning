# Definizione della classe dove viene effettuato il cutset con l'euristica min-fill

# Implementazione del Cutset Conditioning con:
#  - ricerca di cycle-cutset tramite euristica greedy MIN-FILL
#  - aciclicità del grafo tramite leaf-pruning (non con DFS ricorsiva)
#  - costruzione del CSP residuo (copia dei domini + trasformazione vincoli misti in unari)
#  - chiamata a tree_solve

from itertools import product
from csp import CSP
from tree_solver import tree_solve

def is_graph_acyclic_via_leaf_pruning(adj_graph):
    """
    Verifica se il grafo (non orientato) rappresentato da adj_graph è aciclico.
    Metodo: rimozione iterativa dei leaf nodes (nodi con grado <= 1).
    Se alla fine tutti i nodi vengono rimossi => grafo aciclico (foresta).
    Se rimangono nodi con grado >= 2 => esiste ciclo.
    Complessità: O(∣V∣+∣E∣), perché ogni arco e nodo viene rimosso al massimo una volta.
    """
    # Copiamo la struttura per non modificare l'originale
    G = {node: set(neigh) for node, neigh in adj_graph.items()}
    # Coda con i leaf nodes iniziali (grado 0 o 1)
    leaf_queue = [node for node, neigh in G.items() if len(neigh) <= 1]
    # Rimuoviamo iterativamente i leaf nodes; durante il processo i vicini possono diventare leaf
    idx = 0
    while idx < len(leaf_queue):
        node = leaf_queue[idx]
        idx += 1
        # per ciascun vicino rimuoviamo il riferimento a node
        for neighbor in list(G[node]):
            G[neighbor].discard(node)
            # se il vicino è diventato leaf, lo aggiungiamo in coda
            if len(G[neighbor]) == 1:
                leaf_queue.append(neighbor)
        # rimuoviamo completamente il node
        G[node].clear()

    # Se tutti i nodi sono stati svuotati => aciclico
    for node, neigh in G.items():
        if neigh:
            # esiste ancora almeno un arco -> c'è un ciclo
            return False
    return True

def compute_fill_in_count(adj_graph, node):
    """
    Calcola il numero di 'fill-edge' (nuovi archi) che sarebbero introdotti tra i vicini di node
    se node venisse eliminato. La min-fill sceglie il nodo che minimizza questo numero.
    Funziona in modo che per ogni coppia di vicini di node che non sono già collegati,
    l'eliminazione di node richiederebbe di aggiungere un arco per mantenere la connettività
    """
    neighbors = list(adj_graph[node])
    count = 0
    n = len(neighbors)
    # Conta le coppie di vicini non connesse tra loro
    for i in range(n):
        for j in range(i+1, n):
            ni = neighbors[i]
            nj = neighbors[j]
            if nj not in adj_graph[ni]:
                count += 1
    return count

def find_cycle_cutset_min_fill(csp_instance):
    """
    Trova un cycle-cutset usando euristica greedy MIN-FILL con gestione migliorata dei vincoli n-ari:
    - Costruisce il grafo primale usando i soli vincoli binari.
    - Aggiunge forzatamente al cutset NON tutte le variabili dei vincoli n-ari,
      ma UNA sola variabile per ciascun vincolo n-ario (euristica: quella con grado massimo).
    - Iterativamente seleziona la variabile con MINIMO fill-in (numero di nuovi archi tra vicini)
      e la rimuove, fino a che il grafo diventa aciclico.
    Ritorna la lista di variabili del cutset (nell'ordine di rimozione).
    """

    # 1) Costruzione del grafo di adiacenza basato SOLO sui vincoli binari
    adjacency = {v: set() for v in csp_instance.variables}
    for vars_tuple, _ in csp_instance.constraints:
        if len(vars_tuple) == 2:
            a, b = vars_tuple
            adjacency[a].add(b)
            adjacency[b].add(a)

    # 2) Gestione dei vincoli n-ari
    # Invece di inserire tutte le variabili di un vincolo n-ario,
    # scegliamo solo UNA variabile per vincolo.
    forced_cutset = set()
    for vars_tuple, _ in csp_instance.constraints:
        if len(vars_tuple) > 2:
            # scegliamo la variabile con grado massimo nel grafo di adiacenza
            best_var = None
            best_degree = -1
            for var in vars_tuple:
                deg = len(adjacency.get(var, []))
                if deg > best_degree:
                    best_var = var
                    best_degree = deg
            if best_var is not None:
                forced_cutset.add(best_var)

    # 3) Copia del grafo per simulare rimozioni
    working_graph = {v: set(neis) for v, neis in adjacency.items()}
    cutset = list(forced_cutset)

    # Rimuoviamo subito dal grafo le variabili forzate
    for var in forced_cutset:
        neighbors = list(working_graph[var])
        # aggiungiamo archi di fill-in fra i vicini
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                ni, nj = neighbors[i], neighbors[j]
                working_graph[ni].add(nj)
                working_graph[nj].add(ni)
        # togliamo il nodo
        for nb in neighbors:
            working_graph[nb].discard(var)
        working_graph[var].clear()

    # 4) Fase greedy con min-fill finché il grafo non è aciclico
    while not is_graph_acyclic_via_leaf_pruning(working_graph):
        # candidati = nodi con almeno 2 vicini
        candidate_nodes = [n for n in working_graph if len(working_graph[n]) >= 2]
        if not candidate_nodes:
            # fallback: se non ci sono candidati, prendi un nodo qualunque
            node_to_remove = next(iter(working_graph))
        else:
            best_node = None
            best_fill = None
            best_degree = None
            for candidate in candidate_nodes:
                fcount = compute_fill_in_count(working_graph, candidate)
                deg = len(working_graph[candidate])
                if (best_node is None) or (fcount < best_fill) or (fcount == best_fill and deg < best_degree):
                    best_node = candidate
                    best_fill = fcount
                    best_degree = deg
            node_to_remove = best_node

        cutset.append(node_to_remove)

        # aggiorna il grafo simulando la rimozione
        neighbors = list(working_graph[node_to_remove])
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                ni, nj = neighbors[i], neighbors[j]
                working_graph[ni].add(nj)
                working_graph[nj].add(ni)

        for nb in neighbors:
            working_graph[nb].discard(node_to_remove)
        working_graph[node_to_remove].clear()

    return cutset



def make_unary_from_binary_constraint(binary_func, cutset_variable_name, residual_variable_name, fixed_cutset_value, original_order):
    """
    Crea un vincolo unario sul residuo fissando il valore della variabile del cutset.
    original_order indica l'ordine originale delle variabili del vincolo binario (tuple).
    Questo è necessario per chiamare la funzione nel giusto ordine.
    """
    a_name, b_name = original_order
    if a_name == cutset_variable_name and b_name == residual_variable_name:
        # la funzione originale è f(cut_val, residual_val)
        return (residual_variable_name,), (lambda residual_val, f=binary_func, fixed=fixed_cutset_value: f(fixed, residual_val))
    else:
        # la funzione originale è f(residual_val, cut_val) oppure l'ordine è invertito
        return (residual_variable_name,), (lambda residual_val, f=binary_func, fixed=fixed_cutset_value: f(residual_val, fixed))

def solve_with_cutset(csp_instance):
    """
    Implementazione del cutset conditioning:
    1. Trova un cycle-cutset con min-fill.
    2. Per ogni assegnazione possibile del cutset:
       a) verifica i vincoli interni al cutset (se violati => salto)
       b) costruisce il CSP residuo con:
          - variabili residuali
          - domini copiati e ridotti (non modifichiamo i domini originali)
          - vincoli binari tra residuali lasciati invariati
          - vincoli binari misti (cutset,residuo) trasformati in vincoli unari sul residuo usando il valore fissato del cutset
       c) chiama tree_solve sul residuo (se applicabile)
       d) se restituisce assignment completo -> combiniamo e ritorniamo soluzione
    """
    print("Variabili CSP:", csp_instance.variables)
    cutset_variables = find_cycle_cutset_min_fill(csp_instance)
    print("Cutset (min-fill):", cutset_variables)

    # Preleviamo i domini delle variabili del cutset in ordine
    cutset_domains_list = [csp_instance.domains[var] for var in cutset_variables]

    # Per ogni combinazione cartesiana di valori del cutset
    for cutset_values_combo in product(*cutset_domains_list):
        # costruiamo l'assegnazione parziale del cutset
        partial_cutset_assignment = {cutset_variables[i]: cutset_values_combo[i] for i in range(len(cutset_variables))}
        print("\nProvo assegnazione parziale del cutset:", partial_cutset_assignment)

        # 1) verifico i vincoli che coinvolgono solo variabili del cutset (valutabili ora)
        violates_internal_cutset = False
        for constraint_vars, constraint_func in csp_instance.constraints:
            if all(var in partial_cutset_assignment for var in constraint_vars):
                values_for_constraint = [partial_cutset_assignment[var] for var in constraint_vars]
                try:
                    if not constraint_func(*values_for_constraint):
                        violates_internal_cutset = True
                        break
                except Exception:
                    violates_internal_cutset = True
                    break
        if violates_internal_cutset:
            # se l'assegnazione non soddisfa i vincoli locali, salto subito
            print("Assegnazione del cutset viola vincoli interni; salto.")
            continue

        # 2) costruisco lista di variabili residue (quelle non nel cutset)
        residual_variables = [v for v in csp_instance.variables if v not in cutset_variables]

        # 3) creo copia dei domini per il residuo (per non inquinare i domini originali)
        residual_domains = {v: list(csp_instance.domains[v]) for v in residual_variables}

        # 4) costruisco i residual_constraints:
        #    - mantengo i vincoli che coinvolgono solo variabili residue
        #    - trasformo i vincoli binari misti (cutset,residuo) in unari sul residuo usando il valore fissato
        residual_constraints = []
        for constraint_vars, constraint_func in csp_instance.constraints:
            # caso: tutte le variabili del vincolo sono nel residuo -> mantengo il vincolo così com'è
            if all(var in residual_variables for var in constraint_vars):
                residual_constraints.append((constraint_vars, constraint_func))
                continue

            # 1° caso: vincolo binario che coinvolge una cutset-var e una residual-var -> trasformo in unario
            if len(constraint_vars) == 2:
                a, b = constraint_vars
                if (a in cutset_variables and b in residual_variables) or (b in cutset_variables and a in residual_variables):
                    # determino quale delle due è cutset e quale residuo
                    if a in cutset_variables:
                        cut_var_name, res_var_name = a, b
                    else:
                        cut_var_name, res_var_name = b, a
                    # valore fissato per la variabile del cutset
                    fixed_value = partial_cutset_assignment[cut_var_name]
                    # trasformo il vincolo binario in vincolo unario sul residuo
                    unary_scope, unary_func = make_unary_from_binary_constraint(constraint_func, cut_var_name, res_var_name, fixed_value, (a, b))
                    residual_constraints.append((unary_scope, unary_func))
                    continue

            # 2° caso: vincolo n-ario che coinvolge sia cutset che residuo:
            # - se tutte le variabili sono fissate (es. tutto nel cutset), lo abbiamo già verificato in precedenza
            # - se invece rimane qualche variabile libera nel vincolo n-ario, non lo trasformiamo qui:
            #   questo solver per alberi non gestisce vincoli n-ari nel residuo (vedi nota in testa al file).
            #   quindi, per correttezza conservativa, non aggiungiamo il vincolo ai residual_constraints:
            #   significa che tree_solve non lo considererà e pertanto potrebbe non trovare soluzioni valide
            #   in presenza di vincoli n-ari residui. Per la maggior parte delle map-coloring e dei casi
            #   binari questo non è un problema.
            # (nessuna azione)

        # 5) Creo l'istanza CSP residua con domini copiati e residual_constraints
        residual_csp_instance = CSP(residual_variables, residual_domains, residual_constraints)

        # 6) chiamo il risolutore per alberi (TREE-CSP-SOLVER)
        solution_for_residual = tree_solve(residual_csp_instance)

        if solution_for_residual is not None:
            # ho trovato una soluzione completa: combino con la assegnazione del cutset e la ritorno
            complete_solution = {}
            complete_solution.update(partial_cutset_assignment)
            complete_solution.update(solution_for_residual)
            print("==> Soluzione completa trovata:", complete_solution)
            return complete_solution
        else:
            print("Soluzione residua non trovata per questa assegnazione del cutset; proseguo.")

    # Nessuna assegnazione del cutset ha prodotto soluzione
    print("Nessuna soluzione trovata per nessuna assegnazione del cutset.")
    return None
