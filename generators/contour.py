import numpy as np
import numpy as np
import plotnine as p9
from plotnine.data import faithful


parameters = {
    'start_range':  (0, 4),
    'stop_range':  (4, 10), # min should be based on start's max
    'features_range':  (4, 100), 
    'z_constant_range':  (5, 10),
}

def generate_data():
    # generate random x and y
    x_start = np.random.uniform(*parameters['start_range'])
    x_stop = np.random.uniform(*parameters['stop_range'])
    y_start = np.random.uniform(*parameters['start_range'])
    y_stop = np.random.uniform(*parameters['stop_range'])
    features = np.random.randint(*parameters['features_range'])

    # generate a mesh grid (as a basis for the contour)
    x = np.linspace(x_start, x_stop, features)
    y = np.linspace(y_start, y_stop, features)
    X, y = np.meshgrid(x, y)
    
    # calculate z based on x, y and random constants
    constant = np.random.randint(*parameters['z_constant_range'])
    z = np.sin(X) ** constant + np.cos(constant + y * X) * np.cos(X)

    return {
        'X': faithful['eruptions'].to_numpy(),
        'y': faithful['waiting'].to_numpy(),
        'z': z,
    }