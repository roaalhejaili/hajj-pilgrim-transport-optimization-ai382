# main.py
import numpy as np
import matplotlib.pyplot as plt
from optimizer import Optimizer
from data.sample_data import HajjData
import time
from datetime import datetime

class HajjOptimizationSystem:
    def __init__(self):
        self.optimizer = Optimizer()
        self.hajj_data = HajjData()
        
    def format_cost(self, cost):
        """Format cost with thousands separator and currency"""
        return f"{cost:,.2f} SAR"
    
    def create_solution_report(self, example_size, optimal_point, optimal_value, execution_time, data):
        """Create a detailed solution report"""
        ports = list(data['ports'].keys())
        hotels = list(data['hotels'].keys())
        
        report = []
        report.append("\n" + "="*80)
        report.append(f"HAJJ OPTIMIZATION REPORT - {example_size.upper()} EXAMPLE")
        report.append("="*80)
        
        # Summary statistics
        report.append("\nSUMMARY:")
        report.append(f"Total Cost: {self.format_cost(optimal_value)}")
        report.append(f"Execution Time: {execution_time:.2f} seconds")
        report.append(f"Number of Ports: {len(ports)}")
        report.append(f"Number of Hotels: {len(hotels)}")
        
        # Detailed allocation
        report.append("\nDETAILED ALLOCATION:")
        report.append("-"*80)
        report.append(f"{'From Port':<20} {'To Hotel':<20} {'Pilgrims':<10} {'Cost/Pilgrim':<15} {'Total Cost'}")
        report.append("-"*80)
        
        idx = 0
        total_pilgrims = 0
        for i, port in enumerate(ports):
            for j, hotel in enumerate(hotels):
                pilgrims = int(optimal_point[idx])
                if pilgrims > 0:
                    cost_per_pilgrim = data['costs'][(port, hotel)]
                    total_cost = pilgrims * cost_per_pilgrim
                    report.append(
                        f"{port:<20} {hotel:<20} {pilgrims:<10} "
                        f"{self.format_cost(cost_per_pilgrim):<15} {self.format_cost(total_cost)}"
                    )
                    total_pilgrims += pilgrims
                idx += 1
        
        report.append("-"*80)
        report.append(f"Total Pilgrims: {total_pilgrims}")
        report.append(f"Average Cost per Pilgrim: {self.format_cost(optimal_value/total_pilgrims)}")
        
        # Capacity utilization
        report.append("\nCAPACITY UTILIZATION:")
        report.append("-"*80)
        report.append("PORTS:")
        for port, capacity in data['ports'].items():
            used = sum(int(optimal_point[i * len(hotels) + j]) 
                      for i, p in enumerate(ports) if p == port 
                      for j in range(len(hotels)))
            utilization = (used / capacity) * 100
            report.append(f"{port:<20} {used:>5}/{capacity:<5} ({utilization:>6.2f}%)")
        
        report.append("\nHOTELS:")
        for hotel, capacity in data['hotels'].items():
            used = sum(int(optimal_point[i * len(hotels) + j]) 
                      for i in range(len(ports)) 
                      for j, h in enumerate(hotels) if h == hotel)
            utilization = (used / capacity) * 100
            report.append(f"{hotel:<20} {used:>5}/{capacity:<5} ({utilization:>6.2f}%)")
        
        return "\n".join(report)

    def solve_and_visualize(self, example_size='small'):
        """
        Solve the Hajj problem and create visualizations
        """
        # Get data for the specified example
        if example_size == 'small':
            data = self.hajj_data.small_example
        elif example_size == 'medium':
            data = self.hajj_data.medium_example
        else:
            data = self.hajj_data.large_example
            
        # Get optimization matrices
        A, b, c = self.hajj_data.get_problem_matrices(example_size)
        constraints = {'A': A, 'b': b}
        
        # Solve the problem and measure execution time
        start_time = time.time()
        optimal_point, optimal_value = self.optimizer.optimizerIPBB(constraints, c)
        execution_time = time.time() - start_time
        
        # Generate report
        report = self.create_solution_report(example_size, optimal_point, optimal_value, 
                                          execution_time, data)
        print(report)
        
        # Create visualizations
        self.create_visualizations(example_size, data, optimal_point)
        
        # Save report to file
        self.save_report(report, example_size)

    def create_visualizations(self, example_size, data, optimal_point):
        """
        Create visualizations for the solution
        """
        ports = list(data['ports'].keys())
        hotels = list(data['hotels'].keys())
        
        # 1. Port to Hotel Flow Diagram
        plt.figure(figsize=(12, 8))
        plt.title(f'Pilgrim Flow Diagram - {example_size.upper()} Example')
        
        # Position ports on the left and hotels on the right
        port_positions = {port: (0, i) for i, port in enumerate(ports)}
        hotel_positions = {hotel: (1, i) for i, hotel in enumerate(hotels)}
        
        # Plot points
        for port, (x, y) in port_positions.items():
            plt.plot(x, y, 'bo', markersize=10, label='Ports' if port == ports[0] else "")
            plt.text(x-0.1, y, port, horizontalalignment='right')
            
        for hotel, (x, y) in hotel_positions.items():
            plt.plot(x, y, 'rs', markersize=10, label='Hotels' if hotel == hotels[0] else "")
            plt.text(x+0.1, y, hotel, horizontalalignment='left')
            
        # Plot flows
        idx = 0
        for i, port in enumerate(ports):
            for j, hotel in enumerate(hotels):
                pilgrims = int(optimal_point[idx])
                if pilgrims > 0:
                    plt.plot([port_positions[port][0], hotel_positions[hotel][0]],
                           [port_positions[port][1], hotel_positions[hotel][1]],
                           'g-', alpha=pilgrims/max(data['ports'].values()),
                           linewidth=pilgrims/max(data['ports'].values())*5)
                idx += 1
                
        plt.legend()
        plt.grid(True)
        plt.axis('off')
        plt.savefig(f'results/flow_diagram_{example_size}.png')
        plt.close()
        
        # 2. Capacity Utilization Bar Chart
        plt.figure(figsize=(12, 6))
        plt.title(f'Capacity Utilization - {example_size.upper()} Example')
        
        # Prepare data for plotting
        locations = list(ports) + list(hotels)
        capacities = [data['ports'][p] for p in ports] + [data['hotels'][h] for h in hotels]
        used = []
        
        idx = 0
        for port in ports:
            port_used = sum(int(optimal_point[i * len(hotels) + j]) 
                          for i, p in enumerate(ports) if p == port 
                          for j in range(len(hotels)))
            used.append(port_used)
            
        for hotel in hotels:
            hotel_used = sum(int(optimal_point[i * len(hotels) + j]) 
                           for i in range(len(ports)) 
                           for j, h in enumerate(hotels) if h == hotel)
            used.append(hotel_used)
            
        x = range(len(locations))
        plt.bar(x, capacities, alpha=0.3, label='Capacity')
        plt.bar(x, used, alpha=0.7, label='Used')
        plt.xticks(x, locations, rotation=45, ha='right')
        plt.ylabel('Number of Pilgrims')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'results/capacity_utilization_{example_size}.png')
        plt.close()

    def save_report(self, report, example_size):
        """Save the solution report to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'results/hajj_optimization_report_{example_size}_{timestamp}.txt'
        with open(filename, 'w') as f:
            f.write(report)

def main():
    """
    Main function to run the Hajj optimization system
    """
    # Create results directory if it doesn't exist
    import os
    if not os.path.exists('results'):
        os.makedirs('results')
        
    # Initialize the optimization system
    system = HajjOptimizationSystem()
    
    # Solve all three examples
    for size in ['small', 'medium', 'large']:
        print(f"\nProcessing {size} example...")
        system.solve_and_visualize(size)
        print(f"Results saved in the 'results' directory")

if __name__ == "__main__":
    main()