from utils.utils import get_module_attr, get_library_class

def create_graph(graph_type, library, graph_object):
    # set theme 
    theme = graph_object.get('styles', {}).get('theme')
    library_class = get_library_class(library)
    library_class.set_theme(graph_type, theme)

    # graph creation
    creator_function = get_module_attr(
        'creators.{graph_type}'.format(graph_type=graph_type),
        'create_{library}_graph'.format(library=library),
    )
    created_graph = creator_function(graph_object)

    # run any post setup library-dependent steps 
    # will return new graph (if applicable)
    post_creation_graph = library_class.post_creation_hook(graph_type, created_graph)
    graph = created_graph if post_creation_graph == None else post_creation_graph 
    
    return graph

def unpack_graph_object(graph_object):
    unpacked_object = (
        graph_object.get('data', {}).values(),
        graph_object.get('styles', {}), 
    )
    return unpacked_object

def convert_numbers_to_letters(numbers):
    return [chr(int(i) + 65) for i in numbers]