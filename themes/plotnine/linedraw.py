import plotnine as p9

class Theme(p9.themes.theme_gray):
    '''
    A theme with only black lines of various widths on white backgrounds

    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 11.
    base_family : str, optional
        Base font family.
    '''

    def __init__(self, base_size=11, base_family=None):
        p9.themes.theme_gray.__init__(self, base_size, base_family)
        self.add_theme(
            p9.themes.theme(
                axis_text=p9.themes.elements.element_text(color='black', size=base_size*0.8),
                axis_ticks=p9.themes.elements.element_line(color='black', size=0.5),
                axis_ticks_minor=p9.themes.elements.element_blank(),
                legend_key=p9.themes.elements.element_rect(color='black', size=0.5),
                panel_background=p9.themes.elements.element_rect(fill='white'),
                panel_border=p9.themes.elements.element_rect(fill='None', color='black', size=1),
                panel_grid_major=p9.themes.elements.element_line(color='black', size=0.1),
                panel_grid_minor=p9.themes.elements.element_line(color='black', size=0.02),
                strip_background=p9.themes.elements.element_rect(
                    fill='black', color='black', size=1
                ),
                strip_text_x=p9.themes.elements.element_text(color='white'),
                strip_text_y=p9.themes.elements.element_text(color='white', angle=-90),
            ),
            inplace=True,
        )
