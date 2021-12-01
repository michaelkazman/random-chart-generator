from creators.utils import unpack_graph_object

from bokeh.plotting import figure
import numpy as np

import altair as alt
import pandas as pd

# dictionary for creating graphs
parameters = {
    'width':    400,
    'height':   400,
    'line_color': 'black',
    'alt_line_color': '#000',
    'bar_width': 0.7,
    'extreme_width_units': 0.2,
    'extreme_width': 0.01,
    'outlier_fill_opacity': 0.6,
    'outlier_size': 6,
}

def create_bokeh_graph(graph_object):
    # unpackage and get bokeh-specific parameters
    (df, ), style = unpack_graph_object(graph_object)
    limits, quartiles, outliers = calc_params(df)

    # unpackage everything
    upper, lower = limits
    q1, q2, q3 = quartiles
    outx, outy = outliers
    line_color = parameters['line_color']

    # get X labels
    X = np.unique(df.group)

    # define figure
    p = figure(x_range=X)

    # whiskers
    p.segment(X, upper.y, X, q3.y, line_color=line_color)
    p.segment(X, lower.y, X, q1.y, line_color=line_color)

    # boxes
    p.vbar(X, parameters['bar_width'], q2.y, q3.y, line_color=line_color)
    p.vbar(X, parameters['bar_width'], q1.y, q2.y, line_color=line_color)

    # extremes (drawing almost-0 height rects are simpler than drawing segments)
    p.rect(X, lower.y, parameters['extreme_width_units'], parameters['extreme_width'], line_color=line_color)
    p.rect(X, upper.y, parameters['extreme_width_units'], parameters['extreme_width'], line_color=line_color)

    # outliers
    if ((outx != None) and (outy != None)):
        p.circle(outx, outy, size=parameters['outlier_size'], fill_alpha=parameters['outlier_fill_opacity'])

    return p

    
def create_altair_graph(graph_object):
    # unpack data
    (df, ), style = unpack_graph_object(graph_object)

    # create data frame and declare local variables
    source = df
    width = parameters['width']
    height = parameters['height']

    # create box plot chart
    box_plot = alt.Chart(source).mark_boxplot().encode(
        x = 'group:O',
        y = 'y:Q',
    ).properties(
        width=width,
        height=height,
    )

    # get extremes for each box
    df_list = [g for (_, g) in df.groupby('group')]
    _, _, outliers = calc_params(df)
    extreme_values =[]
    extreme_groups = []

    for df_box in df_list:
        group = df_box.group.values[0]
        higher = None
        lower = None
        
        # loop through each y value
        for y_val in df_box.y.values:
            # ensure we are not adding outliers
            if (outliers[1] != None and y_val in outliers[1]): continue
            # otherwise check to see if new records
            if (higher == None or y_val > higher): higher = y_val
            if (lower == None or y_val < lower): lower = y_val

        # store in arrays for later dict
        extreme_values.append(higher)
        extreme_groups.append(group)
        extreme_values.append(lower)
        extreme_groups.append(group)

    # make dictionary from arrays
    extreme_dict = {
        'group': extreme_groups,
        'y': extreme_values,
    }

    # make data frame
    extreme_df = pd.DataFrame(data=extreme_dict)

    # create extremes chart
    size = width*0.7 / (np.unique(df.group).size)
    mark_cap = alt.MarkDef(type='tick', size=size/6, opacity=1)

    extremes = alt.Chart(
        data=extreme_df,
        width=width, 
        height=height,
        mark=mark_cap,
    ).encode(
        x='group',
        y='y:Q',
        color=alt.value(parameters['alt_line_color'])
    )

    # layer into main chart
    chart = alt.layer(
        box_plot, extremes,
    )

    return chart

def create_plotnine_graph(graph_object):
    return {}


# UTIL helper function
def calc_params(df):
    # find the quartiles and IQR for each category
    groups = df.groupby('group')
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1

    # calculate upper and lower limits from quartiles and inter quartile range
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    # find the outliers for each category
    # (needed as inner func for pandas .apply())
    def get_outliers(g):
        X, y = g.name, g.y
        return g[(y > upper.loc[X]['y']) | (y < lower.loc[X]['y'])]['y']
    out = groups.apply(get_outliers).dropna()

    # prepare outlier data for plotting, we need coordinates for every outlier
    outx = None if out.empty else list(out.index.get_level_values(0))
    outy = None if out.empty else list(out.values)
    
    # return all data in tuple format
    limits = (upper, lower)
    quartiles = (q1, q2, q3)
    outliers = (outx, outy)
    
    return limits, quartiles, outliers