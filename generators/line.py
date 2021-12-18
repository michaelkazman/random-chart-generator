import numpy as np
from utils.generators import generate_random_distribution, generate_midpoint_displacement

parameters = {
    'y_start_range':  (50, 400),
    'y_end_range':    (50, 400),
    'x_start_range':  (0, 1),
    'x_end_range':  (400, 1000),
    'rough_range':  (0.7, 1.5),
    'vertical_displacement_range':  (50, 150),
    'num_iterations_range': (2, 4),
    'num_samples_range': (4, 15),
    'layers_range':  (1, 4),
}

def generate_data():
    # get distribution type (random)
    data_distributions = {
        'random': generate_random_distribution,
        'midpoint': generate_midpoint_displacement,
    }
    distribution = np.random.choice(list(data_distributions.keys()))

    # get graph's unique random values
    X, y = data_distributions[distribution](parameters)
    return {
        'X': X,
        'y': y,
        'distribution': distribution,
        'num_repeats': y.shape[0]
    }