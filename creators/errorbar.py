from creators.utils import unpack_graph_object
from bokeh.plotting import figure

import altair as alt
import pandas as pd
import numpy as np

parameters = {
    'width':    400,
    'height':   400,
    'alt_point_size': 40,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, y_errors), style = unpack_graph_object(graph_object)
    plot = figure(width=parameters['width'], height=parameters['height'])

    # plot each layer
    for index, y in enumerate(y):
        y_error = y_errors[index]

        plot.circle(X, y)
        plot.line(X, y)

        if y_error[0] != None:
            y_err_x, y_err_y = [], []
            for px, py, err in zip(X, y, y_error):
                y_err_x.append((px, px))
                y_err_y.append((py - err, py + err))
            plot.multi_line(y_err_x, y_err_y)
        
    return plot

def create_altair_graph(graph_object):
    # format
    (X, y, y_errors), style = unpack_graph_object(graph_object)
    
    # make and store points, error bars, and lines for each layer
    layered_points, layered_errorbars, layered_lines = [], [], []
    for i in range(0, len(y)):
        # set up data frame
        source = pd.DataFrame({"x": X, "y": y[i], "yerr": y_errors[i]})

        # the base chart for other charts to build upon
        base = alt.Chart(source).transform_calculate(
            ymin="datum.y-datum.yerr",
            ymax="datum.y+datum.yerr"
        )

        # make the points
        points = base.mark_point(
            filled=True,
            size=parameters['alt_point_size'],
        ).encode(
            x=alt.X('x'),
            y=alt.Y('y')
        )

        # make the error bars
        errorbars = base.mark_errorbar().encode(
            x="x",
            y="ymin:Q",
            y2="ymax:Q"
        )

        # link the points with lines
        lines = base.mark_line().encode(
            x='x',
            y='y',
        )

        # store, then move to next layer
        layered_points.append(points)
        layered_errorbars.append(errorbars)
        layered_lines.append(lines)

    # make final chart by layering
    chart = alt.layer(*layered_points, *layered_errorbars, *layered_lines)
    return chart

def create_plotnine_graph(graph_object):
    return {}