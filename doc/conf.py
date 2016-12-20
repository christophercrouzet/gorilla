# -*- coding: utf-8 -*-

import os
import sys

src_path = os.path.abspath(os.pardir)
if not src_path in sys.path:
    sys.path.insert(0, src_path)

import gorilla

import sphinx


# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode'
]

if sphinx.version_info >= (1, 3):
    extensions.append('sphinx.ext.napoleon')
else:
    extensions.append('sphinxcontrib.napoleon')

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'gorilla'
copyright = u'2014-2016, Christopher Crouzet'
version = gorilla.__version__
release = version

exclude_patterns = []
default_role = 'autolink'

add_module_names = True
show_authors = False

pygments_style = 'sphinx'
autodoc_member_order = 'bysource'


# -- Options for HTML output ----------------------------------------------

if os.environ.get('READTHEDOCS', None) != 'True':
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    except ImportError:
        pass

html_static_path = ['_static']
htmlhelp_basename = 'gorilladoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
}

latex_documents = [
    ('index', 'gorilla.tex', u'gorilla Documentation',
     u'Christopher Crouzet', 'manual')
]


# -- Options for manual page output ---------------------------------------

man_pages = [
    ('index', 'gorilla', u'gorilla Documentation',
     [u'Christopher Crouzet'], 1)
]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    ('index', 'gorilla', u'gorilla Documentation',
     u'Christopher Crouzet', 'gorilla',
     'Convenient approach to monkey patching.',
     'Miscellaneous')
]
