import codecs
import re
from setuptools import setup
from setuptools import find_packages

version = ''
with open('pygbif/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with codecs.open('Changelog.rst', 'r', 'utf-8') as f:
    changes = f.read()

long_description = readme + '\n\n' + changes

setup(
  name             = 'pygbif',
	version          = version,
	description      = 'Python client for GBIF',
  long_description = long_description,
  author           = 'Scott Chamberlain',
  author_email     = 'myrmecocystus@gmail.com',
  url              = 'http://github.com/sckott/pygbif',
  license          = "MIT",
  packages         = find_packages(exclude=['test-*']),
  install_requires = ['requests>2.7'],
  classifiers      = (
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4'
	)
)
