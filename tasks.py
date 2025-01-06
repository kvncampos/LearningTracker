import os
from pathlib import Path

from dotenv import load_dotenv
from invoke import task

# Load environment variables from .env file
load_dotenv()

# ------------------------------------------------------------------------------------
# CONSTANT VARS
# ------------------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
DJANGO_ENV = os.getenv("DJANGO_ENV", "development")
# Configuration
DOCKER_FILE = (
    "docker-compose-dev.yml" if DJANGO_ENV == "development" else "docker-compose.yml"
)
DOCKER_COMPOSE_FILE = Path("development") / DOCKER_FILE
CONTAINER_CHOICES = ["frontend", "backend"]
BACKEND_CONTAINER = "learningtracker-backend-1"
BACKEND_DIR = "backend"
FRONTEND_DIR = "frontend"
DB_CONTAINER = "dev-learningtracker-db"
LOCAL_RUFF_EXCLUDE = "./backend/tests/*,./backend/learningtracker/migrations,tasks.py,./backend/admin/settings.py"
PROJECT_NAME = os.getenv("PROJECT_NAME", "development")


################################################################################
#                               Backend Tasks
################################################################################
@task
def shell(ctx, container_name=""):
    """
    Log into the Docker container and start the Django ORM shell.

    Args:
        ctx: Invoke context.
        container_name (str): The name or ID of the Docker container.
    """
    if container_name in BACKEND_CONTAINER:
        # Log into the Docker container
        ctx.run(f"docker exec -it {BACKEND_CONTAINER} python manage.py shell", pty=True)
    elif container_name not in CONTAINER_CHOICES:
        print(f"Invalid container name. Must be {CONTAINER_CHOICES}")
    else:
        ctx.run(f"docker exec -it learningtracker-{container_name}-1 bash", pty=True)


@task
def start_backend_debug(ctx):
    """
    Start Django in debug mode (without Docker) for local development.
    """
    with ctx.cd(BACKEND_DIR):
        print("Starting Django backend in debug mode...")
        ctx.run("python manage.py runserver 0.0.0.0:8000", pty=True)


@task
def createsuperuser(ctx):
    """Create a Django superuser inside the Docker container."""
    print(f"Creating superuser in container: {BACKEND_CONTAINER}")
    ctx.run(
        f"docker exec -it {BACKEND_CONTAINER} python manage.py createsuperuser",
        pty=True,
    )


@task
def makemigrations(ctx, app: str | None = None):
    """Run 'python manage.py makemigrations' for the learningtracker app inside the Docker container."""
    base_command = (
        f"docker exec -it {BACKEND_CONTAINER} python /app/manage.py makemigrations"
    )
    if app:
        base_command += f" {app}"
    ctx.run(base_command, pty=True)


@task
def migrate(ctx):
    """Run 'python manage.py migrate' inside the Docker container."""
    ctx.run(
        f"docker exec -it {BACKEND_CONTAINER} python /app/manage.py migrate",
        pty=True,
    )


@task
def showmigrations(ctx):
    """Show migrations status inside the Docker container."""
    ctx.run(
        f"docker-compose -f {DOCKER_COMPOSE_FILE} -p {PROJECT_NAME} exec {BACKEND_CONTAINER} python /app/manage.py showmigrations",
        pty=True,
    )


################################################################################
#                           Full Project Tasks
################################################################################
@task
def start(ctx):
    """Start both the Django backend and React frontend."""
    print("Starting backend and frontend...")
    ctx.run(
        f"docker-compose -f {DOCKER_COMPOSE_FILE} -p {PROJECT_NAME} up -d", pty=True
    )


@task
def debug(ctx):
    """Start both the Django backend and React frontend."""
    print("Starting backend and frontend...")
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} -p {PROJECT_NAME} up", pty=True)


@task
def stop(ctx):
    """Stop both the Django backend and React frontend."""
    print("Stopping backend and frontend...")
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} -p {PROJECT_NAME} down", pty=True)


