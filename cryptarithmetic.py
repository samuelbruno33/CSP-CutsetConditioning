# generata le 3 istanze criptoaritmetiche

from csp import CSP

def send_more_money_csp():
    vars = ['S','E','N','D','M','O','R','Y']
    doms = {v:list(range(10)) for v in vars}
    doms['S'], doms['M'] = list(range(1,10)), list(range(1,10))
    cons = []
    for i in range(len(vars)):
        for j in range(i+1,len(vars)):
            a,b = vars[i], vars[j]
            cons.append(((a,b), lambda x,y: x!=y))
    cons.append((tuple(vars),
        lambda S,E,N,D,M,O,R,Y:
            (1000*S+100*E+10*N+D)
          +(1000*M+100*O+10*R+E)
          ==(10000*M+1000*O+100*N+10*E+Y)
    ))
    return CSP(vars, doms, cons)

def t_plus_t_eq_ee_csp():
    return CSP(['T','E'], {'T':list(range(1,10)),'E':list(range(10))},
               [(('T','E'), lambda T,E: 2*T==11*E)])

def two_two_two_eq_six_csp():
    vars = ['T','W','O','S','I','X']
    doms = {v:list(range(10)) for v in vars}
    doms['T'], doms['S'] = list(range(1,10)), list(range(1,10))
    cons = []
    for i in range(len(vars)):
        for j in range(i+1,len(vars)):
            a,b = vars[i], vars[j]
            cons.append(((a,b), lambda x,y: x!=y))
    cons.append((tuple(vars),
        lambda T,W,O,S,I,X:
            3*(100*T+10*W+O) == 100*S+10*I+X
    ))
    return CSP(vars, doms, cons)
