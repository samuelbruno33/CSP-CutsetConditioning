# Genera le 3 istanze criptoaritmetiche
from csp import CSP

def send_more_money_csp():
    """
    SEND + MORE = MONEY
    8 lettere, domini 0-9 con M,S diversi da 0
    """
    variables = ['S','E','N','D','M','O','R','Y']
    domains   = {v: list(range(10)) for v in variables}
    domains['S'] = list(range(1,10))
    domains['M'] = list(range(1,10))

    constraints = []
    # vincolo all-different binario
    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            v1, v2 = variables[i], variables[j]
            constraints.append(((v1, v2), lambda x,y: x != y))

    # vincolo n-ario di somma
    def sum_send_more(S,E,N,D,M,O,R,Y):
        return (
            (1000*S + 100*E + 10*N + D) +
            (1000*M + 100*O + 10*R + E) ==
            (10000*M + 1000*O + 100*N + 10*E + Y)
        )
    constraints.append((tuple(variables), sum_send_more))
    return CSP(variables, domains, constraints)

def t_plus_t_eq_ee_csp():
    """
    T + T = EE
    2 variabili, dominio 0-9 con T diverso da 0
    """
    variables = ['T','E']
    domains   = {'T': list(range(1,10)), 'E': list(range(10))}
    constraints = [
        (('T','E'), lambda T,E: 2*T == 11*E)
    ]
    return CSP(variables, domains, constraints)

def two_two_two_eq_six_csp():
    """
    TWO + TWO + TWO = SIX
    6 lettere, domini 0-9 con T,S diversi da 0
    """
    variables = ['T','W','O','S','I','X']
    domains   = {v: list(range(10)) for v in variables}
    domains['T'] = list(range(1,10))
    domains['S'] = list(range(1,10))

    constraints = []
    # vincolo all-different
    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            v1, v2 = variables[i], variables[j]
            constraints.append(((v1, v2), lambda x,y: x != y))

    # vincolo tripla somma
    def sum_three_two(T,W,O,S,I,X):
        return 3*(100*T + 10*W + O) == 100*S + 10*I + X
    constraints.append((tuple(variables), sum_three_two))
    return CSP(variables, domains, constraints)
