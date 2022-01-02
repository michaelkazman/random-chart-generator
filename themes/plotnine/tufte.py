import plotnine as p9

class Theme(p9.themes.theme_bw):
    '''
    Tufte Maximal Data, Minimal Ink Theme
    Theme based on Chapter 6 'Data-Ink Maximization and Graphical
    Design of Edward Tufte *The Visual Display of Quantitative
    Information*. No border, no axis lines, no grids. This theme
    works best in combination with :class:`geom_rug()` or
    :class:`geom_rangeframe()`.
    The default font family is set to 'serif' as he uses serif
    fonts for labels in 'The Visual Display of Quantitative
    Information'. The serif font used by Tufte in his books is
    a variant of Bembo, while the sans serif font is Gill Sans.
    If these fonts are installed on your system, consider setting
    them explicitly via the argument `base_family`.
    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 11.
    base_family : str, optional
        Base font family.
    ticks: logical, optional
        Show axis ticks?
    Tufte, Edward R. (2001) The Visual Display of Quantitative
    Information, Chapter 6.
    Translated from the R ggthemes package by hyiltiz <hyiltiz@gmail.com>.
    Released under GNU GPL v2 license or later.
    '''

    def __init__(self, base_size=11, base_family=None, ticks=True):
        p9.themes.theme_bw.__init__(self, base_size, base_family)
        self.add_theme(p9.themes.theme(
            legend_background=p9.themes.elements.element_blank(),
            legend_key=p9.themes.elements.element_blank(),
            panel_background=p9.themes.elements.element_blank(),
            panel_border=p9.themes.elements.element_blank(),
            strip_background=p9.themes.elements.element_blank(),
            plot_background=p9.themes.elements.element_blank(),
            axis_line=p9.themes.elements.element_blank(),
            panel_grid=p9.themes.elements.element_blank()
        ), inplace=True)

        if not ticks:
            self.add_theme(p9.themes.theme(
                axis_ticks=p9.themes.elements.element_blank()
                ), inplace=True)