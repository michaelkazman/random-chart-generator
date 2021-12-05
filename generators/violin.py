import numpy as np
import pandas as pd

parameters = {
    'num_violins_range': (2, 7),
    'num_samples_range': (60, 120),
    'y_data_range': (40, 120),
}

def generate_data():
    # generate random data
    num_violins = np.random.randint(*parameters['num_violins_range'])
    num_samples = np.random.randint(*parameters['num_samples_range'])

    # generate names for violins ('A', 'B', etc.)
    groups= [chr(65 + i) for i in range (0, num_violins)] 

    # select random normal values
    X = [np.random.choice(groups) for _ in range(num_samples)]
    y = [np.random.normal(*parameters['y_data_range']) for _ in range(num_samples)]

    return {
        'X': X,
        'y': y,
    }