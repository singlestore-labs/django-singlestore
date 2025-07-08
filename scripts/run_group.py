import json
import os
import subprocess
import sys

DJANGO_HOME = os.path.join(os.getcwd(), "testrepo")
os.environ["DJANGO_HOME"] = DJANGO_HOME
os.environ["PYTHONPATH"] = (
    f"{DJANGO_HOME}:{DJANGO_HOME}/tests:{DJANGO_HOME}/tests/singlestore_settings:"
    + os.environ.get("PYTHONPATH", "")
)

# Default Django apps
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONTENTTYPES"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_SITES"] = "ROWSTORE REFERENCE"

# 12 many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_PREFETCH_RELATED"] = "ROWSTORE REFERENCE"

# many-to-many to self
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_M2M_RECURSIVE"] = "ROWSTORE REFERENCE"

# lots of many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_VIEWS"] = "ROWSTORE REFERENCE"

# unique keys and many-to-many
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FOREIGN_OBJECT"] = "ROWSTORE REFERENCE"

# unique keys
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH_TESTS"] = "ROWSTORE REFERENCE"

# abstract models
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_MANY_TO_MANY"] = "ROWSTORE REFERENCE"

# models with unique keys and m2m fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FIXTURES_REGRESS"] = "ROWSTORE REFERENCE"

# m2m-related issue
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_DELETE"] = "ROWSTORE REFERENCE"

# OneToOne relationships, disable enforced unique
os.environ["DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE_QUERIES"] = "1"


def setup_module(module, ):
    """Runs a setup SQL script for the given module if it exists."""
    sql_file = f"scripts/setup_section/{module}.sql"
    if not os.path.exists(sql_file):
        # No setup script for this module, which is fine.
        return

    print(f"--- Setting up for module '{module}' ---")
    password = os.environ.get("SINGLESTORE_PASSWORD", "")
    mysql_cmd = [
        "mysql",
        "-h", "127.0.0.1",
        "-P", "3306",
        "-u", "root",
        f"-p{password}",  # Attach password directly to -p
        "-e", f"source {sql_file}",
    ]
    try:
        result = subprocess.run(mysql_cmd, check=True, capture_output=True, text=True)
        print(f"Successfully executed setup for module '{module}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute setup for module '{module}': {e}")
        print(f"Stderr from failed setup: {e.stderr}")
        sys.exit(1)


def run_group(modules, need_keep_db):
    print(f"Running modules: {modules}")
    failed = []
    for module in modules:
        # Run setup for the specific module before running its tests.
        setup_module(module)

        print(f"--- Running tests for module: {module} ---")
        cmd = [
            "./testrepo/tests/runtests.py",
            "--settings=singlestore_settings",
            "--noinput",
            "-v", "3",
            module,
        ]
        if need_keep_db:
            cmd.append("--keepdb")

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Module {module} failed with error: {e}")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
            failed.append(module)
    if failed:
        print(f"\nThe following modules failed: {failed}")
        print(f"{len(failed)} out of {len(modules)} modules failed.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_group.py <modules_json>")
        print('Example: python run_group.py \'["aggregation", "auth_tests"]\' --keepdb')
        sys.exit(1)

    modules = json.loads(sys.argv[1])
    # Check if '--keepdb' flag is present in the arguments
    need_keep_db = "--keepdb" in sys.argv
    run_group(modules, need_keep_db)
