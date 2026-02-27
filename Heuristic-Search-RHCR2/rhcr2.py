import numpy as np

def frog(x_vec):
    x, y = x_vec
    inner1 = np.sqrt(np.abs(x + y + 1))
    inner2 = np.sqrt(np.abs(y - x + 1))
    
    term1 = x * np.cos(inner1) * np.sin(inner2)
    term2 = (1 + y) * np.sin(inner1) * np.cos(inner2)
    return term1 + term2


#starting point, neighborhood size, number of neighbors
def RHC(sp, z, p):
    current_solution = np.array(sp)
    current_value = frog(current_solution)
    calls = 1

    best_neighbor = current_solution
    best_neighbor_value = current_value

    for a in range(p):
        movementVector = np.random.uniform(-z, z, size=2)
        neighbor = current_solution + movementVector
        neighbor = np.clip(neighbor, -512, 512) #Clip the range

        neighbor_value = frog(neighbor)
        calls += 1

        if neighbor_value < best_neighbor_value:
            best_neighbor_value = neighbor_value
            best_neighbor = neighbor
    
    return best_neighbor, best_neighbor_value, calls


def RHCR2(sp, z, p, seed):
    np.random.seed(seed)

    sol1, val1, c1 = RHC(sp,z,p)
    sol2, val2, c2 = RHC(sol1, z/20, p)
    sol3, val3, c3 = RHC(sol2, z/400, p)

    return (sol1, val1, c1), (sol2, val2, c2), (sol3, val3, c3)

if __name__ == "__main__":
    starting_points = [(-300, -400), (0, 0), (-222, -222), (-510, 400)]
    p_values = [120, 400]
    z_values = [9, 50]
    seeds = [42, 123]

    header = f"{'p/z/sp/seed':<25} | {'Solutions Searched (1,2,3,Sum)':<30} | {'Results f(sol1), f(sol2), f(sol3)':<35}"
    print(header)
    print("-" * len(header))

    def run_and_print(sp, z, p, seed, label=""):
        r1, r2, r3 = RHCR2(sp, z, p, seed)
        calls_str = f"{r1[2]}, {r2[2]}, {r3[2]}, {r1[2]+r2[2]+r3[2]}"
        results_str = f"{r1[1]:.5f}, {r2[1]:.5f}, {r3[1]:.5f}"
        id_str = f"p={p},z={z},{sp},{seed}"
        print(f"{id_str:<30} | {calls_str:<30} | {results_str:<35} {label}")

    for p in p_values:
        for z in z_values:
            for sp in starting_points:
                for seed in seeds:
                    run_and_print(sp, z, p, seed)

    # Run #33: Custom Choice
    print("-" * len(header))
    run_and_print((-510, 400), 125, 200, 123,)

    