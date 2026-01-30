# data/sample_data.py

import numpy as np

class HajjData:
    def __init__(self):
        # Sample 1: Small example (2 ports, 2 hotels) - This is the one from the problem description
        self.small_example = {
            'ports': {
                'p1': 60,  # Number of pilgrims at port 1
                'p2': 40   # Number of pilgrims at port 2
            },
            'hotels': {
                'h1': 80,  # Capacity of hotel 1
                'h2': 40   # Capacity of hotel 2
            },
            'bus_capacity': 50,
            'costs': {
                ('p1', 'h1'): 100,  # Cost from port 1 to hotel 1
                ('p1', 'h2'): 80,   # Cost from port 1 to hotel 2
                ('p2', 'h1'): 90,   # Cost from port 2 to hotel 1
                ('p2', 'h2'): 120   # Cost from port 2 to hotel 2
            }
        }

        # Sample 2: Medium example (3 ports, 4 hotels)
        self.medium_example = {
            'ports': {
                'Jeddah_Airport': 200,    # Jeddah Airport
                'Medina_Airport': 150,    # Medina Airport
                'Land_Border': 100        # Land border entry
            },
            'hotels': {
                'Makkah_H1': 150,         # Makkah Hotel 1
                'Makkah_H2': 100,         # Makkah Hotel 2
                'Madinah_H1': 120,        # Madinah Hotel 1
                'Madinah_H2': 80          # Madinah Hotel 2
            },
            'bus_capacity': 50,
            'costs': {
                ('Jeddah_Airport', 'Makkah_H1'): 150,
                ('Jeddah_Airport', 'Makkah_H2'): 160,
                ('Jeddah_Airport', 'Madinah_H1'): 300,
                ('Jeddah_Airport', 'Madinah_H2'): 310,
                ('Medina_Airport', 'Makkah_H1'): 280,
                ('Medina_Airport', 'Makkah_H2'): 290,
                ('Medina_Airport', 'Madinah_H1'): 100,
                ('Medina_Airport', 'Madinah_H2'): 110,
                ('Land_Border', 'Makkah_H1'): 200,
                ('Land_Border', 'Makkah_H2'): 210,
                ('Land_Border', 'Madinah_H1'): 250,
                ('Land_Border', 'Madinah_H2'): 260
            }
        }

        # Sample 3: Large example (5 ports, 6 hotels)
        self.large_example = {
            'ports': {
                'Jeddah_Int_Airport': 300,    # Jeddah International Airport
                'Medina_Int_Airport': 250,    # Medina International Airport
                'Taif_Airport': 150,          # Taif Airport
                'Yanbu_Seaport': 100,         # Yanbu Seaport
                'Northern_Border': 200         # Northern land border
            },
            'hotels': {
                'Makkah_Premium': 200,        # Makkah Premium Hotel
                'Makkah_Standard1': 150,      # Makkah Standard Hotel 1
                'Makkah_Standard2': 150,      # Makkah Standard Hotel 2
                'Madinah_Premium': 180,       # Madinah Premium Hotel
                'Madinah_Standard1': 120,     # Madinah Standard Hotel 1
                'Madinah_Standard2': 120      # Madinah Standard Hotel 2
            },
            'bus_capacity': 50,
            'costs': {
                # Costs from Jeddah International Airport
                ('Jeddah_Int_Airport', 'Makkah_Premium'): 180,
                ('Jeddah_Int_Airport', 'Makkah_Standard1'): 160,
                ('Jeddah_Int_Airport', 'Makkah_Standard2'): 160,
                ('Jeddah_Int_Airport', 'Madinah_Premium'): 350,
                ('Jeddah_Int_Airport', 'Madinah_Standard1'): 330,
                ('Jeddah_Int_Airport', 'Madinah_Standard2'): 330,
                
                # Costs from Medina International Airport
                ('Medina_Int_Airport', 'Makkah_Premium'): 320,
                ('Medina_Int_Airport', 'Makkah_Standard1'): 300,
                ('Medina_Int_Airport', 'Makkah_Standard2'): 300,
                ('Medina_Int_Airport', 'Madinah_Premium'): 120,
                ('Medina_Int_Airport', 'Madinah_Standard1'): 100,
                ('Medina_Int_Airport', 'Madinah_Standard2'): 100,
                
                # Costs from Taif Airport
                ('Taif_Airport', 'Makkah_Premium'): 150,
                ('Taif_Airport', 'Makkah_Standard1'): 130,
                ('Taif_Airport', 'Makkah_Standard2'): 130,
                ('Taif_Airport', 'Madinah_Premium'): 400,
                ('Taif_Airport', 'Madinah_Standard1'): 380,
                ('Taif_Airport', 'Madinah_Standard2'): 380,
                
                # Costs from Yanbu Seaport
                ('Yanbu_Seaport', 'Makkah_Premium'): 380,
                ('Yanbu_Seaport', 'Makkah_Standard1'): 360,
                ('Yanbu_Seaport', 'Makkah_Standard2'): 360,
                ('Yanbu_Seaport', 'Madinah_Premium'): 180,
                ('Yanbu_Seaport', 'Madinah_Standard1'): 160,
                ('Yanbu_Seaport', 'Madinah_Standard2'): 160,
                
                # Costs from Northern Border
                ('Northern_Border', 'Makkah_Premium'): 450,
                ('Northern_Border', 'Makkah_Standard1'): 430,
                ('Northern_Border', 'Makkah_Standard2'): 430,
                ('Northern_Border', 'Madinah_Premium'): 250,
                ('Northern_Border', 'Madinah_Standard1'): 230,
                ('Northern_Border', 'Madinah_Standard2'): 230
            }
        }

    def get_problem_matrices(self, example='small'):
        """
        Convert the dictionary format to matrices for optimization
        Args:
            example: 'small', 'medium', or 'large'
        Returns:
            A, b, c (constraint matrices and cost vector)
        """
        if example == 'small':
            data = self.small_example
        elif example == 'medium':
            data = self.medium_example
        else:
            data = self.large_example

        ports = list(data['ports'].keys())
        hotels = list(data['hotels'].keys())
        n_ports = len(ports)
        n_hotels = len(hotels)
        n_variables = n_ports * n_hotels

        # Create cost vector
        c = np.zeros(n_variables)
        for i, port in enumerate(ports):
            for j, hotel in enumerate(hotels):
                c[i * n_hotels + j] = data['costs'][(port, hotel)]

        # Create constraint matrix A and vector b
        # Constraints:
        # 1. Port capacity constraints
        # 2. Hotel capacity constraints
        # 3. Bus capacity constraints
        A_port = np.zeros((n_ports, n_variables))
        A_hotel = np.zeros((n_hotels, n_variables))
        A_bus = np.eye(n_variables)  # Bus capacity constraints

        b_port = np.zeros(n_ports)
        b_hotel = np.zeros(n_hotels)
        b_bus = np.ones(n_variables) * data['bus_capacity']

        # Fill port constraints
        for i, port in enumerate(ports):
            for j in range(n_hotels):
                A_port[i, i * n_hotels + j] = 1
            b_port[i] = data['ports'][port]

        # Fill hotel constraints
        for j, hotel in enumerate(hotels):
            for i in range(n_ports):
                A_hotel[j, i * n_hotels + j] = 1
            b_hotel[j] = data['hotels'][hotel]

        # Combine all constraints
        A = np.vstack([A_port, A_hotel, A_bus])
        b = np.concatenate([b_port, b_hotel, b_bus])

        return A, b, c
