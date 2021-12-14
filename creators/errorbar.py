import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9

from bokeh.plotting import figure
from utils.creators import convert_numbers_to_letters, unpack_graph_object

parameters = {
    'width':    400,
    'height':   400,
    'alt_point_size': 40,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, y_errors, *_), styles = unpack_graph_object(graph_object)
    p = figure(
        width=parameters.get('width'), 
        height=parameters.get('height'), 
        toolbar_location=None,
    )

    # plot each layer
    for y, y_error in zip(y, y_errors):
        # plot points
        p.circle(X, y)
        p.line(X, y)

        # plot vertical error lines
        y_err_x, y_err_y = [], []
        for px, py, err in zip(X, y, y_error):
            y_err_x.append((px, px))
            y_err_y.append((py - err, py + err))
        p.multi_line(y_err_x, y_err_y)

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, y_errors, *_), styles = unpack_graph_object(graph_object)
    layered_points, layered_errorbars, layered_lines = [], [], []

    # create each 'line' layer
    for y_i, y_error in zip(y, y_errors):
        # set up data frame
        df = pd.DataFrame({
            'X': X,
            'y': y_i,
            'yerr': y_error}
        )

        # the base chart for other charts to build upon
        base = alt.Chart(df).transform_calculate(
            ymin='datum.y-datum.yerr',
            ymax='datum.y+datum.yerr'
        )

        # create points
        points = base.mark_point(
            filled=True,
            size=parameters.get('alt_point_size'),
        ).encode(
            x='X',
            y='y'
        )

        # create error bars
        errorbars = base.mark_errorbar().encode(
            x='X',
            # y='ymin:Q',
            y=alt.Y('ymin:Q', axis=alt.Axis(title='y')),
            y2='ymax:Q'
        )

        # link the points and lines
        lines = base.mark_line().encode(
            x='X',
            y='y',
        )

        # store that layers points, error bars, and lines
        layered_points.append(points)
        layered_errorbars.append(errorbars)
        layered_lines.append(lines)

    # combine layers
    p = alt.layer(*layered_points, *layered_errorbars, *layered_lines)
    return p

def create_plotnine_graph(graph_object):
     # format data
    (X, y_layers, y_errors, *_), styles = unpack_graph_object(graph_object)
    num_layers = len(y_layers)

    # create labels to group layers by, and get max and min for error bars
    layer_names = np.copy(y_layers)
    y_err_min, y_err_max = np.copy(y_layers), np.copy(y_layers)
    for i in range(num_layers):
        layer_names[i, :] = i
        for j in range(len(y_layers[i])):
            y_err_min[i][j] = y_layers[i][j] - y_errors[i][j]
            y_err_max[i][j] = y_layers[i][j] + y_errors[i][j]

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y_layers = y_layers.flatten()
    y_err_min = y_err_min.flatten()
    y_err_max = y_err_max.flatten()
    layer_names = convert_numbers_to_letters(layer_names.flatten())

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y_layers,
        'y_err_min': y_err_min,
        'y_err_max': y_err_max,
    })

    # create plot
    p = p9.ggplot(
        data=df, 
        mapping=p9.aes(
            x=X, 
            y=y_layers, 
            color=layer_names, 
            ymax='y_err_max', 
            ymin='y_err_min',
        ),
    ) + p9.geom_line(show_legend='None') + p9.geom_point(show_legend='None') + p9.geom_errorbar(show_legend='None') + p9.labels.xlab('X') + p9.labels.ylab('y')

    return p