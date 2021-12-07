import matplotlib.pyplot as plt

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from utils.creators import unpack_graph_object

parameters = {
    'width': 400,
    'height': 400
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, z), style = unpack_graph_object(graph_object)
    df = get_contour(X, y, z)

    # initialize figure
    p = figure(
        plot_width=parameters.get('width'),
        plot_height=parameters.get('height'),
        x_range=[X[0][0], X[-1][-1]],
        y_range=[y[0][0], y[-1][-1]]
    )
    # plot various lines (representing the contour segments)
    p.multi_line(
        xs='xs',
        ys='ys',
        line_color='line_color',
        source=df
    )

    return p

def get_contour(X, y, z):
    # format data
    plt.ioff()
    cs = plt.contour(X, y, z)
    xs, ys, col = [], [], []
    isolevelid = 0
    
    # go through each contour level
    for isolevel in cs.collections:
        isocol = isolevel.get_color()[0]
        thecol = 3 * [None]
        isolevelid += 1

        # generate colour values
        for i in range(3):
            thecol[i] = int(255 * isocol[i])
        thecol = '#%02x%02x%02x' % (thecol[0], thecol[1], thecol[2])

        # map out contour paths
        for path in isolevel.get_paths():
            v = path.vertices
            x = v[:, 0]
            y = v[:, 1]
            xs.append(x.tolist())
            ys.append(y.tolist())
            col.append(thecol)

    df = ColumnDataSource({
            'xs': xs,
            'ys': ys,
            'line_color': col
        }
    )

    return df

def create_altair_graph(graph_object):
    return {}

def create_plotnine_graph(graph_object):
    return {}