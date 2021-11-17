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

def generate_histogram_data():
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
    size = np.random.randint(*get_parameter('size_range'))
    bins = np.random.randint(*get_parameter('bins_range'))
    
    # return 
    X, y = data_distributions[distribution](size, bins)
    return X, y

# generates a normal distribution (with random mu, sigma, and size)
def generate_random_normal_distribution(size, bins):
    mu = np.random.uniform(*get_parameter('mu_range'))
    sigma = np.random.uniform(*get_parameter('sigma_range'))
    measured = np.random.normal(mu, sigma, size)
    X, y = np.histogram(measured, density=True, bins=bins)
    return X, y

# generates a logistic normal distribution (with random mu, sigma, and size)
def generate_random_lognormal_distribution(size, bins):
    mu = np.random.uniform(*get_parameter('mu_range'))
    sigma = np.random.uniform(*get_parameter('sigma_range'))
    measured = np.random.lognormal(mu, sigma, size)
    X, y = np.histogram(measured, density=True, bins=bins)
    return X, y

# generates a gamma distribution (with random k, theta, and size)
def generate_random_gamma_distribution(size, bins):
    k = np.random.uniform(*get_parameter('k_range'))
    theta = np.random.uniform(*get_parameter('theta_range'))
    measured = np.random.gamma(k, theta, size)
    X, y = np.histogram(measured, density=True, bins=bins)
    return X, y

# generates a weibull distribution (with random lambda, k, and size)
def generate_random_weibull_distribution(size, bins):
    lam = np.random.uniform(*get_parameter('lambda_range'))
    k = np.random.uniform(*get_parameter('k_range'))
    measured = lam*(-np.log(np.random.uniform(0, 1, size)))**(1/k)
    X, y = np.histogram(measured, density=True, bins=bins)
    return X, y

# generates a np.random.uniform distribution (with random range and size)
def generate_random_uniform_distribution(size, bins):
    low = np.random.uniform(*get_parameter('low_range'))
    high = np.random.uniform(*get_parameter('high_range'))
    measured = np.random.uniform(low, high, size)
    X, y = np.histogram(measured, density=True, bins=bins)
    return X, y