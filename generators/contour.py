import math
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

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

    # generate contour and get values
    (contour_X, contour_y, contour_z, x_text, y_text) = get_contour_data(X, y, z).values()
    
    return {
        'X': contour_X,
        'y': contour_y,
        'z': contour_z,
        'x_text': x_text,
        'y_text': y_text,
        'X_range': (X[0][0], X[-1][-1]),
        'y_range': (y[0][0], y[-1][-1]),
        'num_repeats': len(contour_X),
    }

'''
Title: get_contour_data()
Author: BR123
Date: 2016
Code version: N/A
Availability: https://docs.bokeh.org/en/latest/docs/gallery/histogram.html

The contour function below was used to plot values with matplotlib and scrape the generated plot values
'''

def get_contour_data(X, Y, Z):
    # generate matplotlib contour
    cs = plt.contour(X, Y, Z)
    X_points, y_points, z_points = [], [], np.array([])
    x_text, y_text = np.array([]), np.array([])

    # go through each contour level
    for i, level in enumerate(cs.collections):
        z = round(cs.get_array()[i], 2)

        # append points, text coordinates, text, and colour
        for path in level.get_paths():
            x, y = path.vertices[:, 0], path.vertices[:, 1]
            X_points.append(x.tolist())
            y_points.append(y.tolist())
            x_text = np.append(x_text, x[math.floor(len(x) / 2)])
            y_text = np.append(y_text, y[math.floor(len(y) / 2)])
            z_points = np.append(z_points, z)

    # create dict based on scraped data
    df = {
      'X': np.array(X_points, dtype=object),
      'y': np.array(y_points, dtype=object),
      'z': z_points,
      'x_text': x_text,
      'y_text': y_text,
    }

    return df