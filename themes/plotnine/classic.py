import plotnine as p9

class Theme(p9.themes.theme_bw):
    '''
    A classic-looking theme, with x & y axis lines and
    no gridlines.

    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 11.
    base_family : str, optional
        Base font family.
    '''

    def __init__(self, base_size=11, base_family=None):
        p9.themes.theme_bw.__init__(self, base_size, base_family)
        self.add_theme(
            p9.themes.theme(panel_border=p9.themes.elements.element_blank(),
                axis_line=p9.themes.elements.element_line(color='black'),
                panel_grid_major=p9.themes.elements.element_line(),
                panel_grid_major_x=p9.themes.elements.element_blank(),
                panel_grid_major_y=p9.themes.elements.element_blank(),
                panel_grid_minor=p9.themes.elements.element_line(),
                panel_grid_minor_x=p9.themes.elements.element_blank(),
                panel_grid_minor_y=p9.themes.elements.element_blank(),
                strip_background=p9.themes.elements.element_rect(
                    colour='black', fill='None', size=1,
                ),
                legend_key=p9.themes.elements.element_blank()
            ),
            inplace=True,
        )