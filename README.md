# Hajj Pilgrim Transportation Optimization (AI382 Project)

This project implements an optimization solution for the **Hajj Pilgrim Transportation and Accommodation problem** using **Linear Programming (LP)** and **Integer Programming (IP)** techniques.

The solution is implemented **from scratch in Python**, without using external optimization libraries, and applies a **Branch and Bound** algorithm to solve the integer programming formulation.

This project was developed as part of the **AI382 – Artificial Intelligence II** course.

---

## Problem Overview

During Hajj, pilgrims arrive through multiple ports and must be transported efficiently to available hotels with limited capacity.  
The goal of this project is to **minimize transportation cost** while satisfying:

- Port supply constraints  
- Hotel capacity constraints  
- Bus capacity constraints  
- Integer decision variables (number of buses / pilgrims transported)

---

## Optimization Techniques Used

### Linear Programming (LP)
- Solved using **vertex enumeration**
- Computes feasible region intersections
- Evaluates objective function at extreme points

### Integer Programming (IP)
- Solved using **Branch and Bound**
- Recursively splits the problem into subproblems
- Ensures integer feasibility of solutions

---

## Project Structure

```

Ai382 Project/
│
├── main.py            # Problem formulation and execution
├── optimizer.py       # LP and IP solvers (Branch and Bound)
├── data/
│   └── sample_data.py # Input data definitions
└── README.md

````

---

## Requirements
- Python 3.7 or higher
- NumPy
- Matplotlib

Install required packages:
```bash
pip install numpy matplotlib
````

---

## How to Run

1. Navigate to the project directory:

```bash
cd Ai382\ Project
```

2. Run the main program:

```bash
python main.py
```

The program will:

* Solve the LP formulation
* Apply Branch and Bound for the IP solution
* Display results and visualizations (when applicable)

---

## Problem Parameters (Sample Data)

* Ports:

  * p1: 60 pilgrims
  * p2: 40 pilgrims
* Hotels:

  * h1 capacity: 80 pilgrims
  * h2 capacity: 40 pilgrims
* Bus capacity: 50 pilgrims per bus

### Transportation Costs (SAR)

* p1 → h1: 100
* p1 → h2: 80
* p2 → h1: 90
* p2 → h2: 120

---

## Features

* Custom Linear Programming solver
* Integer Programming via Branch and Bound
* Constraint intersection detection
* Feasible region visualization (2D cases)
* Modular and well-structured code

---

## Group Contribution

This was a **group project**, and all members contributed collaboratively.

* **Roaa Alhejaili**

  * LP and IP problem formulation
  * Branch and Bound implementation
  * Core algorithm design and integration

* **Team Members**

  * Data modeling and validation
  * Testing and result verification
  * Documentation and presentation support

All members participated in discussions, debugging, and final review.

---

## Limitations

* Designed for small-to-medium scale problems
* Visualization limited to 2D cases
* No real-time or large-scale data integration

---

## Future Improvements

* Support higher-dimensional LP visualization
* Add real-world data input
* Improve performance for larger problem sizes
* Extend to multi-stage transportation planning

---

## Course Information

Course: **AI382 – Artificial Intelligence II**
Institution: **Prince Mugrin University**

---

## License

This project is developed for educational purposes and may be freely used or modified.

```

---

ng this repo that highlights *optimization + algorithms* without overselling.
```
