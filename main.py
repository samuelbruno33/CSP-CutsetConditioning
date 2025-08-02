import os
from contextlib import redirect_stdout
from cutset import cutset_conditioning_explain
from mapcolor import australia_csp, europe_simplified_csp, usa_simplified_csp
from cryptarithmetic import (
    send_more_money_csp,
    t_plus_t_eq_ee_csp,
    two_two_two_eq_six_csp
)

LOG_DIR = "logs_of_istances"
os.makedirs(LOG_DIR, exist_ok=True)

def run_and_log(name, gen):
    """
    name: stringa identificativa
    gen:   o funzione che ritorna un CSP, o direttamente un CSP
    """
    # Decide se 'gen' è una funzione o un CSP già istanziato
    if callable(gen):
        csp = gen()
    else:
        csp = gen

    path = os.path.join(LOG_DIR, f"{name.replace(' ','_')}.txt")
    with open(path, "w") as f, redirect_stdout(f):
        print(f"=== ESECUZIONE: {name} ===\n")
        sol = cutset_conditioning_explain(csp)
        print(f"\n--- RISULTATO FINALE PER {name}: {sol}\n")
    print(f"Log di '{name}' scritto in: {path}")


def test_maps():
    for name, gen in [
        ("Australia", australia_csp),
        ("Europa semplificata", europe_simplified_csp()),
        ("USA semplificata", usa_simplified_csp()),
    ]:
        run_and_log(f"MAP_{name}", gen)

def test_cryptarithmetics():
    for name, gen in [
        ("T_plus_T_eq_EE", t_plus_t_eq_ee_csp),
        ("SEND_MORE_MONEY", send_more_money_csp),
        ("TWO_TWO_TWO_eq_SIX", two_two_two_eq_six_csp),
    ]:
        run_and_log(f"CRYPTO_{name}", gen)

if __name__ == '__main__':
    test_maps()
    test_cryptarithmetics()
