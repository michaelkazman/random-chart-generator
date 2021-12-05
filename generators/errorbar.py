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
    'error_max_threshold': 0.15,
    'error_min_threshold': 0.05,
}

def generate_data():
    # pick a random distribution type
    data_distributions = {
        'midpoint': generate_midpoint_displacement,
        'random': generate_random_distribution
    }
    distribution = np.random.choice(list(data_distributions.keys()))

    # generate data
    X, y = data_distributions[distribution](parameters)

    # generate error values for each datapoint
    error_bar_max = calculate_y_lim(y.flatten())
    error_bar_min = calculate_y_lim(y.flatten(), threshold_name='error_min_threshold')
    y_error = [np.random.uniform(error_bar_min, error_bar_max, size=X.shape) for _ in range(len(y))]
    return {
        'X': X,
        'y': y,
        'y_error': y_error,
    }

def calculate_y_lim(y, threshold_name='error_max_threshold'):
    # create violin
    height_limit = (np.max(y) - np.min(y)) * parameters[threshold_name]
    return height_limit