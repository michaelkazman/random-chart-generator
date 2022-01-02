import plotnine as p9
from copy import copy, deepcopy
from matplotlib import patheffects

class Theme(p9.themes.theme_gray):
    """
    xkcd theme

    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 12.
    scale : float, optional
        The amplitude of the wiggle perpendicular to the line
        (in pixels). Default is 1.
    length : float, optional
        The length of the wiggle along the line (in pixels).
        Default is 100.
    randomness : float, optional
        The factor by which the length is randomly scaled.
        Default is 2.
    stroke_size : float, optional
        Size of the stroke to apply to the lines and text paths.
        Default is 4.
    stroke_color : str or tuple, optional
        Color of the strokes. Default is ``white``.
        For no color, use ``'none'``.
    """
    def __init__(self, base_size=12, scale=1, length=100, randomness=2,
                 stroke_size=4, stroke_color='white'):
        p9.themes.theme_gray.__init__(self, base_size)
        self.add_theme(
            p9.themes.theme(
                text=p9.themes.elements.element_text(
                    family=['xkcd', 'Humor Sans', 'Comic Sans MS']),
                axis_ticks=p9.themes.elements.element_line(color='black', size=1.5),
                axis_ticks_minor=p9.themes.elements.element_blank(),
                axis_ticks_direction='in',
                axis_ticks_length_major=6,
                legend_background=p9.themes.elements.element_rect(
                    color='black', fill='None'),
                legend_key=p9.themes.elements.element_rect(fill='None'),
                panel_border=p9.themes.elements.element_rect(color='black', size=1.5),
                panel_grid=p9.themes.elements.element_blank(),
                panel_background=p9.themes.elements.element_rect(fill='white'),
                strip_background=p9.themes.elements.element_rect(
                    color='black', fill='white'),
                strip_background_x=p9.themes.elements.element_rect(width=2/3.),
                strip_background_y=p9.themes.elements.element_rect(height=2/3.),
                strip_margin=-0.5,
            ),
            inplace=True)

        d = {'axes.unicode_minus': False,
             'path.sketch':  (scale, length, randomness),
             'path.effects':  [
                 patheffects.withStroke(
                     linewidth=stroke_size,
                     foreground=stroke_color)]
             }
        self._rcParams.update(d)

    def __deepcopy__(self, memo):
        """
        Deep copy support for theme_xkcd
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        for key, item in old.items():
            if key == '_rcParams':
                continue
            new[key] = deepcopy(old[key], memo)

        result._rcParams = {}
        for k, v in self._rcParams.items():
            try:
                result._rcParams[k] = deepcopy(v, memo)
            except NotImplementedError:
                # deepcopy raises an error for objects that are
                # drived from or composed of
                # matplotlib.transform. TransformNode.
                # Not desirable, but probably requires upstream fix.
                # In particular, XKCD uses
                # matplotlib.patheffects.withStrok
                # -gdowding
                result._rcParams[k] = copy(v)

        return result