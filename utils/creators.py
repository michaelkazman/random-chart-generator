from importlib import import_module

def create_graph(graph_type, library, graph_object):
    create_module = import_module('creators.{graph_type}'.format(graph_type=graph_type))
    creator_function_name = 'create_{library}_graph'.format(library=library)
    creator_function = getattr(create_module, creator_function_name)
    graph = creator_function(graph_object)
    return graph

def unpack_graph_object(graph_object):
    unpacked_object = (
        graph_object['data'],
        graph_object['styles'], 
    )
    return unpacked_object