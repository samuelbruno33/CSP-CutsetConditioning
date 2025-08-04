import os
from contextlib import redirect_stdout

from cutset import solve_with_cutset
from mapcolor import australia_csp, europe_simplified_csp, usa_simplified_csp
from cryptarithmetic import send_more_money_csp, t_plus_t_eq_ee_csp, two_two_two_eq_six_csp

def save_file_log(name, func):
    os.makedirs("logs_of_istances", exist_ok=True)
    path = f"logs_of_istances/{name}.txt"
    with open(path, "w") as log_file, redirect_stdout(log_file):
        print(f"=== ISTANZA: {name} ===")
        csp_instance = func()
        sol = solve_with_cutset(csp_instance)
        print(f"\n---> SOLUZIONE FINALE: {sol}")

    print(f"Log di '{name}' scritto in: {path}")

def main():
    for name, map in [
        ("Australia", australia_csp),
        ("Europa_semplificata", europe_simplified_csp),
        ("USA_semplificata", usa_simplified_csp)
    ]:
        save_file_log(f"Mappa_{name}", map)

    for name, crypt in [
        ("T+T=EE", t_plus_t_eq_ee_csp),
        ("SEND+MORE=MONEY", send_more_money_csp),
        ("TWO+TWO+TWO=SIX", two_two_two_eq_six_csp)
    ]:
        save_file_log(f"Cryptoaritmetica_{name}", crypt)

if __name__ == "__main__":
    main()
