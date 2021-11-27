from importlib import import_module

def generate_data(graph_type):
    generate_module = import_module('generators.{graph_type}'.format(graph_type=graph_type))
    generate_function_name = 'generate_data'
    generate_function = getattr(generate_module, generate_function_name)
    data = generate_function()
    return data