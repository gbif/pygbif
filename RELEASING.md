# Release process

_This is only of interest to the project maintainers._

This is based on the documentation at https://setuptools.pypa.io/en/latest/userguide/quickstart.html and https://packaging.python.org/en/latest/tutorials/packaging-projects/.

1. Install necessary tools and configure PyPI credentials

   - `pip3 install --upgrade setuptools build twine`
   - edit `~/.pypirc`
     ```
     [pypi]
     username = __token__
     password = <PyPI token>

     [testpypi]
     username = __token__
     password = <TestPyPI token>
     ```

2. Prepare the release

- Update `Changelog.rst` with a new section describing the changes in this release
- Change the version number in `setup.py`.  It is in the version line and the download_url line.
- Change the version number in `pygbif/package_metadata.py`
  - For a trial run, just use a version like "0.6.1.dev1".
  - Otherwise, commit and push the changes to both files.

3. Build and verify the package

- `rm -rf dist && python3 -m build`
- `python3 -m twine check dist/*`

4. Upload to PyPI Test:

- `python3 -m twine upload --repository testpypi dist/*`

5. Test the package in an empty virtual environment

- Wait 2-3 minutes for test.pypi.org to update
- `python3 -m venv test20220623-a`
- `source test20220623-a/bin/activate`
- `pip install --index-url https://test.pypi.org/simple/ --no-deps pygbif==0.6.1.dev1`
  (Installs only the pygbif release.)
- `pip install pygbif==0.6.1.dev1`
  (Installs dependencies.)
- `python`
  - `from pygbif import registry`
  - `registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')`

(Run other checks as required, e.g. any new or changed functionality.)

6. Don't rebuild the package, but upload what was already built to pypi.org:

- `python3 -m twine upload --repository pypi dist/*`

7. Create a release on GitHub

- Go to https://github.com/gbif/pygbif/releases and create a release, using a tag matching the `download_url` from step 2, e.g. `v0.6.1`.
