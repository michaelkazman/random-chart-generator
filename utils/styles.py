import json
import numpy as np

# generate style object based on graph
def generate_styles(graph_type, library):
    styles_json = json_from_file('styles/{graph_type}.json'.format(graph_type=graph_type))
    styles_merged = styles_json['default'] | styles_json[library]
    styles = resolve_styles(styles_merged)
    return styles

# retrieve json from file
def json_from_file(file_path):
    with open(file_path) as f:
      return json.load(f)

# transform json properties to usable values
def resolve_styles(styles):
    resolved_styles = {}
    for style_name, style_object in styles.items():
        # extract all fields except for type
        style_type = style_object['type']
        style_dict = dict([(key, value) for key, value in style_object.items() if key != 'type'])
        # resolve value and append to output dict
        resolved_value = resolves[style_type](**style_dict)
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
def resolve_range(value, **_):
    min_value, max_value = value
    random_function = np.random.uniform if (value['float'] == True) else np.random.randint
    return random_function(min_value, max_value)

# generates random RGB value
def resolve_color(**_):
    return (
        np.random.randint(0, 255), 
        np.random.randint(0, 255),
        np.random.randint(0, 255)
    )

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
