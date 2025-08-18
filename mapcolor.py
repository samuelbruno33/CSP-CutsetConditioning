# Genera le 3 istanze di map coloring

from csp import CSP

def australia_csp():
    """
    Mappa dell'Australia:
    WA, NT, SA, Q, NSW, V, T con 3 colori
    Le regioni sono: WA (Western Australia), NT (Northern Territory), SA (South Australia), Q (Queensland),
    NSW (New South Wales), V (Victoria), T (Tasmania)
    """
    variables = ['WA','NT','SA','Q','NSW','V','T']
    domains = {v: ['R','G','B'] for v in variables}
    # regioni adiacenti
    edges = [
        ('WA','NT'),('WA','SA'),('NT','SA'),
        ('NT','Q'),('SA','Q'),('SA','NSW'),
        ('SA','V'),('Q','NSW'),('NSW','V')]

    # vincolo: colori diversi se adiacenti
    constraints = [((v1, v2), lambda c1,c2: c1 != c2) for v1,v2 in edges]
    return CSP(variables, domains, constraints)

def europe_simplified_csp():
    """
    Mappa semplificata dell'Europa centrale con 11 stati e 4 colori
    I paesi sono: Portogallo (P), Spagna (S), Francia (F), Italia (I), Svizzera (SW), Germania (G), Belgio (B),
    Paesi Bassi (NL), Austria (A), Repubblica Ceca (CZ), Polonia (PL)

    Si possono usare 4 colori perchè secondo il teorema dei quattro colori, qualunque mappa piana può
    essere colorata con al massimo 4 colori senza che due regioni adiacenti condividano lo stesso.
    """
    variables = ['P','S','F','I','SW','G','B','NL','A','CZ','PL']
    domains = {v: ['R','G','B','Y'] for v in variables}
    edges = [('P','S'),('S','F'),('F','I'),('I','SW'),
        ('SW','G'),('G','CZ'),('CZ','PL'),('PL','G'),
        ('G','A'),('A','I'),('F','G'),('F','B'),
        ('B','NL'),('NL','G'),('SW','A'),('F','SW'),
        ('G','B'),('G','PL'),('CZ','A')]

    constraints = [((v1, v2), lambda c1,c2: c1 != c2) for v1,v2 in edges]
    return CSP(variables, domains, constraints)

def usa_simplified_csp():
    """
    Mappa semplificata degli Stati Uniti con 5 stati e 3 colori
    Gli stati sono: WA (Washington), OR (Oregon), CA (California), NV (Nevada), UT (Utah)
    """
    variables = ['WA','OR','CA','NV','UT']
    domains = {v: ['R','G','B'] for v in variables}
    edges = [('WA','OR'),('OR','CA'),('CA','NV'),
             ('NV','UT'),('UT','OR'),('CA','UT')]

    constraints = [((v1, v2), lambda c1,c2: c1 != c2) for v1,v2 in edges]
    return CSP(variables, domains, constraints)
