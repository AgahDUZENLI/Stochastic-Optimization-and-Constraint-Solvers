# RHCR2 Optimization Tool

## Description

This program implements the **Randomized Hill Climbing with Resampling (RHCR2)** algorithm to find the local (and potentially global) minimum of the "Frog" function. The algorithm operates in three distinct stages, reducing the neighborhood search radius ($z$) at each stage to refine the solution.

## Prerequisites

* **Python 3.x**
* **NumPy** library

If you do not have NumPy installed, you can install it via pip:

```bash
pip install numpy

```

## File Structure

* `rhcr2.py`: The main source code containing the `frog` function, the `RHC` procedure, and the `RHCR2` three stage wrapper.
* `README.md`: This file.

## How to Run the Program

1. Open your terminal or command prompt.
2. Navigate to the directory containing the source code.
3. Run the script using the following command:
```bash
python rhcr2.py

```

## Program Output

The program prints a formatted table to the console containing the following columns:

1. **p/z/sp/seed**: The parameters used for each run:
* **p**: Number of neighbors.
* **z**: Initial search radius.
* **sp**: Starting $(x, y)$ coordinates.
* **seed**: The random seed for reproducibility.


2. **Solutions Searched (1,2,3,Sum)**: A breakdown of function calls for Stage 1, Stage 2, Stage 3, and the final total sum.
3. **Results f(sol1), f(sol2), f(sol3)**: The objective function value $f(x,y)$ found at the conclusion of each of the three stages.

## Implementation Details

* **The Frog Function**: A non-convex mathematical function designed to test the algorithm's ability to navigate complex terrain with multiple local minima.
* **Stage-wise Zooming**:
* **Stage 1**: Search radius = $z$
* **Stage 2**: Search radius = $z/20$
* **Stage 3**: Search radius = $z/400$


* **Clipping**: All generated neighbors are clipped to the range $[-512, 512]$ to ensure the search stays within the defined problem bounds.

---

# CSP Solver

## Description
This program solves three hierarchically organized Constraint Satisfaction Problems (CSPs) involving variables **A through M**, each taking integer values in the domain **{1,...,120}**.

The problems are structured hierarchically:

- **Problem A** solves constraints **C1–C5** using variables A–F.
- **Problem B** extends a valid solution of Problem A by solving constraints **C6–C12** with additional variables G–J.
- **Problem C** extends a valid solution of Problem B by solving constraints **C13–C17** with additional variables K–M.

The program stops as soon as a valid solution is found and does **not search for additional solutions**, as required.

---

# Features

- Solves **Problem A, B, or C** using the same solver.
- Uses **mathematical pre-analysis** to reduce the search space.
- Uses a **hierarchical solving strategy (A → B → C)**.
- Tracks the number of variable assignments using the counter **nva**.
- Outputs the solution and **nva value** to a CSV file.
- Includes a **verification function** to ensure all constraints are satisfied.

---

# Requirements

- Python **3.8+**
- No external libraries are required (only standard Python libraries).

---

# How to Run

1. Place the solver file (for example `csp_solver.py`) in a folder.

2. Open a terminal in that folder.

3. Run the program using: python csp_solver.py

The program will automatically solve:

- Problem A
- Problem B
- Problem C

and verify that all constraints are satisfied.

---

# Output

After running the program:

- A file named **`results.csv`** will be created.
- The file contains the solution for each problem and the final **nva** value.

Example structure:
Problem,A,B,C,D,E,F,G,H,I,J,K,L,M,nva
A, … values …
B, … values …
C, … values …

Empty fields correspond to variables not used in earlier problems.

---

# Program Structure

The program is organized into modular components:

### `problem_A()`
Solves the CSP for **variables A–F** using constraints C1–C5.

### `problem_B(solution_A)`
Extends a valid solution of Problem A to solve constraints **C6–C12**.

### `problem_C(solution_B)`
Extends a valid solution of Problem B to solve constraints **C13–C17**.

### `solve_csp(problem)`
Main solver interface that selects whether to solve: 
A
B
C

### `verify(problem, solution)`
Checks that all constraints for the requested problem are satisfied.

### `main()`
Runs the solver, verifies results, and writes the output to `results.csv`.

---

# nva Counter

The variable **nva (number of variable assignments)** counts how many times:

- a variable receives an initial value, or
- a variable’s value changes during the search.

This metric is used to measure the efficiency of the solver.

---

# Notes

- The solver uses **mathematical constraint reductions** to significantly reduce the search space.
- The hierarchical structure ensures that **Problem B builds on Problem A**, and **Problem C builds on Problem B**.
- The program is written in a modular way so that similar CSP problems could reuse the same structure by modifying the constraints.

---

# Author

Agah Düzenli  