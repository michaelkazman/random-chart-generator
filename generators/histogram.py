import numpy as np

parameters = {
    'size_range': (300, 1000),
    'bins_range': (7, 100),
    'mu_range': (0, 4),
    'sigma_range': (0.01, 0.5),
    'k_range': (1, 10),
    'lambda_range': (0.5, 1.5),
    'theta_range': (0.5, 2),
    'low_range': (0.2, 1),
    'high_range': (1, 2),
}

def generate_data():
    # select a distribution type
    data_distributions = {
        'normal': generate_random_normal_distribution,
        'log-normal': generate_random_lognormal_distribution,
        'gamma': generate_random_gamma_distribution,
        'weibull': generate_random_weibull_distribution,
        'uniform': generate_random_uniform_distribution,
    }
    distribution = np.random.choice(list(data_distributions.keys()))

    # generate parameters
    size = np.random.randint(*parameters.get('size_range', ()))
    bins = np.random.randint(*parameters.get('bins_range', ()))
    
    # get data distribution (and ensure no negative y values)
    y, X = data_distributions[distribution](size, bins)
    y = y.clip(0)

    return {
        'X': X,
        'y': y,
        'distribution': distribution,
    }

'''
Title: histogram.py
Author: Bokeh
Date: 2021
Code version: N/A
Availability: https://docs.bokeh.org/en/latest/docs/gallery/histogram.html

The basis for the following generation functions was taken from the above
'''

# generates a normal distribution (with random mu, sigma, and size)
def generate_random_normal_distribution(size, bins):
    mu = np.random.uniform(*parameters.get('mu_range', ()))
    sigma = np.random.uniform(*parameters.get('sigma_range', ()))
    measured = np.random.normal(mu, sigma, size)
    y, X = np.histogram(measured, density=False, bins=bins)
    return y, X

# generates a logistic normal distribution (with random mu, sigma, and size)
def generate_random_lognormal_distribution(size, bins):
    mu = np.random.uniform(*parameters.get('mu_range', ()))
    sigma = np.random.uniform(*parameters.get('sigma_range', ()))
    measured = np.random.lognormal(mu, sigma, size)
    y, X = np.histogram(measured, density=True, bins=bins)
    return y, X

# generates a gamma distribution (with random k, theta, and size)
def generate_random_gamma_distribution(size, bins):
    k = np.random.uniform(*parameters.get('k_range', ()))
    theta = np.random.uniform(*parameters.get('theta_range', ()))
    measured = np.random.gamma(k, theta, size)
    y, X = np.histogram(measured, density=True, bins=bins)
    return y, X

# generates a weibull distribution (with random lambda, k, and size)
def generate_random_weibull_distribution(size, bins):
    lam = np.random.uniform(*parameters.get('lambda_range', ()))
    k = np.random.uniform(*parameters.get('k_range', ()))
    measured = lam*(-np.log(np.random.uniform(0, 1, size)))**(1/k)
    y, X = np.histogram(measured, density=True, bins=bins)
    return y, X

# generates a uniform distribution (with random range and size)
def generate_random_uniform_distribution(size, bins):
    low = np.random.uniform(*parameters.get('low_range', ()))
    high = np.random.uniform(*parameters.get('high_range', ()))
    measured = np.random.uniform(low, high, size)
    y, X = np.histogram(measured, density=True, bins=bins)
    return y, X