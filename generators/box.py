import numpy as np
import pandas as pd

parameters = {
    'num_boxes_range': (2, 7),
    'num_samples_range': (70, 100),
}

def generate_data():
    # generate values based on hyperparameters
    num_boxes = np.random.randint(*parameters['num_boxes_range'])
    num_samples = np.random.randint(*parameters['num_samples_range'])

    # create df
    groups = list(map(str, range(num_boxes)))
    X = np.random.choice(groups, num_samples)
    y = np.random.randn(num_samples)

    # X is needed to generate whiskers in certain visualization libraries
    return {
        'X': X,
        'y': y,
        'num_repeats': num_boxes,
    }