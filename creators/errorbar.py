import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from utils.creators import convert_numbers_to_letters, unpack_graph_object

def create_bokeh_graph(graph_object):
    # format data
    (X, y, y_errors, *_), styles = unpack_graph_object(graph_object)
    p = figure(
        width=styles.get('width'), 
        height=styles.get('height'), 
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )

    # plot each layer
    for i, (y, y_error) in enumerate(zip(y, y_errors)):
        # plot points
        getattr(p, styles.get('marker_type'))(X, y, color=styles.get('color')[i], size=styles.get('marker_size'))
        p.line(X, y, color=styles.get('color')[i], line_width=styles.get('line_thickness'))

        # plot vertical error lines
        y_err_x, y_err_y = [], []
        for px, py, err in zip(X, y, y_error):
            y_err_x.append((px, px))
            y_err_y.append((py - err, py + err))
        p.multi_line(y_err_x, y_err_y, color=styles.get('color')[i], line_width=styles.get('error_bar_thickness'))

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, y_errors, *_), styles = unpack_graph_object(graph_object)
    layered_points, layered_errorbars, layered_lines = [], [], []

    # create each 'line' layer
    for i, (y_i, y_error) in enumerate(zip(y, y_errors)):
        # set up data frame
        df = pd.DataFrame({
            'X': X,
            'y': y_i,
            'yerr': y_error,
            'color': styles.get('color')[i],
            'size': styles.get('marker_size')
        })

        # the base chart for other charts to build upon
        base = alt.Chart(df).transform_calculate(
            ymin='datum.y-datum.yerr',
            ymax='datum.y+datum.yerr'
        )

        # create points
        points = base.mark_point(
            filled=True,
            size=alt.Value(styles.get('marker_size')),
        ).encode(
            x='X',
            y='y'
        )

        # create error bars
        errorbars = base.mark_errorbar().encode(
            x='X',
            y=alt.Y('ymin:Q', axis=alt.Axis(title='y')),
            y2='ymax:Q',
            strokeWidth=alt.value(styles.get('error_bar_thickness'))
        )

        # link the points and lines
        lines = base.mark_line().encode(
            x='X',
            y='y',
            color=alt.Color('color', legend=None),
            strokeWidth=alt.value(styles.get('line_thickness'))
        )

        # store that layers points, error bars, and lines
        layered_points.append(points)
        layered_errorbars.append(errorbars)
        layered_lines.append(lines)

    # combine layers
    p = alt.layer(
        *layered_points,
        *layered_errorbars,
        *layered_lines
    ).properties(
        width=styles.get('width'),
        height=styles.get('height')
    )
    
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
    p = (
        p9.ggplot(
            data=df, 
            mapping=p9.aes(
                x='X', 
                y='y', 
                ymax='y_err_max', 
                ymin='y_err_min',
                color=layer_names,
                fill=layer_names,
            ),
        )
        + p9.geom_line(show_legend='None', size=styles.get('line_thickness'))
        + p9.geom_point(show_legend='None', size=styles.get('marker_size'))
        + p9.geom_errorbar(show_legend='None', size=styles.get('error_bar_thickness'))
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
        + p9.scale_color_manual(values=styles.get('color'))
        + p9.scale_fill_manual(values=styles.get('color'))
    )

    return p