@task
def build(ctx):
    """Build both the Django backend and React frontend."""
    print(
        f"Building Docker Images for frontend and backend services using {DOCKER_COMPOSE_FILE}..."
    )
    ctx.run(
        f"docker-compose -f {DOCKER_COMPOSE_FILE} -p {PROJECT_NAME} build", pty=True
    )


@task
def destroy(ctx, remove_images=False, remove_volumes=False):
    """
    Destroy all containers, networks, and volumes related to the Docker Compose project.
    Optionally remove associated images and dangling volumes.
    """
    print(
        f"Stopping and removing Docker Compose containers for project {PROJECT_NAME}..."
    )
    ctx.run(
        f"docker-compose -f {DOCKER_COMPOSE_FILE} -p {PROJECT_NAME} down --volumes --remove-orphans",
        pty=True,
    )

    # Optional: Remove images associated with this project
    if remove_images:
        print("Removing Docker images associated with the project...")
        ctx.run(
            f"docker images --filter=reference='{PROJECT_NAME}_*' -q | xargs -r docker rmi"
        )

    # Optional: Remove dangling volumes
    if remove_volumes:
        print("Removing dangling Docker volumes associated with the project...")
        ctx.run(
            f"docker volume ls -q --filter=name='{PROJECT_NAME}_*' | xargs -r docker volume rm"
        )

    print("Docker Compose project resources have been destroyed.")


################################################################################
#                           Test & Linkt Project Tasks
################################################################################


@task
def ruff(ctx, fix: bool = False, filename: str | None = None):
    """
    Run Ruff on Python files in the project.

    Args:
        ctx: Invoke context.
        filename (str): Specific file or directory to check (default: backend/).
        fix (bool): Whether to auto-fix issues (default: False).
    """
    # Default to 'backend/' if no filename is provided
    target = filename or "backend/"

    # Use shorthand '-f' for fix
    fix_flag = "--fix" if fix else ""

    # Build and run the Ruff command
    command = f"ruff check {target} {fix_flag}"
    print(f"Running command: {command}")
    ctx.run(command, pty=True)


@task
def black(ctx, filename: str | None = None):
    """Run Black to format Python files in the project."""
    print("Running Black on Python files...")
    command = "black"
    if filename:
        command += filename
    else:
        command += " ."
    ctx.run(
        command,
        pty=True,
    )


@task
def pytest(
    ctx,
    coverage=False,
    report_type="term-missing",
    test_file=None,
    verbose=False,
    last_failed=False,
    disable_warnings=False,
    max_failures=None,
    debug=False,
):
    """
    Run Pytest tests with optional coverage reporting and popular flags.

    Args:
        coverage (bool): If True, run tests with coverage reporting.
        report_type (str): Coverage report type (default: 'term-missing').
        test_file (str): Path to a specific test file to run (e.g., 'test_models.py').
        verbose (bool): If True, increase verbosity (equivalent to pytest -v).
        last_failed (bool): If True, re-run only the last failed tests.
        disable_warnings (bool): If True, suppress warnings during test run.
        max_failures (int): Maximum number of failures before stopping the test run.
        debug (bool): Enables Print in Tests
    """
    print("Running Pytest tests...")

    # Base pytest command
    command = "pytest"

    # Add coverage options if enabled
    if coverage:
        command += f" --cov=backend --cov-report={report_type}"

    # Add specific test file if provided
    if test_file:
        command += f" backend/tests/{test_file}"

    # Additional popular pytest options
    if verbose:
        command += " -v"  # Increase verbosity
    if last_failed:
        command += " --lf"  # Re-run last failed tests
    if disable_warnings:
        command += " -p no:warnings"  # Suppress warnings
    if max_failures is not None:
        command += f" --maxfail={max_failures}"  # Limit failures before stopping
    if debug:
        command += " -s"

    print(f"Executing: {command}")
    ctx.run(command, pty=True)


@task
def test_and_lint(ctx):
    ruff(ctx, fix=True)
    black(ctx)
    pytest(ctx)
    print("All Tests and Lint Complete!")
