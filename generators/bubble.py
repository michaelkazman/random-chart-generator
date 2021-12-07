import numpy as np
from sklearn.datasets import make_regression

parameters = {
    'num_features' : 1, # required to ensure no negative dimensions occur
    'sample_range' : (30, 200),
    'tail_strength_range' : (0, 0.7),
    'noise_range' : (1, 80),
    'random_noise_range' : (200, 400),
    'log_random_noise_range': (0, 2),
    'log_base_range': (1.2, 2.0),
    'bubble_size_range': (5, 20),
    'max_generation_attempts': 3,
}

def generate_data():
    # get parameters
    noise_level = np.random.uniform(*parameters['noise_range']) 
    random_noise_level = np.random.uniform(*parameters['random_noise_range']) # for no correlation
    num_samples = np.random.randint(*parameters['sample_range'])
    num_features = parameters['num_features']
    tail_strength = np.random.uniform(*parameters['tail_strength_range'])
    correlation = np.random.choice(['none', 'log_negative', 'log_positive', 'negative', 'positive'])

    # base correlation
    noise = random_noise_level if correlation == 'none' else noise_level
    X, y = make_regression(n_samples=num_samples, n_features=num_features, noise=noise, tail_strength=tail_strength)
    
    # log correlation uses different algorithm for y values
    # and can sometimes generate invalid values (which need to be filtered out)
    if (correlation == 'log_positive' or correlation == 'log_negative'):
        # remove and replace all invalid x data (i.e. values where x <= 0)
        X_valid, attempts = filter_invalid_samples(X), 0
        while (attempts < parameters['max_generation_attempts'] or len(X_valid) != len(X)):
            # generate as many samples as needed
            num_invalid = len(X) - len(X_valid)
            X_new, _ = make_regression(n_samples=num_invalid, n_features=num_features, noise=noise, tail_strength=tail_strength)
            # filter out the invalid ones and iterate
            X_new = filter_invalid_samples(X_new)
            X_valid = np.concatenate((X_valid, X_new))
            attempts += 1
        X = X_valid
        y = calculate_log_y(X) 

    # negate correlation (if needed)
    y = -y if (correlation == 'negative' or correlation == 'log_negative') else y

    # calculate bubble sizes
    bubble_size = np.random.uniform(*parameters['bubble_size_range'], X.shape)

    # convert data to be one dimensional
    X = X.flatten()
    y = y.flatten()
    bubble_size = bubble_size.flatten()

    return {
        'X': X,
        'y': y,
        'bubble_size': bubble_size,
    }

def filter_invalid_samples(X):
    return  X[X > 0]

def calculate_log_y(X):   
    # logarithmic with custom base (log_1.2(x) to log_2.0(x))
    log_base = np.random.uniform(*parameters['log_base_range'])
    y = np.log(X) / np.log(log_base)

    # add noise to y
    log_noise_level = np.random.uniform(*parameters['log_random_noise_range'])
    noise = np.random.normal(0, log_noise_level, y.shape)
    y = (y + noise)

    return y

