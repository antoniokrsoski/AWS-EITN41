import numpy as np
from typing import List, Tuple
import re

def evaluate_polynomial(coefficients: List[float], x: float) -> float:
    return sum(coef * (x ** i) for i, coef in enumerate(coefficients))

def lagrange_interpolation(points: List[Tuple[float, float]], x: float) -> float:
    result = 0
    for i, (xi, yi) in enumerate(points):
        term = yi
        for j, (xj, _) in enumerate(points):
            if i != j:
                term *= (x - xj) / (xi - xj)
        result += term
    return result

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
    k, n = 5, 8
    
    # get coefficients, you could also just take them out manually but thats not fun
    private_poly = parse_poly("13+8x+11x^2+x^3+5x^4")
    
    # we can just write everything manually, the question specificed a program that takes in some inputs
    # so i natrually thought it would take an arbirtary input, todo
    your_shares = {
        2: 161,
        3: 568,
        4: 1565,
        5: 3578,
        6: 7153,
        7: 12956,
        8: 21773
    }
    
    received_shares = {
        2: 75,
        3: 75,
        4: 54,
        5: 52,
        6: 77,
        7: 54,
        8: 43
    }
    
    master_points = [
        (2, 2782),
        (4, 30822),
        (5, 70960),
        (7, 256422)
    ]
    
    # compute f(1)
    value_at_1 = evaluate_polynomial(private_poly, 1)
    # compute f(1) + sum of everyone else f(1) with their private poly
    master_value_at_1 = value_at_1 + sum(received_shares.values())
    master_points.append((1, master_value_at_1))
    
    # f(0) - secret
    secret = round(lagrange_interpolation(master_points, 0))
    print(secret)

if __name__ == "__main__":
    main()