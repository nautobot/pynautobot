# Contributing

This section describes how to install *pynautobot* for development, how to run tests, and make sure you are a good contributor.

## Branches

- `main` - Reserved for released code
- `develop` - Planned next release code
- `<feature>` - Individual feature branches, should be based on and PR'd with `develop`

## Python Versions

This leverages Python 3.8 or later.

## Installing dependencies for local development

This repository uses [poetry](https://python-poetry.org/) for dependency management and [invoke](http://www.pyinvoke.org) for task execution. 

Follow these steps to set up your local development environment:

```bash
# Double check your version
$ python --version
Python 3.8.7
# Activate the Poetry environment, which will auto create the virtual environment related to the project
$ poetry shell
# Install project dependencies as well as development dependencies
$ poetry install
```

When you install dependencies via Poetry you will get invoke as part of the process.

## Invoke

Python Invoke provides a help context `invoke --list` to help identify possible commands to use. The invoke commands in turn execute the commands necessary to run the linting and unit tests.

## Running tests locally

1. Execute `poetry shell` to enter the virtual environment for the project
2. Execute `poetry install` to install the dependencies
3. Execute `invoke black --local` to execute the black style check
4. Execute `invoke pytest --local` to execute pytest


## Testing

All tests should be located within the `tests/` directory with `tests/unit` for the unit tests. Integration tests should be in the `tests/integration` directory.

### Testing - Required

The following linting tasks are required:

* [Black code style](https://github.com/psf/black)
* [Pylint](https://www.pylint.org)

### Testing Tools coming soon

* [Bandit](https://bandit.readthedocs.io/en/latest/)
* [Pydocstyle](https://github.com/PyCQA/pydocstyle/)
* [Yamllint](https://yamllint.readthedocs.io)
* [Flake8](https://flake8.pycqa.org/en/latest/)
  * Black vs Flake conflicts: When conflicts arise between Black and Flake8, Black should win and Flake8 should be configured as such

## Creating Changelog Fragments

All pull requests to `next` or `develop` must include a changelog fragment file in the `./changes` directory. To create a fragment, use your GitHub issue number and fragment type as the filename. For example, `2362.added`. Valid fragment types are `added`, `changed`, `deprecated`, `fixed`, `removed`, and `security`. The change summary is added to the file in plain text. Change summaries should be complete sentences, starting with a capital letter and ending with a period, and be in past tense. Each line of the change fragment will generate a single change entry in the release notes. Use multiple lines in the same file if your change needs to generate multiple release notes in the same category. If the change needs to create multiple entries in separate categories, create multiple files.

!!! example

    **Wrong**
    ```plaintext title="changes/1234.fixed"
    fix critical bug in documentation
    ```

    **Right**
    ```plaintext title="changes/1234.fixed"
    Fixed critical bug in documentation.
    ```

!!! example "Multiple Entry Example"

    This will generate 2 entries in the `fixed` category and one entry in the `changed` category.

    ```plaintext title="changes/1234.fixed"
    Fixed critical bug in documentation.
    Fixed release notes generation.
    ```

    ```plaintext title="changes/1234.changed"
    Changed release notes generation.
    ```
