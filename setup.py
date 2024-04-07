import codecs
from setuptools import setup
from setuptools import find_packages

with codecs.open("README.rst", "r", "utf-8") as f:
    readme = f.read().replace("\r", '')

with codecs.open("Changelog.rst", "r", "utf-8") as f:
    changes = f.read().replace("\r", '')
changes = changes.replace(":issue:", "")
long_description = readme + "\n\n" + changes

setup(
    name="pygbif",
    version="0.6.4",
    description="Python client for GBIF",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Scott Chamberlain",
    author_email="myrmecocystus@gmail.com",
    url="http://github.com/gbif/pygbif",
    download_url="https://github.com/gbif/pygbif/archive/refs/tags/v0.6.4.tar.gz",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    keywords = ['gbif', 'biodiversity', 'specimens', 'API', 'web-services', 'occurrences', 'species', 'taxonomy'],
)
