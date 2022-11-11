import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# --------------------------------------------------------------------------------------

project = "nisystemlink"
copyright = "2020, National Instruments"
author = "National Instruments"

# The short X.Y version
version = "0.1"
# The full version, including alpha/beta/rc tags
release = "0.1.4"

# --------------------------------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "docs.cleanup",
]
master_doc = "index"

html_theme = "sphinx_rtd_theme"
html_extra_path = [
    "../LICENSE",
]
nitpicky = True
nitpick_ignore = [
    ("py:class", "datetime.datetime"),
    ("py:class", "datetime.timedelta"),
    ("py:class", "pathlib.Path"),
    ("py:data", "typing.Any"),
    ("py:data", "typing.Awaitable"),
    ("py:data", "typing.Dict"),
    ("py:data", "typing.Iterable"),
    ("py:data", "typing.List"),
    ("py:data", "typing.Optional"),
    ("py:data", "typing.Sequence"),
    ("py:data", "typing.Tuple"),
    ("py:data", "typing.Union"),
]
autodoc_default_options = {
    "special-members": "__init__",
    "no-private-members": True,
}
# Don't let napoleon force methods to be included in the docs; use autodoc flags and our
# own docs.cleanup module for that.
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
