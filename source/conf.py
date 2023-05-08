# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RouterOS7.6 中文使用手册'
copyright = '2023, be-engineer'
author = 'be-engineer'
release = '7.x'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # 'myst_parser',
    # 'recommonmark',
    #'sphinx_mdinclude',
    #'sphinxcontrib-markdown',
    # 'sphinx.ext.mathjax',
    #'sphinx_markdown_tables'
    # 'sphinxnotes.strike'
]

templates_path = ['_templates']
exclude_patterns = []

# root_doc = 'index'
language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
