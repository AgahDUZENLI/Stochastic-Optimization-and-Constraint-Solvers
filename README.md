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