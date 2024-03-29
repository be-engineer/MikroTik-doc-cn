'''
Author: be-engineer 41234995@qq.com
Date: 2023-10-22 16:39:13
LastEditors: be-engineer 41234995@qq.com
LastEditTime: 2023-10-22 22:54:41
FilePath: /MikroTik-doc-cn/conf.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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
    'sphinx_mdinclude',
    # 'sphinxcontrib-markdown',
    # 'sphinx.ext.mathjax',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_markdown_tables',
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
