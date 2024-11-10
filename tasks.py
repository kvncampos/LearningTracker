# tasks.py
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
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')
# Configuration
DOCKER_FILE = "docker-compose-dev.yml" if DJANGO_ENV == "development" else "docker-compose.yml"
DOCKER_COMPOSE_FILE = Path("development") / DOCKER_FILE
FRONTEND_DIR = 'frontend'
BACKEND_DIR = 'backend'
SERVICE_NAME = "web"  # Ensure this matches your docker-compose.yml service name
CONTAINER_NAME = "dev-learningtracker-web-1"
DB_CONTAINER = "dev-learningtracker-db"
LOCAL_RUFF_EXCLUDE = (
    "./backend/tests/*,./backend/learningtracker/migrations,tasks.py,./backend/admin/settings.py"
)
################################################################################
#                               Backend Tasks
################################################################################

@task
def build_backend(ctx):
    """Build the Django backend Docker image."""
    print("Building Django backend Docker image...")
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} build", pty=True)

@task
def start_backend(ctx):
    """Start the Django backend and database."""
    print("Starting Django backend...")
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} up -d", pty=True)

@task
def stop_backend(ctx):
    """Stop the Django backend."""
    print("Stopping Django backend...")
    ctx.run(f"docker-compose -f {DOCKER_COMPOSE_FILE} down", pty=True)

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
    """Create a Django superuser."""
    with ctx.cd(BACKEND_DIR):
        ctx.run("python manage.py createsuperuser", pty=True)

@task
def backend_shell(ctx):
    """Open a Django shell in the Docker container."""
    ctx.run("docker-compose exec backend python manage.py shell", pty=True)

################################################################################
#                               FrontEnd Tasks
################################################################################
@task
def install_frontend(ctx):
    """Install frontend dependencies."""
    with ctx.cd(FRONTEND_DIR):
        print("Installing frontend dependencies...")
        ctx.run("npm install", pty=True)

@task
def start_frontend(ctx):
    """Start the React frontend development server."""
    with ctx.cd(FRONTEND_DIR):
        print("Starting React frontend...")
        ctx.run("npm start", pty=True)

@task
def build_frontend(ctx):
    """Build the React frontend for production."""
    with ctx.cd(FRONTEND_DIR):
        print("Building React frontend...")
        ctx.run("npm run build", pty=True)

@task
def stop_frontend(ctx):
    """Stop the React frontend."""
    print("Stopping React frontend...")
    # Find and kill the process running on port 3000 (React dev server)
    ctx.run("lsof -t -i :3000 | xargs kill -9", warn=True, pty=True)

@task
def start_frontend_debug(ctx):
    """
    Start React frontend in debug mode (with hot-reloading).
    """
    with ctx.cd(FRONTEND_DIR):
        print("Starting React frontend in debug mode...")
        ctx.run("npm start", pty=True)

@task
def clean_frontend(ctx):
    """Clean the frontend build directory."""
    with ctx.cd(FRONTEND_DIR):
        print("Cleaning frontend build directory...")
        ctx.run("rm -rf build", pty=True)

################################################################################
#                           Full Project Tasks
################################################################################
@task
def start(ctx):
    """Start both the Django backend and React frontend."""
    print("Starting backend and frontend...")
    start_backend(ctx)
    start_frontend(ctx)

@task
def stop(ctx):
    """Stop both the Django backend and React frontend."""
    print("Stopping backend and frontend...")
    stop_backend(ctx)
    stop_frontend(ctx)

@task
def build(ctx):
    """Build both the Django backend and React frontend."""
    build_backend(ctx)
    build_frontend(ctx)

@task
def install(ctx):
    """Install dependencies for both backend and frontend."""
    install_frontend(ctx)
    print("Dependencies installed for frontend.")

@task
def debug(ctx):
    """
    Start both Django backend and React frontend in debug mode.
    """
    print("Starting both backend and frontend in debug mode...")
    ctx.run("invoke start-backend-debug & invoke start-frontend-debug", pty=True)

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
        command += " --cov=backend --cov-report=term-missing"

    # Add test name filter if specified
    if testname:
        command += f" -k {testname}"

    # Run the command
    ctx.run(command, pty=True)

