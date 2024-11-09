# tasks.py
import os
from pathlib import Path

from dotenv import load_dotenv
from invoke import task

# LOGIN TO HEROKU BEFORE STARTING ANY HEROKU TASKS

# Load environment variables from .env file
load_dotenv()

# ------------------------------------------------------------------------------------
# CONSTANT VARS
# ------------------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
SERVICE_NAME = "web"

DOCKER_COMPOSE_FILE = Path("development") / "docker-compose.yml"
CONTAINER_NAME = "dev-learningtracker-web-1"
DB_CONTAINER = "dev-learningtracker-db"
LOCAL_RUFF_EXCLUDE = (
    "./src/tests/*,./app/movies/migrations/*,tasks.py,./admin/settings.py"
)
# ------------------------------------------------------------------------------------
# DOCKER COMPOSE TASKS
# ------------------------------------------------------------------------------------
@task
def down(ctx, volumes=False):
    """Stop and remove Docker containers, with optional volume removal."""
    command = f"docker-compose -f {DOCKER_COMPOSE_FILE} down"
    if volumes:
        command += " -v"
    ctx.run(command, pty=True)


@task
def start(ctx):
    """Start Docker containers in detached mode."""
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} up -d", pty=True)


@task
def debug(ctx):
    """Start Docker containers in attached mode with rebuild."""
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} up --build", pty=True)


@task
def stop(ctx):
    """Stop running Docker containers."""
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} stop", pty=True)


@task
def restart(ctx):
    """Restart Docker containers."""
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} restart", pty=True)


@task
def logs(ctx, follow=False):
    """Show Docker container logs, with optional following."""
    command = f"docker-compose -f {DOCKER_COMPOSE_FILE} logs"
    if follow:
        command += " -f"
    ctx.run(command, pty=True)


@task
def build(ctx, no_cache=False):
    """Build Docker images."""
    command = f"docker-compose -f {DOCKER_COMPOSE_FILE} build"
    if no_cache:
        command += " --no-cache"
    ctx.run(command, pty=True)


@task
def build_no_cache(ctx):
    """Build Docker images without using cache."""
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} build --no-cache", pty=True)


@task
def remove_volumes(ctx):
    """Remove all Docker volumes."""
    ctx.run("docker volume prune -f", pty=True)


@task
def destroy(ctx):
    """Stop and remove Docker containers, and remove all associated volumes."""
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} down -v", pty=True)
    ctx.run("docker volume prune -f", pty=True)


@task
def createsuperuser(ctx):
    """Run 'python manage.py createsuperuser' inside the Docker container."""
    ctx.run(
        f"docker-compose -f {DOCKER_COMPOSE_FILE} exec {SERVICE_NAME} python /app/manage.py createsuperuser",
        pty=True,
    )
# ------------------------------------------------------------------------------------
# DOCKER CLI COMMANDS
# ------------------------------------------------------------------------------------

@task
def cli(ctx, shell="/bin/bash"):
    """Open a shell in the Docker container 'development-movies-1'."""
    ctx.run(f"docker exec -it {CONTAINER_NAME} {shell}", pty=True)

@task
def makemigrations(ctx, app: str= None):
    """Run 'python manage.py makemigrations' for the learningtracker app inside the Docker container."""
    base_command = f"docker-compose -f {DOCKER_COMPOSE_FILE} exec {SERVICE_NAME} python manage.py makemigrations"
    if app:
        base_command += app
    ctx.run(
        base_command,
        pty=True,
    )

@task
def migrate(ctx):
    """Run 'python manage.py migrate' inside the Docker container."""
    ctx.run(
        f"docker-compose -f {DOCKER_COMPOSE_FILE} exec {SERVICE_NAME} python /app/manage.py migrate",
        pty=True,
    )

@task
def showmigrations(ctx):
    """Show migrations status inside the Docker container."""
    ctx.run(
        f"docker-compose -f {DOCKER_COMPOSE_FILE} exec {SERVICE_NAME} python /app/manage.py showmigrations",
        pty=True,
    )

# ------------------------------------------------------------------------------------
# LOCAL TESTS AND LINT
# ------------------------------------------------------------------------------------
@task
def ruff(ctx, fix=False):
    """Run Ruff linter (use --fix to auto-fix)."""
    command = f"ruff check ."
    if fix:
        command += " --fix"
    ctx.run(command, pty=True)


@task
def black(ctx):
    """Run Black formatter."""
    ctx.run("black .")


@task
def pytest(ctx, coverage=False, testname=None):
    """
    Run tests with pytest.

    Args:
        coverage (bool): If True, run with code coverage.
        testname (str): A string to filter tests by name.
    """
    # Base command
    command = "pytest"

    # Add coverage option if specified
    if coverage:
        command += " --cov=src --cov-report=term-missing"

    # Add test name filter if specified
    if testname:
        command += f" -k {testname}"

    # Run the command
    ctx.run(command, pty=True)