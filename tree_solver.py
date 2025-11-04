# Definizione del risolutore di alberi

# Implementa l'algoritmo TREE-CSP-SOLVER (Russell & Norvig, capitolo 5.5)
#  - passata bottom-up: MAKE-ARC-CONSISTENT(parent, child)
#  - passata top-down: assegnamento dei valori compatibili senza backtracking

from collections import deque

def tree_solve(csp_instance):
    """
    Risoluzione seguendo procedimento di R&N:
    1. Costruire strutture per vincoli binari e unari.
    2. Costruire il grafo di adiacenza usando solo i vincoli binari.
    3. Per ogni componente connessa (albero):
       a) scegliere una radice e ottenere un ordine topologico (padre prima dei figli).
       b) passata bottom-up (dal basso verso la radice): per ogni arco (parent, child) eseguire
          MAKE-ARC-CONSISTENT(parent, child) che rimuove dal dominio del parent i valori
          che non hanno alcun valore nel dominio del child che soddisfi il vincolo.
          Se qualche dominio diventa vuoto -> inconsistenza -> return None.
       c) passata top-down: assegnare un valore alla radice (qualsiasi valore rimasto),
          poi per ogni figlio scegliere un valore compatibile con il genitore (esiste di sicuro
          se la passata bottom-up ha avuto successo).
       d) Restituisce un dizionario assignment var->value se trova una soluzione,
          altrimenti None.
    """

    # 1) Separare vincoli binari e vincoli unari; controllare vincoli n-ari
    binary_constraints = {}  # key: frozenset({x,y}), quindi è un set immutabile
    unary_constraints = {}   # key: var -> lista di funzioni unarie

    # Scansione dei vincoli per popolare le due strutture
    for vars_tuple, func in csp_instance.constraints:
        # Salvo in un set immutabile il vincolo binario
        if len(vars_tuple) == 2:
            a_name, b_name = vars_tuple[0], vars_tuple[1]
            key = frozenset({a_name, b_name})
            # memorizziamo la funzione con l'ordine originale dei nomi
            binary_constraints[key] = (a_name, b_name, func)
        # Salvo in un set il vincolo unario
        elif len(vars_tuple) == 1:
            var_name = vars_tuple[0]
            unary_constraints.setdefault(var_name, []).append(func)
        else:
            # Presenza di vincolo n-ario (presenti solo in cryptoaritmetica e gestiti nella classe del cutset)
            # Ritorno None perchè l’algoritmo di tree solving (DAC - Directional Arc Consistency) è pensato per vincoli binari / unari.
            return None

    
    # 2) Costruzione grafo di adiacenza (usando solo vincoli binari)
    adjacency = {var: set() for var in csp_instance.variables}
    # Qui (a_name, b_name, _) va a prendere una tupla di 3 elemtni che contiene i valori del mio binary_constraints[key] = (a_name, b_name, func)
    # dato che voglio prendere solo i primi due valori ed ignorare il terzo (la func) per creare il grafo posso inserire
    # questo carattere _ che in Python si usa come variabili "usa e getta" e significa che sappiamo che li c'è un valore, ma che non ci interessa e lo ignoriamo
    for key, (a_name, b_name, _) in binary_constraints.items():
        adjacency[a_name].add(b_name)
        adjacency[b_name].add(a_name)

    # Se non ci sono variabili (CSP vuoto) ritorna vuoto
    if not csp_instance.variables:
        return {}
    
    # 3) Copia dei domini e applicazione immediata dei vincoli unari
    # Copia dei domini, contiene liste separate per evitare side-effects
    domains = {var: list(csp_instance.domains.get(var, [])) for var in csp_instance.variables}

    # Applichiamo i vincoli unari subito per ridurre i domini iniziali (pruning semplice)
    for var, funcs in unary_constraints.items():
        if var not in domains:
            # inconsistenza
            return None
        filtered_domain = []
        for value in domains[var]:
            # se il valore soddisfa tutte le condizioni unarie, lo manteniamo
            ok = True
            for f in funcs:
                try:
                    if not f(value):
                        ok = False
                        break
                except Exception:
                    # se la funzione lancia eccezione consideriamo il valore non valido
                    ok = False
                    break
            if ok:
                filtered_domain.append(value)
        domains[var] = filtered_domain
        if not domains[var]:
            # dominio vuoto dopo i vincoli unari -> inconsistente
            return None

    
    # 4) Risolvi componente per componente
    final_assignment = {}
    visited = set()

    # Itero su tutte le variabili per coprire eventuali componenti disconnesse
    for start_var in csp_instance.variables:
        if start_var in visited:
            continue

        # BFS per costruire parent map e ordine topologico in radice = start_var
        parent = {start_var: None}
        bfs_order = []
        queue = deque([start_var])
        visited.add(start_var)

        while queue:
            node = queue.popleft()
            bfs_order.append(node)
            for neighbor in adjacency[node]:
                if neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)
                    visited.add(neighbor)

        # Se la componente è un singolo nodo senza vicini la BFS la gestisce correttamente.
        # Ora vogliamo la post-order (children prima dei parent) per la passata bottom-up.
        postorder = list(reversed(bfs_order))

        
        # 4a) Passata bottom-up: ripulire i domini dei parent usando i child (MAKE-ARC-CONSISTENT)
        # Ripetiamo fino a punto fisso nella componente
        changed = True
        while changed:
            changed = False
            # iteriamo su postorder: i figli vengono prima dei padri
            for node in postorder:
                node_parent = parent[node]
                if node_parent is None:
                    continue  # la radice non ha parent in questa BFS
                # Individuiamo la funzione che lega node_parent e node
                key = frozenset({node_parent, node})
                if key not in binary_constraints:
                    # Se non c'è il vincolo binario, non facciamo nulla (nessun vincolo tra parent e child)
                    continue
                a_name, b_name, constraint_func = binary_constraints[key]
                # vogliamo chiamare constraint(parent_val, child_val)
                if (a_name, b_name) == (node_parent, node):
                    # la funzione è già nell'ordine giusto
                    func_parent_child = constraint_func
                else:
                    # bisogna invertire gli argomenti quando si chiama
                    func_parent_child = lambda parent_val, child_val, f=constraint_func: f(child_val, parent_val)

                # Costruiamo il nuovo dominio del parent filtrando i parent_val senza supporto nel child
                new_parent_domain = []
                for parent_val in domains[node_parent]:
                    # cerchiamo almeno un child_val che supporti parent_val
                    supported = False
                    for child_val in domains[node]:
                        try:
                            if func_parent_child(parent_val, child_val):
                                supported = True
                                break
                        except Exception:
                            # se la funzione solleva eccezione, ignoriamo quella coppia
                            continue
                    if supported:
                        new_parent_domain.append(parent_val)

                # Se il dominio del parent si è ridotto, aggiorniamo e segnaliamo il cambiamento
                if len(new_parent_domain) < len(domains[node_parent]):
                    domains[node_parent] = new_parent_domain
                    changed = True
                    # Se diventa vuoto siamo inconsistente: non esiste soluzione per questa componente
                    if not domains[node_parent]:
                        return None

        
        # 4b) Passata top-down: assegnamento senza backtracking
        # Assumiamo che ogni nodo abbia almeno un valore dopo bottom-up.
        # Scegliamo per la radice il primo valore valido (qualsiasi va bene)
        if not domains[start_var]:
            return None
        component_assignment = {}
        component_assignment[start_var] = domains[start_var][0]  # scelta arbitraria ma garantita compatibile

        # Seguiamo l'ordine BFS (padre prima dei figli) per assegnare i figli rispetto al parent
        for node in bfs_order:
            if node == start_var:
                continue
            node_parent = parent[node]
            # trovi il vincolo tra node_parent e node per verificarne la compatibilità
            key = frozenset({node_parent, node})
            # Se non esiste vincolo binario tra parent e child, possiamo scegliere un valore qualsiasi del child
            if key not in binary_constraints:
                if not domains[node]:
                    return None
                component_assignment[node] = domains[node][0]
                continue

            a_name, b_name, constraint_func = binary_constraints[key]
            if (a_name, b_name) == (node_parent, node):
                func_parent_child = constraint_func
            else:
                func_parent_child = lambda parent_val, child_val, f=constraint_func: f(child_val, parent_val)

            # cerchiamo il primo valore del child compatibile con il valore scelto del parent
            chosen_child_value = None
            parent_assigned_value = component_assignment[node_parent]
            for candidate_child_value in domains[node]:
                try:
                    if func_parent_child(parent_assigned_value, candidate_child_value):
                        chosen_child_value = candidate_child_value
                        break
                except Exception:
                    continue
            if chosen_child_value is None:
                # Questo non dovrebbe accadere se bottom-up ha funzionato, ma lo gestiamo comunque
                return None
            component_assignment[node] = chosen_child_value

        # Uniamo l'assegnamento della componente all'assegnamento globale
        final_assignment.update(component_assignment)

    # Se siamo arrivati qui, ogni componente è stata assegnata con successo
    return final_assignment
