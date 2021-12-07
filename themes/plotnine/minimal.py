import plotnine as p9

class Theme(p9.themes.theme_bw):
    """
    A minimalistic theme with no background annotations

    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 11.
    base_family : str, optional
        Base font family.
    """

    def __init__(self, base_size=11, base_family=None):
        p9.themes.theme_bw.__init__(self, base_size, base_family)
        self.add_theme(
            p9.themes.theme(legend_background=p9.themes.elements.element_blank(),
                  legend_key=p9.themes.elements.element_blank(),
                  panel_background=p9.themes.elements.element_blank(),
                  panel_border=p9.themes.elements.element_blank(),
                  strip_background=p9.themes.elements.element_blank(),
                  plot_background=p9.themes.elements.element_blank(),
                  axis_ticks=p9.themes.elements.element_blank(),
                  axis_ticks_length=12),
            inplace=True)
