from setuptools import setup

setup(name='pygbif',
	version='0.0.5.9500',
	description='Python client for GBIF',
  author='Scott Chamberlain',
  author_email='myrmecocystus@gmail.com',
  url='http://github.com/sckott/pygbif',
  license="MIT",
  packages=['pygbif'],
  install_requires=['requests>2.7'],
  classifiers=(
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7'
	)
)
