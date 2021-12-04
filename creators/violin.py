import numpy as np
import pandas as pd
import altair as alt
import hvplot.pandas
import holoviews as hv

from holoviews import opts
from utils.creators import unpack_graph_object

# set holoviews to use bokeh
hv.extension('bokeh')

parameters = {
    'color': 'black',
    'orientation': 'horizontal',
    'stack': 'center',
    'resolve_mode': 'independent',
    'bokeh_height_min_threshold': 1.5,
    'bokeh_height_max_threshold': 1.5,
    'height_min_threshold': 1,
    'height_max_threshold': 1,
    'padding': 20,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y), style = unpack_graph_object(graph_object)
    data = pd.DataFrame({
        'X': X,
        'y': y,
    })

    p = data.hvplot.violin(
        y='y',
        by='X',
        c='X',
        legend=False, 
    ).opts(opts.Violin(
        ylim=calculate_y_lim(y, ['bokeh_height_min_threshold', 'bokeh_height_max_threshold']),
    ))

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y), style = unpack_graph_object(graph_object)
    
    # create boxplot
    boxplot = alt.Chart().mark_boxplot(color='black').encode(
        alt.Y(f'y:Q')
    ).properties(width=200)

    # create violin
    y_limit = calculate_y_lim(y)
    violin = alt.Chart().transform_density(
        'y',
        as_=['y', 'density'],
        extent=y_limit,
        groupby=['X']
    ).mark_area(orient='horizontal').encode(
        y='y:Q',
        color=alt.Color('X:N', legend=None),
        x=alt.X(
            'density:Q',
            stack='center',
            impute=None,
            title=None,
            scale=alt.Scale(nice=False, zero=False, padding=parameters['padding']),
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True),
        ),
    )

    # stack violin with inner boxplot
    facet = lambda data: alt.layer(
        violin,
        boxplot,
        data=data
    ).facet(
        column='X:N',
    ).resolve_scale(
        x=alt.ResolveMode('independent')
    )


    # plot the layered violin and boxplots from above
    # puts layered graphs into a facet for plotting
    df = pd.DataFrame({ 'X': X, 'y': y, })
    plot = alt.hconcat(facet(df), spacing=40).configure_facet(
        spacing=0,
    ).configure_header(
        titleOrient='bottom',
        labelOrient='bottom'
    ).configure_view(
        stroke=None,
    )

    return plot

def create_plotnine_graph(graph_object):
    return {}

def calculate_y_lim(y, threshold_names=['height_min_threshold', 'height_max_threshold']):
    # create violin
    height_range = (np.min(y) * (1 + parameters[threshold_names[0]]), np.max(y) * (1 + parameters[threshold_names[1]]))
    return height_range