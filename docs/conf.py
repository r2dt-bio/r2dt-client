"""Sphinx configuration."""
project = "R2DT API Client"
author = "Aleksei Naiden"
copyright = "2023, Aleksei Naiden"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
