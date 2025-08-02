# funzioni per trovare il cutset e applicare il cutset conditioning

from itertools import product
from csp import CSP
from tree_solver import tree_backtrack

def find_cycle_cutset(csp):
    # Costruisce lista di adiacenze
    adj = {v:set() for v in csp.variables}
    for vars_tuple, _ in csp.constraints:
        if len(vars_tuple)==2:
            v1,v2 = vars_tuple
            adj[v1].add(v2); adj[v2].add(v1)
    # DFS per ciclo
    def has_cycle():
        visited=set()
        def dfs(u, parent):
            visited.add(u)
            for w in adj[u]:
                if w==parent: continue
                if w in visited or dfs(w,u):
                    return True
            return False
        return any(dfs(v,None) for v in csp.variables if v not in visited)
    cutset=set()
    while has_cycle():
        # variabile di max grado
        v=max(adj, key=lambda x: len(adj[x]))
        cutset.add(v)
        for w in list(adj[v]):
            adj[w].remove(v)
        adj[v].clear()
    return list(cutset)

def cutset_conditioning_explain(csp):
    print("\n=== CUTSET CONDITIONING ===")
    print("Variabili:", csp.variables)
    cutset = find_cycle_cutset(csp)
    print("Cutset individuato:", cutset)
    # 1) enumerazione
    for vals in product(*[csp.domains[v] for v in cutset]):
        partial = dict(zip(cutset, vals))
        print("\n--- Provo assegnazione partial:", partial)
        # 2) verifica interna
        ok=True
        for vars_tuple, func in csp.constraints:
            if all(v in partial for v in vars_tuple):
                if not func(*(partial[v] for v in vars_tuple)):
                    print("partial viola vincolo su", vars_tuple)
                    ok=False; break
        if not ok:
            continue
        # 3) costruzione residual CSP
        res_vars=[v for v in csp.variables if v not in cutset]
        res_domains={v:[] for v in res_vars}
        res_constraints=[]
        # mantieni vincoli inter-residui e trasforma vincoli cutset→residui
        for vars_tuple, func in csp.constraints:
            vs=set(vars_tuple)
            if vs<=set(res_vars):
                res_constraints.append((vars_tuple,func))
            elif vs & set(cutset) and vs & set(res_vars):
                # trasformo in unario su variabile residua
                cut, res = (vars_tuple[0],vars_tuple[1]) if vars_tuple[0] in cutset else (vars_tuple[1],vars_tuple[0])
                x=partial[cut]
                res_constraints.append(((res,), lambda y,f=func,x=x: f(x,y)))
        # filtro domini
        for v in res_vars:
            funcs=[f for (vt,f) in res_constraints if len(vt)==1 and vt[0]==v]
            for val in csp.domains[v]:
                if all(f(val) for f in funcs):
                    res_domains[v].append(val)
        print("residual vars/domains:", list(zip(res_vars,[res_domains[v] for v in res_vars])))
        # 4) risolvo
        sol = tree_backtrack(CSP(res_vars,res_domains,res_constraints), res_vars)
        if sol is not None:
            print("Sol residua trovata:", sol)
            sol.update(partial)
            print("SOLUZIONE COMPLETA:", sol)
            return sol
        else:
            print("Nessuna soluzione residual, proseguo…")
    print("Fallito: nessuna assegnazione di cutset porta a soluzione.")
    return None
