from creators.utils import unpack_graph_object
from bokeh.plotting import figure

parameters = {
    'width':    400,
    'height':   400,
    'colours': ['red', 'blue', 'green', 'orange', 'purple'],
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, y_error), style = unpack_graph_object(graph_object)
    plot = figure(width=parameters['width'], height=parameters['height'])

    # plot each layer
    for index, y in enumerate(y):
        colour = parameters['colours'][index]
        yerrs = y_error[index]
        plot = error_bar_bokeh(plot, X, y, yerrs, colour)
        
    return plot

def error_bar_bokeh(fig, x, y, yerr, color):
    # create line graph
    fig.circle(x, y, color=color)
    fig.line(x, y, line_color = color)

    # add error bars (as applicable)
    if yerr[0] != None:
        y_err_x, y_err_y = [], []
        for px, py, err in zip(x, y, yerr):
            y_err_x.append((px, px))
            y_err_y.append((py - err, py + err))
        fig.multi_line(y_err_x, y_err_y, color=color)
    
    return fig

def create_altair_graph(graph_object):
    return {}

def create_plotnine_graph(graph_object):
    return {}