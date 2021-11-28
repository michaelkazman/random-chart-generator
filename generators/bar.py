import numpy as np

parameters = {
    'x_range': (-5, 5),
    'height_range': (0, 50),
    'features_range': (4, 5 * 2) # the 2nd argument of features_range should be 2 * x_range
}

def generate_data():
    # get features
    features = np.random.randint(*parameters['features_range'])

    # generate x and y
    X = np.linspace(*parameters['x_range'], features)
    y = [np.random.uniform(*parameters['height_range']) for _ in range (0, features)]
    
    # random chance of correlation
    correlation = np.random.choice(['none', 'positive', 'negative'])
    
    if (correlation == 'positive' or correlation == 'negative'):
        y = np.sort(y)
        if (correlation == "negative"):
            # reverse sorted array
            y = y[::-1]
    
    # random chance of graph being vertical/horizontal bar chart
    is_vertical = bool(np.random.randint(2))

    return (X, y, is_vertical)

