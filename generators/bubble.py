import numpy as np
from sklearn.datasets import make_regression

parameters = {
    'num_features' : 1,
    'sample_range' : (30, 200),
    'tail_strength_range' : (0, 0.7),
    'noise_range' : (1, 60),
    'random_noise_range' : (200, 400),
    'log_random_noise_range': (0, 2),
    'log_base_range': (1.2, 2.0),
    'bubble_size_range': (5, 20)
}

def generate_data():
    # get noise levels (random)
    noise_level = np.random.uniform(*parameters['noise_range']) 
    random_noise_level = np.random.uniform(*parameters['random_noise_range']) # for no correlation
    num_samples = np.random.randint(*parameters['sample_range'])
    num_features = parameters['num_features']
    tail_strength = np.random.uniform(*parameters['tail_strength_range'])
    # correlation = np.random.choice(['none', 'log_negative', 'log_positive', 'negative', 'positive'])
    correlation = np.random.choice(['log_negative'])

    # base correlation
    noise = random_noise_level if correlation == 'none' else noise_level
    X, y = make_regression(n_samples=num_samples, n_features=num_features, noise=noise, tail_strength=tail_strength)
    
    # log correlation uses different algorithm for y values 
    if (correlation == 'log_positive' or correlation == 'log_negative'):
        y = calculate_log_y(X, correlation)

    # negate correlation (if needed)
    y = -y if (correlation == 'negative' or correlation == 'log_negative') else y

    # calcualte bubble sizes
    bubble_size = np.random.uniform(*parameters['bubble_size_range'], X.shape)

    # convert data to be one dimensional
    X = X.flatten()
    y = y.flatten()
    bubble_size = bubble_size.flatten()

    print(X.shape, y.shape, correlation)

    return (X, y, bubble_size)

def calculate_log_y(X, correlation):
    # clip x values to avoid undefined errors
    if (correlation == 'log_positive'):
        X.clip(0.0001)
    
    # logarithmic with custom base (log_1.2(x) to log_2.0(x))
    log_base = np.random.uniform(*parameters['log_base_range'])
    y = np.log(X) / np.log(log_base)

    # add noise to y
    log_noise_level = np.random.uniform(*parameters['log_random_noise_range'])
    noise = np.random.normal(0, log_noise_level, y.shape)
    y = (y + noise)

    return y

