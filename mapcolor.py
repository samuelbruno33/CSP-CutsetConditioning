# genera le 3 istanze di map coloring

from csp import CSP

def australia_csp():
    vars = ['WA','NT','SA','Q','NSW','V','T']
    doms = {v:['R','G','B'] for v in vars}
    edges = [('WA','NT'),('WA','SA'),('NT','SA'),
             ('NT','Q'),('SA','Q'),('SA','NSW'),
             ('SA','V'),('Q','NSW'),('NSW','V')]
    cons = [((x,y), lambda a,b: a!=b) for x,y in edges]
    return CSP(vars, doms, cons)

def europe_simplified_csp():
    vars = ['P','S','F','I','SW','G','B','NL','A','CZ','PL']
    doms = {v:['R','G','B','Y'] for v in vars}
    edges = [
      ('P','S'),('S','F'),('F','I'),('I','SW'),('SW','G'),('G','CZ'),
      ('CZ','PL'),('PL','G'),('G','A'),('A','I'),('F','G'),
      ('F','B'),('B','NL'),('NL','G'),('SW','A'),('F','SW'),
      ('G','B'),('G','PL'),('CZ','A'),('S','P'),('F','S')
    ]
    cons = [((x,y), lambda a,b: a!=b) for x,y in edges]
    return CSP(vars, doms, cons)

def usa_simplified_csp():
    vars=['WA','OR','CA','NV','UT']
    doms={v:['R','G','B'] for v in vars}
    edges=[('WA','OR'),('OR','CA'),('CA','NV'),
           ('NV','UT'),('UT','OR'),('CA','UT')]
    cons=[((x,y), lambda a,b: a!=b) for x,y in edges]
    return CSP(vars, doms, cons)
