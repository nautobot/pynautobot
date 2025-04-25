"""Tasks for use with Invoke."""

import os

from invoke.collection import Collection
from invoke.tasks import task as invoke_task


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.
    Examples
    --------
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg

    val = str(arg).lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"Invalid truthy value: `{arg}`")


# Use pyinvoke configuration for default values, see http://docs.pyinvoke.org/en/stable/concepts/configuration.html
# Variables may be overwritten in invoke.yml or by the environment variables INVOKE_PYNAUTOBOT_xxx
namespace = Collection("pynautobot")
namespace.configure(
    {
        "pynautobot": {
            "nautobot_ver": "stable",
            "project_name": "pynautobot",
            "python_ver": "3.12",
            "local": False,
            "compose_dir": os.path.join(os.path.dirname(__file__), "development"),
            "compose_files": ["docker-compose.yml"],
            "compose_http_timeout": "86400",
            "image_name": "pynautobot/nautobot",
        }
    }
)


# pylint: disable=keyword-arg-before-vararg
def task(function=None, *args, **kwargs):
    """Task decorator to override the default Invoke task decorator and add each task to the invoke namespace."""

    def task_wrapper(function=None):
        """Wrapper around invoke.task to add the task to the namespace as well."""
        if args or kwargs:
            task_func = invoke_task(*args, **kwargs)(function)
        else:
            task_func = invoke_task(function)
        namespace.add_task(task_func)
        return task_func

    if function:
        # The decorator was called with no arguments
        return task_wrapper(function)
    # The decorator was called with arguments
    return task_wrapper


def docker_compose(context, command, **kwargs):
    """Helper function for running a specific docker compose command with all appropriate parameters and environment.
    Args:
        context (obj): Used to run specific commands
        command (str): Command string to append to the "docker compose ..." command, such as "build", "up", etc.
        **kwargs: Passed through to the context.run() call.
    """
    build_env = {
        "NAUTOBOT_VER": context.pynautobot.nautobot_ver,
        "PYTHON_VER": context.pynautobot.python_ver,
        "IMAGE_NAME": context.pynautobot.image_name,
        "IMAGE_VER": f"{context.pynautobot.nautobot_ver}-py{context.pynautobot.python_ver}",
    }
    compose_command = f'docker compose --project-name {context.pynautobot.project_name} --project-directory "{context.pynautobot.compose_dir}"'
    for compose_file in context.pynautobot.compose_files:
        compose_file_path = os.path.join(context.pynautobot.compose_dir, compose_file)
        compose_command += f' -f "{compose_file_path}"'
    compose_command += f" {command}"
    print(f'Running docker compose command "{command}"')
    return context.run(compose_command, env=build_env, **kwargs)


def run_command(context, command, service="pynautobot-dev", port=None, **kwargs):
    """Wrapper to run a command locally or inside the nautobot container."""
    if is_truthy(context.pynautobot.local):
        context.run(command, **kwargs)
    else:
        # Check if nautobot is running, no need to start another nautobot container to run a command
        docker_compose_status = "ps --services --filter status=running"
        results = docker_compose(context, docker_compose_status, hide="out")
        publish = f" --publish {port}" if port else ""
        if service in results.stdout:
            compose_command = f"exec {service} {command}"
        else:
            compose_command = f"run --rm --entrypoint '{command}'{publish} {service} "

        docker_compose(context, compose_command, pty=True)


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------
@task(
    help={
        "force_rm": "Always remove intermediate containers",
        "cache": "Whether to use Docker's cache when building the image (defaults to enabled)",
    }
)
def build(context, force_rm=False, cache=True):
    """Build Nautobot docker image."""
    command = "build"

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    print(f"Building Nautobot with Python {context.pynautobot.python_ver}...")
    print(f"Nautobot Version: {context.pynautobot.nautobot_ver}")
    docker_compose(context, command)


# ------------------------------------------------------------------------------
# START / STOP / DEBUG
# ------------------------------------------------------------------------------
@task
def debug(context):
    """Start Nautobot and its dependencies in debug mode."""
    print("Starting Nautobot in debug mode...")
    docker_compose(context, "up")


@task
def start(context):
    """Start Nautobot and its dependencies in detached mode."""
    print("Starting Nautobot in detached mode...")
    docker_compose(context, "up --detach")


@task
def restart(context):
    """Gracefully restart all containers."""
    print("Restarting Nautobot...")
    docker_compose(context, "restart")


@task
def stop(context):
    """Stop Nautobot and its dependencies."""
    print("Stopping Nautobot...")
    docker_compose(context, "down")


