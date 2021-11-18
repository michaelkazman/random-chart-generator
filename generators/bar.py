import numpy as np

parameters = {
    'x_range': (-5, 5),
    'height_range': (0, 50),
    # the 2nd argument of features_range should be 2 * x_range
    'features_range': (4, 5 * 2)
}

def get_parameter(parameter):
    return parameters[parameter]

def generate_data():
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
            # reverse sorted array
            y = y[::-1]

    return x, y

