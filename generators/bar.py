import numpy as np

from utils.creators import convert_numbers_to_letters

parameters = {
    'x_range': (-5, 5),
    'height_range': (0, 50),
    'features_range': (4, 5 * 2), # the 2nd argument of features_range should be 2 * x_range
    'noise_range': (0, 0.15),
}

def generate_data():
    # get features
    features = np.random.randint(*parameters['features_range'])

    # generate x (rounded to two decimal places) and y
    X = np.around(np.linspace(*parameters['x_range'], features), decimals=2)
    y = [np.random.uniform(*parameters['height_range']) for _ in range (0, features)]
    
    # random chance of correlation
    correlation = np.random.choice(['none', 'positive', 'negative'])
    
    if (correlation == 'positive' or correlation == 'negative'):
        y = np.sort(y)
        if (correlation == 'negative'):
            # reverse sorted array
            y = y[::-1]
        
        # random noise level
        noise = np.random.uniform(*parameters['noise_range'], len(y))
        for i in range (0, len(y)):
            operation = np.random.choice([-1, 1])
            y[i] += operation * (y[i] * noise[i])
    
    # random chance of graph being vertical/horizontal bar chart
    is_vertical = bool(np.random.randint(2))

    bar_names = convert_numbers_to_letters(range(len(X)))

    return {
        'X': bar_names,
        'y': y,
        'is_vertical': is_vertical
    }

