import codecs
from setuptools import setup
from setuptools import find_packages

from pygbif import package_metadata

with codecs.open("README.rst", "r", "utf-8") as f:
    readme = f.read()

with codecs.open("Changelog.rst", "r", "utf-8") as f:
    changes = f.read()
changes = changes.replace(":issue:", "")
long_description = readme + "\n\n" + changes

setup(
    name="pygbif",
    version=package_metadata.__version__,
    description="Python client for GBIF",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Scott Chamberlain",
    author_email="myrmecocystus@gmail.com",
    url="http://github.com/sckott/pygbif",
    license="MIT",
    packages=find_packages(exclude=["test-*"]),
    install_requires=[
        "requests>2.7",
        "requests-cache",
        "geojson_rewind",
        "geomet",
        "appdirs>=1.4.3",
        "matplotlib",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
)
