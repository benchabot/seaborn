import re
import pydoc
from .external.docscrape import NumpyDocString


class DocstringComponents:

    regexp = re.compile(r"\n((\n|.)+)\n\s*", re.MULTILINE)

    def __init__(self, comp_dict, strip_whitespace=True):
        """Read entries from a dict, optionally stripping outer whitespace."""
        if strip_whitespace:
            entries = {}
            for key, val in comp_dict.items():
                m = re.match(self.regexp, val)
                if m is None:
                    entries[key] = val
                else:
                    entries[key] = m.group(1)
        else:
            entries = comp_dict.copy()

        self.entries = entries

    def __getattr__(self, attr):
        """Provided dot access to entries."""
        if attr in self.entries:
            return self.entries[attr]
        else:
            return self.__getattribute__(attr)

    @classmethod
    def from_nested_components(cls, **kwargs):
        """Add multiple sub-sets of components."""
        return cls(kwargs, strip_whitespace=False)

    @classmethod
    def from_function_params(cls, func):
        """Use the numpydoc parser to extract components from existing func."""
        params = NumpyDocString(pydoc.getdoc(func))["Parameters"]
        comp_dict = {}
        for p in params:
            name = p.name
            type = p.type
            desc = "    \n".join(p.desc)
            comp_dict[name] = f"{name} : {type}\n    {desc}"

        return cls(comp_dict)


# TODO is "vector" the best term here? We mean to imply 1D data with a variety
# of types, but vectors are actually 2D (row or columns...)

_core_params = dict(
    data="""
data : :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
    Input data structure. Either a long-form collection of vectors that can be
    assigned to named variables or a wide-form dataset that will be internally
    reshaped.
    """,  # TODO add link to user guide narrative when exists
    xy="""
x, y : vectors or keys in ``data``
    Variables that specify positions on the x and y axes.
    """,
    hue="""
hue : vector or key in ``data``
    Semantic variable that is mapped to determine the color of plot elements.
    """,
    palette="""
palette : string, list, dict, or :class:`matplotlib.colors.Colormap`
    Method for choosing the colors to use when mapping the ``hue`` semantic.
    String values are passed to :func:`color_palette`. List or dict values
    imply categorical mapping, while a colormap object implies numeric mapping.
    """,  # noqa: E501
    hue_order="""
hue_order : vector of strings
    Specify the order of processing and plotting for categorical levels of the
    ``hue`` semantic.
    """,
    hue_norm="""
hue_norm : tuple or :class:`matplotlib.colors.Normalize`
    Either a pair of values that set the normalization range in data units
    for numeric ``hue`` mapping. Can also be an object that will map from data
    units into a [0, 1] interval. Usage implies numeric mapping.
    """,
    color="""
color : :mod:`matplotlib color <matplotlib.colors>`
    Single color specification for when hue mapping is not used. Otherwise, the
    plot will try to hook into the matplotlib property cycle.
    """,
    ax="""
ax : :class:`matplotlib.axes.Axes`
    Pre-existing axes for the plot. Otherwise, call :func:`matplotlib.pyplot.gca`
    internally.
    """,  # noqa: E501
)


_core_returns = dict(
    ax="""
ax : :class:`matplotlib.axes.Axes`
    The matplotlib axes containing the plot.
    """,
)


_seealso_blurbs = dict(

    # Distribution plots
    rugplot="""
rugplot : Plot a tick at each observation value along the x and/or y axes.
    """,

    # Categorical plots
    violinplot="""
violinplot : Draw an enhanced boxplot using kernel density estimation.
    """,

    # Multiples
    jointplot="""
jointplot : Draw a bivariate plot with univariate marginal distributions.
    """,
)


_core_docs = dict(
    params=DocstringComponents(_core_params),
    returns=DocstringComponents(_core_returns),
    seealso=DocstringComponents(_seealso_blurbs),
)