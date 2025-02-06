import numpy as np
from typing import List, Tuple
import re
from m2p1 import *

def main():
    k, n = 4, 6
    
    private_poly = parse_poly("2+12x+20x^2+18x^3")
    
    your_shares = {
        2: 250,
        3: 704,
        4: 1522,
        5: 2812,
        6: 4682
    }
    
    received_shares = {
        2: 44,
        3: 23,
        4: 34,
        5: 41,
        6: 42
    }
    
    master_points = [
        (3, 2930),
        (5, 11816),
        (6, 19751)
    ]
    
    your_value_at_1 = evaluate_polynomial(private_poly, 1)
    master_value_at_1 = your_value_at_1 + sum(received_shares.values())
    master_points.append((1, master_value_at_1))
    
    secret = round(lagrange_interpolation(master_points, 0))
    
    print(secret)

if __name__ == "__main__":
    main()