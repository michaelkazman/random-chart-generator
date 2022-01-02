import plotnine as p9

class Theme(p9.themes.theme_gray):
    '''
    Theme in the likeness of fivethirtyeight.com plots

    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 11.
    base_family : str, optional
        Base font family.
    '''
    def __init__(self, base_size=11, base_family='DejaVu Sans'):
        p9.themes.theme_gray.__init__(self, base_size, base_family)
        bgcolor = '#F0F0F0'
        self.add_theme(
            p9.themes.theme(
                axis_ticks=p9.themes.elements.element_blank(),
                title=p9.themes.elements.element_text(color='#3C3C3C'),
                legend_background=p9.themes.elements.element_rect(fill='None'),
                legend_key=p9.themes.elements.element_rect(fill='#E0E0E0'),
                panel_background=p9.themes.elements.element_rect(fill=bgcolor),
                panel_border=p9.themes.elements.element_blank(),
                panel_grid_major=p9.themes.elements.element_line(
                    color='#D5D5D5', linetype='solid', size=1),
                panel_grid_minor=p9.themes.elements.element_blank(),
                plot_background=p9.themes.elements.element_rect(
                    fill=bgcolor, color=bgcolor, size=1),
                strip_background=p9.themes.elements.element_rect(size=0)),
            inplace=True)