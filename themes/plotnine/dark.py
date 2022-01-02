import plotnine as p9

class Theme(p9.themes.theme_gray):
    '''
    The dark cousin of :class:`theme_light`, with similar line
    sizes but a dark background. Useful to make thin colored
    lines pop out.

    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 11.
    base_family : str, optional
        Base font family.
    '''

    def __init__(self, base_size=11, base_family=None):
        p9.theme_gray.__init__(self, base_size, base_family)
        self.add_theme(p9.themes.theme(
            axis_ticks=p9.themes.elements.element_line(color='#666666', size=0.5),
            axis_ticks_minor=p9.themes.elements.element_blank(),
            legend_key=p9.themes.elements.element_rect(
                fill='#7F7F7F', color='#666666', size=0.5),
            panel_background=p9.themes.elements.element_rect(fill='#7F7F7F', color='None'),
            panel_grid_major=p9.themes.elements.element_line(color='#666666', size=0.5),
            panel_grid_minor=p9.themes.elements.element_line(color='#737373', size=0.25),
            strip_background=p9.themes.elements.element_rect(fill='#333333', color='None'),
            strip_text_x=p9.themes.elements.element_text(color='white'),
            strip_text_y=p9.themes.elements.element_text(color='white', angle=-90)
        ), inplace=True)