@task
def destroy(context):
    """Destroy all containers and volumes."""
    print("Destroying Nautobot...")
    docker_compose(context, "down --volumes --remove-orphans")


@task(aliases=("unittest",))
def pytest(context, label="", failfast=False, keepdb=False, stdout=False):
    """Run pytest for the specified name and Python version.

    Args:
        context (obj): Used to run specific commands
        label (str): Label to run tests for
        failfast (bool): Stop on first failure
        keepdb (bool): Keep the database between test runs, not implemented yet, argument is necessary for upstream CI tests
        stdout (bool): Print the stdout of the pytest command
    """
    if keepdb:
        print("WARNING: `--keepdb` is not implemented yet, ignoring...")

    command = [
        "pytest -vv",
        "--maxfail=1" if failfast else "",
        label,
    ]
    if stdout:
        command.append("-s")
    if is_truthy(context.pynautobot.local):
        # No need to destroy the containers for local testing
        run_command(context, " ".join(command))
        return

    # Clean up from any previous failed runs
    destroy(context)
    # Run tests
    run_command(context, " ".join(command), service="pynautobot-dev-tests")
    # Clean up after successfully running tests
    destroy(context)


@task(aliases=("a",))
def autoformat(context):
    """Run code autoformatting."""
    ruff(context, action=["format"], fix=True)


@task(
    help={
        "action": "Available values are `['lint', 'format']`. Can be used multiple times. (default: `['lint', 'format']`)",
        "target": "File or directory to inspect, repeatable (default: all files in the project will be inspected)",
        "fix": "Automatically fix selected actions. May not be able to fix all issues found. (default: False)",
        "output_format": "See https://docs.astral.sh/ruff/settings/#output-format for details. (default: `concise`)",
    },
    iterable=["action", "target"],
)
def ruff(context, action=None, target=None, fix=False, output_format="concise"):
    """Run ruff to perform code formatting and/or linting."""
    if not action:
        action = ["lint", "format"]
    if not target:
        target = ["."]

    exit_code = 0

    if "format" in action:
        command = "ruff format "
        if not fix:
            command += "--check "
        command += " ".join(target)
        if not context.run(command, warn=True):
            exit_code = 1

    if "lint" in action:
        command = "ruff check "
        if fix:
            command += "--fix "
        command += f"--output-format {output_format} "
        command += " ".join(target)
        if not context.run(command, warn=True):
            exit_code = 1

    if exit_code != 0:
        raise Exit(code=exit_code)


@task
def pylint(context):
    """Run pylint for the specified name and Python version.

    Args:
        context (obj): Used to run specific commands
    """
    exec_cmd = "pylint **/*.py"
    run_command(context, exec_cmd)


@task
def yamllint(context):
    """Run yamllint to validate formatting adheres to NTC defined YAML standards.

    Args:
        context (obj): Used to run specific commands
    """
    exec_cmd = "yamllint ."
    run_command(context, exec_cmd)


@task
def pydocstyle(context):
    """Run pydocstyle to validate docstring formatting adheres to NTC defined standards.

    Args:
        context (obj): Used to run specific commands
    """
    exec_cmd = "pydocstyle ."
    run_command(context, exec_cmd)


@task
def bandit(context):
    """Run bandit to validate basic static code security analysis.

    Args:
        context (obj): Used to run specific commands
    """
    exec_cmd = "bandit --recursive ./ --configfile .bandit.yml"
    run_command(context, exec_cmd)


@task
def cli(context):
    """Enter the image to perform troubleshooting or dev work.

    Args:
        context (obj): Used to run specific commands
    """
    run_command(context, "bash")


@task
def tests(context):
    """Run all tests for the specified name and Python version.

    Args:
        context (obj): Used to run specific commands
    """
    ruff(context)
    pylint(context)
    yamllint(context)
    # Skipping due to using different doc strings atm.
    # pydocstyle(context)
    bandit(context)
    pytest(context)

    print("All tests have passed!")


@task
def docs(context):
    """Build and serve docs locally for development."""
    exec_cmd = "mkdocs serve -v --dev-addr=0.0.0.0:8001"
    run_command(context, exec_cmd, port="8001:8001")


@task
def check_migrations(_):
    """Upstream CI test runs check-migration test, but pynautobot has no migration to be tested; Hence including to pass CI test"""


@task(
    help={
        "version": "Version of pynautobot to generate the release notes for.",
    }
)
def generate_release_notes(context, version=""):
    """Generate Release Notes using Towncrier."""
    command = "poetry run towncrier build"
    if version:
        command += f" --version {version}"
    else:
        command += " --version `poetry version -s`"
    # Due to issues with git repo ownership in the containers, this must always run locally.
    context.run(command)
