==============================
pygbif |version| documentation
==============================

|pypi| |docs| |ghactions| |coverage|

Python client for the `GBIF API
<http://www.gbif.org/developer/summary>`_

Source on GitHub at `sckott/pygbif <https://github.com/sckott/pygbif>`_

Getting help
============

Having trouble? Or want to know how to get started?

* Try the :doc:`FAQ <../docs/faq>` -- it's got answers to some common questions.
* Looking for specific information? Try the :ref:`genindex`
* Report bugs with pygbif in our `issue tracker`_.

.. _issue tracker: https://github.com/sckott/pygbif/issues


Installation
============

.. toctree::
   :caption: Installation
   :hidden:

   intro/install

:doc:`intro/install`
    How to install pygbif.


Docs
====

.. toctree::
   :caption: Docs
   :hidden:

   docs/faq
   docs/usecases

:doc:`docs/faq`
    Frequently asked questions.

:doc:`docs/usecases`
    Usecases for pygbif.


Modules
=======

.. toctree::
   :caption: Modules
   :hidden:

   modules/intro
   modules/caching
   modules/occurrence
   modules/registry
   modules/species
   modules/maps
   modules/utils

:doc:`modules/intro`
    Introduction to pygbif modules.

:doc:`modules/occurrence`
    The occurrence module: core GBIF occurrence data, including count, search, and download APIs.

:doc:`modules/registry`
    The registry module: including datasets, installations, networks, nodes, and organizations.

:doc:`modules/species`
    The species module: including name search, lookup, suggest, usage, and backbone search.

:doc:`modules/maps`
    The maps module: including map.

:doc:`modules/utils`
    The utils module: including wkt_rewind.

All the rest
============

.. toctree::
   :caption: All the rest
   :hidden:

   changelog_link
   contributors
   contributing
   conduct
   license

:doc:`changelog_link`
    See what has changed in recent pygbif versions.

:doc:`contributors`
    pygbif contributors.

:doc:`contributing`
    Learn how to contribute to the pygbif project.

:doc:`conduct`
    Expected behavior in this community. By participating in this project you agree to abide by its terms.

:doc:`license`
    The pygbif license.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |pypi| image:: https://img.shields.io/pypi/v/pygbif.svg
   :target: https://pypi.python.org/pypi/pygbif

.. |docs| image:: https://readthedocs.org/projects/pygbif/badge/?version=latest
   :target: http://pygbif.rtfd.org/

.. |ghactions| image:: https://github.com/sckott/pygbif/workflows/Python/badge.svg
   :target: https://github.com/sckott/pygbif/actions?query=workflow%3APython

.. |coverage| image:: https://codecov.io/gh/sckott/pygbif/branch/master/graph/badge.svg?token=frXPREGk1D
   :target: https://codecov.io/gh/sckott/pygbif
