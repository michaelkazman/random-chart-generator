import numpy as np
import pandas as pd
import plotnine as p9
import matplotlib.pyplot as plt

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from utils.creators import unpack_graph_object
import math

parameters = {
    'width': 400,
    'height': 400,
}

def create_bokeh_graph(graph_object):
  # format data
    (X, y, z), styles = unpack_graph_object(graph_object)
    df = get_contour_data(X, y, z)

    # initialize figure
    p = figure(
        plot_width=500,
        plot_height=300,
        x_range=[X[0][0], X[-1][-1]],
        y_range=[y[0][0], y[-1][-1]],
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    
    # plot various lines (representing the contour segments)
    p.multi_line(
        xs='X',
        ys='y',
        line_color='line_color',
        source=df
    )

    # plot contour values
    p.text(
        x='x_text',
        y='y_text',
        text='z',
        text_color='line_color',
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
    (X, y, z), styles = unpack_graph_object(graph_object)
    data = get_contour_data(X, y, z)

    # flatten arrays
    X_flattened = np.hstack(data['X']).flatten()
    y_flattened = np.hstack(data['y']).flatten()
    z_flattened = np.hstack([[data['z'][i]] * len(row) for i, row in enumerate(data['X'])]).flatten()

    # create df
    df = pd.DataFrame({
        'X': X_flattened,
        'y': y_flattened,
        'z': z_flattened,
    })

    p = (
        p9.ggplot(p9.aes(x='X', y='y'), data=df)
        + p9.stat_density_2d(
        p9.aes(),
        )
        + p9.scales.scale_x_continuous(limits=(-2, 2), expand=(0, 0))
        + p9.scales.scale_y_continuous(limits=(-2, 2), expand=(0, 0))
        + p9.geom_text(p9.aes(x='X', y='y', label='z'), data=df[::200])
    )

    return p

'''
Title: get_contour_data()
Author: BR123
Date: 2016
Code version: N/A
Availability: https://docs.bokeh.org/en/latest/docs/gallery/histogram.html

The contour function below was used to plot values with matplotlib and scrape the generated plot values
'''

def get_contour_data(X, Y, Z):
    # generate matplotlib contour
    cs = plt.contour(X, Y, Z)
    X_points, y_points, z_points, z_flattened = [], [], np.array([]), np.array([])
    x_text, y_text, line_color = np.array([]), np.array([]), np.array([])

    # go through each contour level
    for i, level in enumerate(cs.collections):
        level_color = level.get_color()[0]
        level_rgb_color = [int(255 * rgb_value) for rgb_value in level_color]
        level_hex_color = "#{0:02x}{1:02x}{2:02x}".format(*level_rgb_color)
        z = round(cs.get_array()[i], 2)

        # append points, text coordinates, text, and colour
        for path in level.get_paths():
            x, y = path.vertices[:, 0], path.vertices[:, 1]
            X_points.append(x.tolist())
            y_points.append(y.tolist())
            x_text = np.append(x_text, x[math.floor(len(x) / 2)])
            y_text = np.append(y_text, y[math.floor(len(y) / 2)])
            z_points = np.append(z_points, z)
            line_color = np.append(line_color, level_hex_color)

    # create dict based on scraped data
    df = {
      'X': np.array(X_points, dtype=object),
      'y': np.array(y_points, dtype=object),
      'z': z_points,
      'x_text': x_text,
      'y_text':y_text,
      'line_color': line_color
    }
    return df