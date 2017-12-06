# -*- coding: utf-8 -*-
#
# Release Notes build configuration file, created by
# sphinx-quickstart on Thu Feb 12 02:10:34 2009.
#
# This file is execfile()d with the current directory set to its containing
# dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed
# automatically).
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.


# If your extensions are in another directory, add it here. If the directory
# is relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
import os
import sys
from datetime import datetime
sys.path.append(os.path.abspath('_ext'))


# Set this up to parse Django-driven code.
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..', '..',
                                                '..', 'djblets')))
sys.path.insert(0, os.path.dirname(__file__))

import reviewboard
from reviewboard.dependencies import django_doc_major_version


# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.intersphinx',
    'beanbag_docutils.sphinx.ext.django_utils',
    'beanbag_docutils.sphinx.ext.extlinks',
    'beanbag_docutils.sphinx.ext.http_role',
    'beanbag_docutils.sphinx.ext.intersphinx_utils',
    'beanbag_docutils.sphinx.ext.retina_images',
    'extralinks',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Release Notes'
copyright = u'2009-%s, Beanbag, Inc.' % datetime.now().year
bugtracker_url = 'https://www.reviewboard.org/bugs/%s'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '.'.join([str(i) for i in reviewboard.__version_info__[:2]])
# The full version, including alpha/beta/rc tags.
release = reviewboard.get_version_string()

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

suppress_warnings = ['ref.option']


# Options for HTML output
# -----------------------

html_theme = 'classic'

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'classic.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "Release Notes"

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
html_use_index = False

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'ReleaseNotes'


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class
# [howto/manual]).
latex_documents = [
  ('index', 'ReleaseNotes.tex', ur'Release Notes',
   ur'Christian Hammond', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True


# Check whether reviewboard.org intersphinx lookups should use the local
# server.
if os.getenv('DOCS_USE_LOCAL_RBWEBSITE') == '1':
    rbwebsite_url = 'http://localhost:8081'
else:
    rbwebsite_url = 'https://www.reviewboard.org'


# Add references for intersphinx and custom roles.
django_doc_base_url = ('http://django.readthedocs.io/en/%s.x/'
                       % django_doc_major_version)

intersphinx_mapping = {
    'django': (django_doc_base_url, None),
    'djblets0.9': ('%s/docs/djblets/0.9/' % rbwebsite_url, None),
    'djblets0.10': ('%s/docs/djblets/1.0/' % rbwebsite_url, None),
    'djblets1.0': ('%s/docs/djblets/1.0/' % rbwebsite_url, None),
    'python': ('https://docs.python.org/2.7', None),
    'rbt0.6': ('%s/docs/rbtools/0.6/' % rbwebsite_url, None),
    'rbt0.7': ('%s/docs/rbtools/0.7/' % rbwebsite_url, None),
    'rb-latest': ('%s/docs/rbtools/latest/' % rbwebsite_url, None),
    'rb1.7': ('%s/docs/manual/1.7/' % rbwebsite_url, None),
    'rb2.0': ('%s/docs/manual/2.0/' % rbwebsite_url, None),
    'rb2.5': ('%s/docs/manual/2.5/' % rbwebsite_url, None),
    'rb3.0': ('%s/docs/manual/3.0/' % rbwebsite_url, None),
}

extlinks = {
    'djangodoc': ('%s%%s.html' % django_doc_base_url, None),
    'backbonejs': ('http://backbonejs.org/#%s', 'Backbone.'),
    'rbintegration': ('https://www.reviewboard.org/integrations/%s', ''),
}
