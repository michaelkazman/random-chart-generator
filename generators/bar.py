import numpy as np

parameters = {
    'size_range': (100, 1000),
    'bins_range': (4, 100),
    'mu_range': (0, 4),
    'sigma_range': (0, 1),
    'k_range': (1, 10),
    'lambda_range': (0.5, 1.5),
    'theta_range': (0.5, 2),
    'low_range': (0, 1),
    'high_range': (1, 2),
}

def get_parameter(parameter):
    return parameters[parameter]

def generate_bar_data():
    # get features
    features = np.random.randint(*get_parameter('features_range'))

    # generate x and y
    x = np.linspace(*get_parameter('x_range'), features)
    y = [np.random.uniform(*get_parameter('height_range')) for _ in range (0, features)]
    
    # random chance of correlation
    correlation = np.random.choice(["none", "positive", "negative"])
    
    if (correlation == 'positive' or correlation == 'negative'):
        y = np.sort(y)
        if (correlation == "negative"):
            y = y[::-1] # reverse sorted array

    return x, y

