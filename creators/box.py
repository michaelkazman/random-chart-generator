from creators.utils import unpack_graph_object
from bokeh.plotting import figure

# dictionary for creating graphs
creator_parameters = {
    'line_color': 'black',
    'bar_width': 0.7,
    'extreme_width_units': 0.2,
    'extreme_width': 0.01,
    'outlier_fill_opacity': 0.6,
    'outlier_size': 6,
}

def create_bokeh_graph(graph_object):
    # get bokeh-specific parameters
    (X, df), style = unpack_graph_object(graph_object)
    limits, quartiles, outliers = calc_params_bokeh(df)
    # unpackage everything
    upper, lower = limits
    q1, q2, q3 = quartiles
    outx, outy = outliers
    line_color = creator_parameters['line_color']
    # define figure
    p = figure(x_range=X)
    # whiskers
    p.segment(X, upper.y, X, q3.y, line_color=line_color)
    p.segment(X, lower.y, X, q1.y, line_color=line_color)
    # boxes
    p.vbar(X, creator_parameters['bar_width'], q2.y, q3.y, line_color=line_color)
    p.vbar(X, creator_parameters['bar_width'], q1.y, q2.y, line_color=line_color)
    # extremes (drawing almost-0 height rects are simpler than drawing segments)
    p.rect(X, lower.y, creator_parameters['extreme_width_units'], creator_parameters['extreme_width'], line_color=line_color)
    p.rect(X, upper.y, creator_parameters['extreme_width_units'], creator_parameters['extreme_width'], line_color=line_color)
    # outliers
    if ((outx != None) and (outy != None)):
        p.circle(outx, outy, size=creator_parameters['outlier_size'], fill_alpha=creator_parameters['outlier_fill_opacity'])
    return p

def calc_params_bokeh(df):
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
    
def create_altair_graph(graph_object):
    return {}

def create_plotnine_graph(graph_object):
    return {}