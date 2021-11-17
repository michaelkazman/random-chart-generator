import numpy as np
from sklearn.datasets import make_regression

parameters = {
    'num_features': 1,
    'sample_range': (30, 300),
    'noise_range': (1, 70),
    'random_noise_range': (200, 400),
    'tail_strength': 0.5,
}

def get_parameter(parameter):
    return parameters[parameter]

def generate_scatter_data():
    # generate hyperparameters
    noise = np.random.uniform(*get_parameter('noise_range'))
    random_noise = np.random.uniform(*get_parameter('random_noise_range')) # for no correlation
    num_samples = np.random.randint(*get_parameter('sample_range'))
    correlation = np.random.choice(["none", "positive", "negative"])

    # calculate data points from random linear regression model
    X, y = make_regression(
        n_samples=num_samples,
        n_features=get_parameter('num_features'),
        noise=(random_noise if correlation == 'none' else noise),
        tail_strength=get_parameter('tail_strength')
    )

    # y correlation is flipped if generating a negative scatter
    y = -y if correlation == 'negative' else y

    return X, y