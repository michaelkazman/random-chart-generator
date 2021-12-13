import numpy as np
import numpy as np
import scipy.stats as st

parameters = {
    "num_points": 500,
    "origin": (0, 0),
    "covariance_range": [-5, 5],
    "x_range": [-2, 2],
    "y_range": [-2, 2],
    "smoothness": 100j,
}

def generate_data():
    # generate random data
    cov = [
        np.random.uniform(parameters.get('covariance_range'), 2),
        np.random.uniform(parameters.get('covariance_range'), 2),
    ]
    data = np.random.multivariate_normal(
        parameters.get('origin'),
        cov,
        parameters.get('num_points'),
        check_valid='ignore',
    )

    # compute kernel density estimate
    XX, yy = data[:, 0], data[:, 1]
    X, y = np.mgrid[
        parameters.get("x_range")[0]:parameters.get("x_range")[1]:parameters.get("smoothness"),
        parameters.get("y_range")[0]:parameters.get("y_range")[1]:parameters.get("smoothness"),
    ]
    positions = np.vstack([X.ravel(), y.ravel()])
    kernel = st.gaussian_kde(np.vstack([XX, yy]))
    z = np.reshape(kernel(positions).T, X.shape)
    z[z==0] = 0.01
    
    return {
        'X': X,
        'y': y,
        'z': z
    }