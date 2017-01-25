# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.pardir))

import gorilla


# -- General configuration ------------------------------------------------

needs_sphinx = '1.3'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = gorilla.__title__
version = gorilla.__version__
description = gorilla.__summary__
author = gorilla.__author__
copyright = "2014-%i, %s" % (datetime.utcnow().year, gorilla.__author__)
release = version
language = None

add_module_names = True
autodoc_member_order = 'bysource'
default_role = 'autolink'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
show_authors = False
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

html_theme = 'alabaster'
html_theme_options = {
    'description': description,
    'github_user': 'christophercrouzet',
    'github_repo': 'gorilla',
    'github_type': 'star',
    'fixed_sidebar': True,
}
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'links.html',
        'searchbox.html',
        'donate.html',
    ],
}
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = '%sdoc' % (project,)


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
}

latex_documents = [
    (master_doc, '%s.tex' % (project,), "%s Documentation" % (project,),
     author, 'manual'),
]


# -- Options for manual page output ---------------------------------------

man_pages = [
    (master_doc, project, "%s Documentation" % (project,), [author], 1),
]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (master_doc, project, "%s Documentation" % (project,), author, project,
     description, 'Miscellaneous'),
]
