import json
import numpy as np
from utils.utils import json_from_file, get_library_class

# generate style object based on graph
def generate_styles(graph_type, library, num_repeats):
    # resolve styles to values from style json
    styles_json = json_from_file('styles/{graph_type}.json'.format(graph_type=graph_type))
    styles_merged = styles_json.get('default', {}) | styles_json.get(library, {})
    styles = resolve_styles(styles_merged, num_repeats)
    # add random theme (i.e. theme name) to style object
    library_class = get_library_class(library)
    styles['theme'] = library_class.get_theme()
    return styles

# transform json properties to usable values
def resolve_styles(styles, num_repeats):
    resolved_styles = {}
    for style_name, style_object in styles.items():
        # extract all fields except for type
        style_type, should_repeat = style_object['type'], style_object.get('repeat', False)
        # resolve style values and append to output dict
        # calculate multiple (if style has repeat flag (as well as the repeat number))
        resolved_value = (
            resolves[style_type](**style_object) if not should_repeat
            else [resolves[style_type](**style_object) for _ in range(num_repeats)]
        )        
        resolved_styles[style_name] = resolved_value
    return resolved_styles

# return static value
def resolve_value(value, **_):
    return value

# pick random value from the list
def resolve_option(value, **_):
    return np.random.choice(value)

# generates random boolean value
def resolve_boolean(**_):
    return bool(np.random.getrandbits(1))

# generates a value between the specified range
# default is int unless float flag is specified
def resolve_range(value, float=False, **_):
    min_value, max_value = value
    random_function = np.random.uniform if float else np.random.randint
    return random_function(min_value, max_value)

# generates random RGB value
def resolve_color(**_):
    colors = (
        np.random.randint(0, 255), 
        np.random.randint(0, 255),
        np.random.randint(0, 255)
    )
    return '#%02x%02x%02x' % colors

# reads in JSON file from path
def resolve_json(value, **_):
    with open(value) as f:
        return json.load(f)

# a mapping of the style type and the function to resolve it
resolves = {
    'value': resolve_value,
    'option': resolve_option,
    'boolean': resolve_boolean,
    'range': resolve_range,
    'color': resolve_color,
    'json': resolve_json,
}
