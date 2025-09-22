# Testing Locally

## Testing Locally Overview

We provide the ability to run the tests locally to make sure the CI/CD pipeline will pass without having to wait for the CI/CD to run.

The tests are provided by enabling the environment using Poetry to provide the Invoke commands to run the tests.

## Invoke Tasks

You can get the list of available Invoke commands available for running the tests after launching `poetry shell`.

```shell
❯ poetry shell
```

```shell
❯ invoke --list
Available tasks:

  autoformat (a)           Run code autoformatting.
  build                    Build Nautobot docker image.
  check-migrations         Upstream CI test runs check-migration test, but pynautobot has no migration to be tested; Hence including to pass CI test.
  cli                      Enter the image to perform troubleshooting or dev work.
  debug                    Start Nautobot and its dependencies in debug mode.
  destroy                  Destroy all containers and volumes.
  docs                     Build and serve docs locally for development.
  generate-release-notes   Generate Release Notes using Towncrier.
  pylint                   Run pylint for the specified name and Python version.
  pytest (unittest)        Run pytest for the specified name and Python version.
  restart                  Gracefully restart all containers.
  ruff                     Run ruff to perform code formatting and/or linting.
  start                    Start Nautobot and its dependencies in detached mode.
  stop                     Stop Nautobot and its dependencies.
  tests                    Run all tests for the specified name and Python version.
  yamllint                 Run yamllint to validate formatting adheres to NTC defined YAML standards.
```

You can then run `invoke tests` to run the tests.

```
❯ invoke tests
```

## Using Environment Variables

You can use the following environment variables to test against different Python or Nautobot version.

- **INVOKE_PYNAUTOBOT_NAUTOBOT_VER**
- **INVOKE_PYNAUTOBOT_PYTHON_VER**

## Using Docker Compose Overrides

If you require changing any of the defaults found in `docker-compose.yml`, create a file inside the `development` directory called `docker-compose.override.yml` and add this file to the `compose_files` setting in your `invoke.yml` file, for example:

```yaml
pynautobot:
  compose_files:
    - "docker-compose.yml"
    - "docker-compose.override.yml"
```

This file will override any configuration in the main `docker-compose.yml` file, without making changes to the repository.

Please see the [official documentation on extending Docker Compose](https://docs.docker.com/compose/extends/) for more information.

## Using a Custom Nautobot Init File

If you require using a custom Nautobot init file, you can create a file inside the `development` directory called `nautobot.sql` and add this file to the `volumes` setting in your `docker-compose.override.yml` file, for example:

```yaml
---
services:
  postgres:
    volumes:
      - "./nautobot.sql:/docker-entrypoint-initdb.d/nautobot.sql"
```
