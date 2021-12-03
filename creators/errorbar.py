import numpy as np
import pandas as pd
import altair as alt

from bokeh.plotting import figure
from creators.utils import unpack_graph_object

parameters = {
    'width':    400,
    'height':   400,
    'alt_point_size': 40,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, y_errors), style = unpack_graph_object(graph_object)
    p = figure(width=parameters['width'], height=parameters['height'])

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
    (X, y, y_errors), style = unpack_graph_object(graph_object)
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
            size=parameters['alt_point_size'],
        ).encode(
            x='X',
            y='y'
        )

        # create error bars
        errorbars = base.mark_errorbar().encode(
            x='X',
            y='ymin:Q',
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
    return {}