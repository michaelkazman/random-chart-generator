import numpy as np
from scipy.stats import norm
from sklearn.neighbors import KernelDensity

parameters = {
    'mean_range': [0, 5],
    'sigma_range': [1, 1],
    'size_range': (0.3, 0.7),
    'N': 100,
    'num_distribution_range': (1, 3),
}

def generate_data():
    # generate parameters
    N = parameters.get('N')
    num_distributions = np.random.randint(*parameters.get(('num_distribution_range')))
    means = np.random.uniform(*parameters.get('mean_range'), num_distributions)
    sigmas = np.random.uniform(*parameters.get('sigma_range'), num_distributions)
    sizes = np.random.uniform(*parameters.get('size_range'), num_distributions)

    X = np.concatenate(
        [np.random.normal(means[i], sigmas[i], int(sizes[i] * N)) for i in range(num_distributions)]
    )[:, np.newaxis]

    X_plot = np.linspace(-5, 10, 1000)[:, np.newaxis]

    true_dens = 0
    kernel_options = ['gaussian', 'epanechnikov', 'exponential', 'linear', 'cosine']
    kernels = np.random.choice(kernel_options, size=num_distributions, replace=False)

    X_data, y_data = [], []
    for i in range(num_distributions):
        true_dens = sizes[i] * norm(means[i], sigmas[i]).pdf(X_plot[:, 0]) + true_dens
        kde = KernelDensity(kernel=kernels[i], bandwidth=0.5).fit(X)
        X_i = X_plot[:, 0]
        y_i = np.exp(kde.score_samples(X_plot)) 
        X_data.append(X_i)
        y_data.append(y_i)
    
    return {
        'X': np.array(X_data),
        'y': np.array(y_data),
        'num_repeats': len(X_data)
    }