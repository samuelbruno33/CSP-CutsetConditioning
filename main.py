from cutset import solve_with_cutset
from mapcolor import australia_csp, europe_csp, usa_simple_csp
from cryptarithmetic import send_more_money_csp, t_plus_t_eq_ee_csp, two_two_two_eq_six_csp

def main():
    for name, f in [
        ("Australia", australia_csp),
        ("Europa", europe_csp),
        ("USA", usa_simple_csp)
    ]:
        print("\n-- Maps ", name)
        solve_with_cutset(f())

    for name, f in [
        ("T+T=EE", t_plus_t_eq_ee_csp),
        ("SEND+MORE=MONEY", send_more_money_csp),
        ("TWO+TWO+TWO=SIX", two_two_two_eq_six_csp)
    ]:
        print("\n-- Cryptarithmetic ", name)
        solve_with_cutset(f())

if __name__ == "__main__":
    main()
