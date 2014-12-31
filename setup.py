from setuptools import setup

setup(name='pygbif',
	version='0.0.1',
	description='Python client for GBIF',
    author='Scott Chamberlain',
    author_email='myrmecocystus@gmail.com',
    url='http://github.com/sckott/pygbif',
    packages=['pygbif'],
    install_requires=['requests>2.0',
                      'pandas>0.1'],
    )
