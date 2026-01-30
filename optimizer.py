# optimizer.py
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

class Optimizer:
    def __init__(self):
        pass

    def intersections(self, constraints):
        """
        Find all feasible intersections between constraints
        Args:
            constraints: Dictionary containing A (coefficient matrix) and b (RHS vector)
        Returns:
            List of feasible intersection points
        """
        A = constraints['A']
        b = constraints['b']
        n = A.shape[1]  # number of variables
        points = []
        
        # Get all possible combinations of n constraints
        for idx in combinations(range(len(b)), n):
            A_sub = A[list(idx)]
            b_sub = b[list(idx)]
            
            try:
                # Solve the system of equations
                x = np.linalg.solve(A_sub, b_sub)
                
                # Check if point satisfies all constraints
                if all(np.dot(A, x) <= b + 1e-10):  # small tolerance for numerical errors
                    points.append(x)
            except np.linalg.LinAlgError:
                continue
                
        return np.array(points)

    def optimizerLP(self, constraints, cost):
        """
        Solve Linear Programming problem using Vertex Enumeration
        Args:
            constraints: Dictionary containing A and b
            cost: Cost vector c
        Returns:
            optimal_point, optimal_value
        """
        # Find all feasible vertices
        vertices = self.intersections(constraints)
        
        if len(vertices) == 0:
            return None, None
        
        # Evaluate cost at each vertex
        costs = np.dot(vertices, cost)
        
        # Find minimum cost and corresponding point
        min_idx = np.argmin(costs)
        return vertices[min_idx], costs[min_idx]

    def optimizerIPBB(self, constraints, cost):
        """
        Solve Integer Programming problem using Branch and Bound
        Args:
            constraints: Dictionary containing A and b
            cost: Cost vector c
        Returns:
            optimal_point, optimal_value
        """
        def branch_and_bound(constraints, cost, best_sol=None, best_val=float('inf')):
            # Solve LP relaxation
            sol, val = self.optimizerLP(constraints, cost)
            
            if sol is None:  # Infeasible
                return None, float('inf')
            
            if val >= best_val:  # Prune by bound
                return best_sol, best_val
            
            # Check if solution is integer
            if all(abs(x - round(x)) < 1e-10 for x in sol):
                return sol, val
            
            # Find first non-integer variable
            for i, x in enumerate(sol):
                if abs(x - round(x)) > 1e-10:
                    # Branch on this variable
                    floor_val = np.floor(x)
                    ceil_val = np.ceil(x)
                    
                    # Add new constraints for both branches
                    A_new = np.vstack([constraints['A'], [0] * i + [1] + [0] * (len(sol) - i - 1)])
                    
                    # Floor branch
                    b_floor = np.append(constraints['b'], floor_val)
                    constraints_floor = {'A': A_new, 'b': b_floor}
                    sol_floor, val_floor = branch_and_bound(constraints_floor, cost, best_sol, best_val)
                    
                    if val_floor < best_val:
                        best_sol = sol_floor
                        best_val = val_floor
                    
                    # Ceil branch
                    b_ceil = np.append(constraints['b'], -ceil_val)
                    constraints_ceil = {'A': A_new, 'b': b_ceil}
                    sol_ceil, val_ceil = branch_and_bound(constraints_ceil, cost, best_sol, best_val)
                    
                    if val_ceil < best_val:
                        best_sol = sol_ceil
                        best_val = val_ceil
                    
                    break
            
            return best_sol, best_val
        
        return branch_and_bound(constraints, cost)

    def plot_2d_problem(self, constraints, cost, solution=None):
        """
        Plot the feasible region and solution for 2D problems
        """
        A = constraints['A']
        b = constraints['b']
        
        # Create a grid of points
        x = np.linspace(-10, 100, 1000)
        y = np.linspace(-10, 100, 1000)
        X, Y = np.meshgrid(x, y)
        
        # Plot feasible region
        plt.figure(figsize=(10, 8))
        for i in range(len(b)):
            if np.abs(A[i, 1]) < 1e-10:  # Vertical line
                plt.axvline(x=b[i]/A[i, 0], color='r', alpha=0.3)
            else:
                plt.plot(x, (b[i] - A[i, 0]*x)/A[i, 1], 'r', alpha=0.3)
        
        # Shade feasible region
        for i in range(len(x)):
            for j in range(len(y)):
                point = np.array([X[i,j], Y[i,j]])
                if all(np.dot(A, point) <= b):
                    plt.plot(X[i,j], Y[i,j], 'b.', alpha=0.1)
        
        if solution is not None:
            plt.plot(solution[0], solution[1], 'g*', markersize=15, label='Optimal Solution')
        
        plt.grid(True)
        plt.legend()
        plt.xlabel('x1')
        plt.ylabel('x2')
        plt.title('Feasible Region and Optimal Solution')
        plt.show()