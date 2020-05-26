.. _contributing:

Contributing
============


Bug reports
-----------

Please report bug reports on our `issue tracker`_.

.. _issue tracker: https://github.com/sckotr/pygbif/issues


Feature requests
----------------

Please put feature requests on our `issue tracker`_.


Pull requests
-------------

When you submit a PR you'll see a template that pops up - it's reproduced
here.


- Provide a general summary of your changes in the Title
- Describe your changes in detail
- If the PR closes an issue make sure include e.g., `fix #4` or similar,
  or if just relates to an issue make sure to mention it like `#4`
- If introducing a new feature or changing behavior of existing
  methods/functions, include an example if possible to do in brief form
- Did you remember to include tests? Unless you're changing docs/grammar,
  please include new tests for your change


Writing tests
-------------

We're using `nose` for testing. See the `nose docs`_ for help on
contributing to or writing tests.

Before running tests for the first time, you'll need install pygbif
dependencies, but also nose and a couple other packages:

.. code-block:: shell

    $ pip install -e .
    $ pip install nose vcrpy coverage

The Makefile has a task for testing under Python 3:

.. code-block:: shell

    $ make test

.. _nose docs: http://nose.readthedocs.io/en/latest/

Code formatting
---------------

We're using the `Black`_  formatter, so make sure you use that before
submitting code - there's lots of text editor integrations, a command
line tool, etc.

.. _Black: https://github.com/psf/black
