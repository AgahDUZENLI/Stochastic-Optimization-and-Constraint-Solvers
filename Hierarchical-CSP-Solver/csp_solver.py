import math
import csv

MIN_VAL, MAX_VAL = 1, 120

# Check if a value is within the allowed range
def in_domain(value):
    return MIN_VAL <= value <= MAX_VAL

nva = [0]

def assign(variable_name, value, assignment_dict):
    if not in_domain(value):
        return False
    if variable_name not in assignment_dict:
        nva[0] += 1
    elif assignment_dict[variable_name] != value:
        nva[0] += 1
    assignment_dict[variable_name] = value
    return True

# ----------
# PROBLEM A
#   C1: A = B^2 - C^2
#   C2: E + F > B
#   C3: D = B^2 - 3*A
#   C4: (B-C)^2 = E*F*C - 1861
#   C5: C + D + E + F < 120

#   - A is calculated from B and C 
#   - D is calculated from B and C
#   - C must be 0.8165*B < C < B
#   - E and F are calculated using the quadratic formula
#   - B must divide evenly into 200
# ----------

def problem_A():
    nva[0] = 0
    assignment = {}

    for B in range(1, 121):

        # B must divide evenly into 200
        if 200 % B != 0:
            continue

        if not assign("B", B, assignment):
            continue

        # C must satisfy: 0.8165*B < C < B
        c_start = int(0.8165 * B) + 1

        for C in range(c_start, B):
            if not assign("C", C, assignment):
                continue

            # C1: A = B^2 - C^2
            A = B**2 - C**2
            if not assign("A", A, assignment):
                continue

            # C3: D = B^2 - 3*A
            D = B**2 - 3 * A
            if not assign("D", D, assignment):
                continue

            # From C4:
            # (B-C)^2 = E*F*C - 1861
            # E*F*C = (B-C)^2 + 1861
            rightSide = (B - C)**2 + 1861

            # E*F must be an integer
            if rightSide % C != 0:
                continue

            EF_product = rightSide // C

            # From C2 and C5 we get a range for E+F
            # C2: E + F > B
            # C5: C + D + E + F < 120
            sum_min = B + 1
            sum_max = 119 - C - D

            if sum_min > sum_max:
                continue

            # For real roots, sum must be at least 2*sqrt(product)
            real_sum_min = math.ceil(2 * math.sqrt(EF_product))
            sum_start = max(sum_min, real_sum_min)

            # Try possible sums
            for s in range(sum_start, sum_max + 1):

                # If E+F = s and E*F = p,
                # then E and F are roots of x^2 - s*x + p = 0
                discriminant = s * s - 4 * EF_product

                if discriminant < 0:
                    continue

                sqrt_disc = math.isqrt(discriminant)

                # discriminant must be a perfect square
                if sqrt_disc * sqrt_disc != discriminant:
                    continue

                # roots must be integers
                if (s - sqrt_disc) % 2 != 0:
                    continue

                E = (s - sqrt_disc) // 2
                F = (s + sqrt_disc) // 2

                if not assign("E", E, assignment):
                    continue
                if not assign("F", F, assignment):
                    continue

                #check for C2
                if E + F <= B:
                    continue

                #check for C5
                if C + D + E + F >= 120:
                    continue

                yield assignment.copy()

    return False, None, nva[0]

# ----------
# PROBLEM B
#   C6:  (G+I)^3 = (H-A-1)^2
#   C7:  B*E*F = H*B - 200
#   C8:  (C+I)^2 = B*E*(G+1)
#   C9:  G+I < E
#   C10: D+H > 180
#   C11: J < H-C-G
#   C12: J > B*G + D + E + G

# Math shortcuts:
#   - H is calculated directly from C7
#   - G+I must be exactly 4, 9, or 16
#   - I = (G+I) - G  once G is chosen
#   - J is searched in a very tight range from C11 and C12
# ----------

def problem_B(solution_A):
    
    A = solution_A["A"]
    B = solution_A["B"]
    C = solution_A["C"]
    D = solution_A["D"]
    E = solution_A["E"]
    F = solution_A["F"]

    # Calculate H
    # C7: B*E*F = H*B - 200  =>  H = E*F + 200/B
    H = E * F + 200 // B
    if not in_domain(H):
        return
    
    nva[0] += 1

    #C10: D + H > 180
    if D + H <= 180:
        return 

    # --- Figure out required G+I value from C6 ---
    # delta = H - A - 1
    # We need: delta^2 = (G+I)^3
    # For integer solutions, G+I must be a perfect square m^2
    # Then delta = m^3 (or -m^3)
    # Valid options given domain [1,120]:
    #   G+I=4  => |delta|=8
    #   G+I=9  => |delta|=27
    #   G+I=16 => |delta|=64

    Range_GI = {8: 4, 27: 9, 64: 16}

    if abs(H-A-1) not in Range_GI:
        return

    GI = Range_GI[abs(H-A-1)]  # the exact value G+I must equal

    #C9: G+I < E
    if GI >= E:
        return

    for G in range(1, GI):
        I = GI - G

        if not (in_domain(G) and in_domain(I)):
            continue

        # Count G and I being assigned (2 variables)
        nva[0] += 2

        #C8: (C+I)^2 = B*E*(G+1)
        if (C + I) ** 2 != B * E * (G + 1):
            continue

        # C12: J > B*G + D + E + G   (lower bound)
        # C11: J < H - C - G         (upper bound)
        J_low  = B * G + D + E + G + 1  # +1 because strictly greater 
        J_high = H - C - G - 1          # -1 because strictly less 

        for J in range(J_low, J_high + 1):
            if not in_domain(J):
                continue

            nva[0] += 1

            all_ok = (
                (G + I) ** 3 == (H - A - 1) ** 2  and  # C6
                B * E * F    == H * B - 200         and  # C7
                (C + I) ** 2 == B * E * (G + 1)    and  # C8
                G + I < E                           and  # C9
                D + H > 180                         and  # C10
                J < H - C - G                       and  # C11
                J > B * G + D + E + G                    # C12
            )

            if all_ok:
                solution_B = dict(solution_A)
                solution_B.update({"G": G, "H": H, "I": I, "J": J})
                yield solution_B

