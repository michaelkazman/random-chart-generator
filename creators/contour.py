import numpy as np
import pandas as pd
import plotnine as p9
from bokeh.plotting import figure
from utils.creators import unpack_graph_object

def create_bokeh_graph(graph_object):
  # format data
    (X, y, z, x_text, y_text, X_range, y_range), styles = unpack_graph_object(graph_object)
    df = {
        'X': X,
        'y': y,
        'z': z,
        'x_text': x_text,
        'y_text': y_text,
        'color': styles.get('color') if styles.get('use_random_colors') else styles.get('color')[:1] * len(styles.get('color')),
        'text_color': [styles.get('text_color')] * len(styles.get('color'))
    }

    # initialize figure
    p = figure(
        plot_width=500,
        plot_height=300,
        x_range=X_range,
        y_range=y_range,
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    
    # plot various lines (representing the contour segments)
    p.multi_line(
        xs='X',
        ys='y',
        line_color='color',
        line_width=styles.get('line_thickness'),
        source=df
    )

    # plot contour values
    p.text(
        x='x_text',
        y='y_text',
        text='z',
        text_color='text_color',
        text_baseline='middle',
        text_align='center',
        source=df,
    )

    return p

def create_altair_graph(graph_object):
    # not supported by vega-lite (the altair renderer)
    return {}

def create_plotnine_graph(graph_object):
    # unpack / format data
    (X, y, z, *_), styles = unpack_graph_object(graph_object)

    # flatten arrays
    X_flattened = np.hstack(X).flatten()
    y_flattened = np.hstack(y).flatten()
    z_flattened = np.hstack([[z[i]] * len(row) for i, row in enumerate(X)]).flatten()

    # create df
    df = pd.DataFrame({
        'X': X_flattened,
        'y': y_flattened,
        'z': z_flattened,
    })

    p = (
        p9.ggplot(p9.aes(x='X', y='y'), data=df)
        + p9.stat_density_2d(geom='polygon', show_legend=False, color=styles.get('color', [])[0], fill=None, size=styles.get('line_thickness'))
        + p9.scales.scale_x_continuous(limits=(-2, 2), expand=(0, 0))
        + p9.scales.scale_y_continuous(limits=(-2, 2), expand=(0, 0))
        + p9.geom_text(p9.aes(x='X', y='y', label='z', group='X'), data=df[::200])
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
    )

    return p