from generators.utils import generate_midpoint_displacement

parameters = {
    'start_range':  (50, 400),
    'end_range':    (50, 400),
    'width_range':  (400, 1000),
    'rough_range':  (0.7, 2),
    'vertical_displacement_range':  (50, 250),
    'num_iterations_range': (3, 10),
    'layers_range':  (1, 6),
}

def generate_data():
    return generate_midpoint_displacement(parameters)