# ----------
# PROBLEM C
#   C13: K*L*M = B*(B+5)
#   C14: F^3 = K^2 * M^2 * 10 + 331
#   C15: H*M^2 = J*K - 20
#   C16: J + L = I*L
#   C17: A + D + M = B*(F-2)

#   M from C17: M = B*(F-2) - A - D
#   K from C15: K = (H*M^2 + 20) / J
#   L from C16: L = J / (I-1)
#  verify only C13 and C14.
# ----------

def problem_C(solution_B):
    A = solution_B["A"]
    B = solution_B["B"]
    D = solution_B["D"]
    F = solution_B["F"]
    H = solution_B["H"]
    I = solution_B["I"]
    J = solution_B["J"]

    #Calculate M from C17
    # C17: A + D + M = B*(F-2)  =>  M = B*(F-2) - A - D
    M = B * (F-2) - A - D
    if not in_domain(M):
        return None
    nva[0] += 1

    # --- Calculate K from C15 ---
    # C15: H*M^2 = J*K - 20  =>  K = (H*M^2 + 20) / J
    k_numerator = H * M * M + 20
    if k_numerator % J != 0:
        return None
    K = k_numerator // J
    if not in_domain(K):
        return None
    nva[0] += 1

    # --- Calculate L from C16 ---
    # C16: J + L = I*L  =>  J = I*L - L = L*(I-1)  =>  L = J / (I-1)
    if I <= 1:
        return None
    if J % (I - 1) != 0:
        return None
    L = J // (I - 1)
    if not in_domain(L):
        return None
    nva[0] += 1 

    # --- Verify C13 and C14 ---
    # C13: K*L*M = B*(B+5)
    if K * L * M != B * (B + 5):
        return None

    # C14: F^3 = K^2 * M^2 * 10 + 331
    if F ** 3 != K * K * M * M * 10 + 331:
        return None

    solution_C = dict(solution_B)  # copy B solution
    solution_C.update({"K": K, "L": L, "M": M})
    return solution_C

# ----------
# SOLVER
# ----------
def solve_csp(problem):
    problem = problem.upper()

    nva[0] = 0 #Reset the nva counter

    #Problem A
    for sol_a in problem_A():

        if problem == 'A':
            return sol_a, nva[0]

        # Problem B - Needs A first
        for sol_b in problem_B(sol_a):

            if problem == 'B':
                return sol_b, nva[0]

            # Problem C - Needs B
            sol_c = problem_C(sol_b)
            if sol_c is not None:
                return sol_c, nva[0]

    return None, nva[0]


def verify(problem, sol):
    a = sol

    checks = [
        a["A"] == a["B"]**2 - a["C"]**2,
        a["E"] + a["F"] > a["B"],
        a["D"] == a["B"]**2 - 3*a["A"],
        (a["B"]-a["C"])**2 == a["E"]*a["F"]*a["C"]-1861,
        a["C"]+a["D"]+a["E"]+a["F"] < 120,
    ]

    if problem in ('B', 'C'):
        checks += [
            (a["G"]+a["I"])**3 == (a["H"]-a["A"]-1)**2,
            a["B"]*a["E"]*a["F"] == a["H"]*a["B"]-200,
            (a["C"]+a["I"])**2 == a["B"]*a["E"]*(a["G"]+1),
            a["G"]+a["I"] < a["E"],
            a["D"]+a["H"] > 180,
            a["J"] < a["H"]-a["C"]-a["G"],
            a["J"] > a["B"]*a["G"]+a["D"]+a["E"]+a["G"],
        ]

    if problem == 'C':
        checks += [
            a["K"]*a["L"]*a["M"] == a["B"]*(a["B"]+5),
            a["F"]**3 == a["K"]**2*a["M"]**2*10+331,
            a["H"]*a["M"]**2 == a["J"]*a["K"]-20,
            a["J"]+a["L"] == a["I"]*a["L"],
            a["A"]+a["D"]+a["M"] == a["B"]*(a["F"]-2),
        ]

    return all(checks)


def main():
    rows = []

    for p in ["A", "B", "C"]:
        solution, nva_count = solve_csp(p)
        if solution:
            if verify(p, solution):
                print(f"Problem {p}: all constraints passed")
            else:
                print(f"Problem {p}: FAILED")

            row = {"Problem": p}
            for var in ["A","B","C","D","E","F","G","H","I","J","K","L","M"]:
                row[var] = solution.get(var, "")
            row["nva"] = nva_count
            rows.append(row)

    # Write to CSV
    filename = "results.csv"
    fields = ["Problem","A","B","C","D","E","F","G","H","I","J","K","L","M","nva"]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for row in rows:
            writer.writerow([row.get(col, "") for col in fields])

    print(f"Results saved to {filename}")


if __name__ == "__main__":
    main()