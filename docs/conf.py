# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'Seatools'
copyright = '2024, dragons96'
author = 'dragons96'
release = '1.0.35'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = []

# -- Extension configuration -------------------------------------------------
autodoc_member_order = 'bysource'
