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
    X = list(map(str, range(num_boxes)))
    y = np.random.randn(num_samples)
    g = np.random.choice(X, num_samples)
    df = pd.DataFrame(dict(y=y, group=g))
    
    # X is needed to generate whiskers in certain visualization libraries
    return (X, df)