import numpy as np
from utils.creators import convert_numbers_to_letters

parameters = {
    'num_violins_range': (2, 7),
    'num_samples_range': (60, 120),
    'y_data_range': (40, 120),
}

def generate_data():
    # generate random data
    num_violins = np.random.randint(*parameters.get('num_violins_range', ()))
    num_samples = np.random.randint(*parameters.get('num_samples_range', ()))

    # generate names for violins ('A', 'B', etc.)
    groups = convert_numbers_to_letters(range(num_violins))

    # select random normal values
    X = sorted([np.random.choice(groups) for _ in range(num_samples)])
    y = [np.random.normal(*parameters.get('y_data_range', ())) for _ in range(num_samples)]

    return {
        'X': X,
        'y': y,
        'num_repeats': num_violins,
    }