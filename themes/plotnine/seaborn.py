import plotnine as p9

class Theme(p9.themes.theme):
    '''
    Theme for seaborn.

    Credit to Michael Waskom's seaborn:

        - http://stanford.edu/~mwaskom/software/seaborn
        - https://github.com/mwaskom/seaborn

    Parameters
    ----------
    style: str in ``['whitegrid', 'darkgrid', 'nogrid', 'ticks']``
        Style of axis background.
    context: str in ``['notebook', 'talk', 'paper', 'poster']``
        Intended context for resulting figures.
    font : str
        Font family, see matplotlib font manager.
    font_scale : float, optional
        Separate scaling factor to independently scale the
        size of the font elements.
    '''

    def __init__(self, style='darkgrid', context='notebook', font='sans-serif', font_scale=1):
        p9.themes.theme.__init__(self,
            aspect_ratio=p9.options.get_option('aspect_ratio'),
            dpi=p9.options.get_option('dpi'),
            figure_size=p9.options.get_option('figure_size'),
            panel_spacing=0.1,
            complete=True,
        )
        d = p9.themes.seaborn_rcmod.set(
            context=context,
            style=style,
            font=font,
            font_scale=font_scale,
        )
        self._rcParams.update(d)