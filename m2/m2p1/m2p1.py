import re
from typing import List

def parse_poly(eqn: str) -> List[int]:
    # cred to darthbhyrava Nov 29, 2019 at 20:11 on stack
    if eqn == "":
        return []

    # add a leading 1 where necessary
    eqn = '1'+eqn if not eqn[0].isdigit() else eqn

    # remove all powers
    no_carets = re.sub(r"(\^\d+)", "", eqn)

    # get numeric coefficients
    raw_coeffs = re.findall(r'[+-]?\d*\.?\d*(?=x?)', no_carets)
    
    # add a 1 to lone signs and convert coefficients to int
    coeffs = [int(float(x+'1')) if x in ['+', '-'] or x == '' else int(float(x)) for x in raw_coeffs if x]
    return coeffs

def main():

if __name__ == "__main__":
    main()