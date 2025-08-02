# generata le 3 istanze criptoaritmetiche
# crypto.py
from csp import CSP

def send_more_money_csp():
    vars = ['S','E','N','D','M','O','R','Y']
    doms = {v:list(range(10)) for v in vars}
    doms['S']=list(range(1,10)); doms['M']=list(range(1,10))
    cons=[]
    # all-different
    for i in range(len(vars)):
        for j in range(i+1,len(vars)):
            cons.append(((vars[i],vars[j]), lambda a,b: a!=b))
    # vincolo n-ario di somma
    def sum_send_more(S,E,N,D,M,O,R,Y):
        return ((1000*S+100*E+10*N+D)
              +(1000*M+100*O+10*R+E)
              ==(10000*M+1000*O+100*N+10*E+Y))
    cons.append((tuple(vars), sum_send_more))
    return CSP(vars, doms, cons)

def t_plus_t_eq_ee_csp():
    vars=['T','E']
    doms={v:list(range(10)) for v in vars}
    doms['T']=list(range(1,10))
    cons=[(('T','E'), lambda T,E: 2*T==11*E)]
    return CSP(vars, doms, cons)

def two_two_two_eq_six_csp():
    vars=['T','W','O','S','I','X']
    doms={v:list(range(10)) for v in vars}
    doms['T']=list(range(1,10)); doms['S']=list(range(1,10))
    cons=[]
    # all-different
    for i in range(len(vars)):
        for j in range(i+1,len(vars)):
            cons.append(((vars[i],vars[j]), lambda a,b: a!=b))
    # vincolo n-ario tripla somma
    def sum_two_two_two(T,W,O,S,I,X):
        return 3*(100*T+10*W+O)==100*S+10*I+X
    cons.append((tuple(vars), sum_two_two_two))
    return CSP(vars, doms, cons)
