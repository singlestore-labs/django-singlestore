import json
import os
import subprocess
import sys

import singlestoredb as s2

DJANGO_HOME = os.environ.get("DJANGO_HOME", os.path.join(os.getcwd(), "testrepo"))
DJANGO_SINGLESTORE_HOME = os.getcwd()
os.environ["DJANGO_HOME"] = DJANGO_HOME

os.environ["PYTHONPATH"] = (
    f"{DJANGO_HOME}:{DJANGO_HOME}/tests:{DJANGO_SINGLESTORE_HOME}/scripts:"
    + os.environ.get("PYTHONPATH", "")
)

# Default Django apps
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONTENTTYPES"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_SITES"] = "ROWSTORE REFERENCE"

# 12 many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_PREFETCH_RELATED"] = "ROWSTORE REFERENCE"

# models with many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CUSTOM_MANAGERS"] = "ROWSTORE REFERENCE"

# models with many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_WIDGETS"] = "ROWSTORE REFERENCE"

# models with many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_M2M_REGRESS"] = "ROWSTORE REFERENCE"

# many-to-many to self
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_M2M_RECURSIVE"] = "ROWSTORE REFERENCE"

# lots of many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_VIEWS"] = "ROWSTORE REFERENCE"

# have both M2M and O2O in the same model
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_MODELADMIN"] = "ROWSTORE REFERENCE"

# not important as we don't support it
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_DISTINCT_ON_FIELDS"] = "ROWSTORE REFERENCE"

# through model with multi level inheritance , unique and multi m2m
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_M2M_THROUGH_REGRESS"] = "ROWSTORE REFERENCE"

# multi M2M in the same models
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_M2M_SIGNALS"] = "ROWSTORE REFERENCE"

# M2M field and custom pk
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CUSTOM_PK"] = "ROWSTORE REFERENCE"

# multiple unique and o2o relationships
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_UTILS"] = "ROWSTORE REFERENCE"

# unique keys and many-to-many
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FOREIGN_OBJECT"] = "ROWSTORE REFERENCE"

# unique keys and many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_MODEL_INHERITANCE_REGRESS"] = "ROWSTORE REFERENCE"

# unique keys and many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_INLINES"] = "ROWSTORE REFERENCE"

# many many field with ordering
# TODO: check ordering works in default storage type
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_ORDERING"] = "ROWSTORE REFERENCE"

# lot of unique
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_VALIDATION"] = "ROWSTORE REFERENCE"

# multiple many-to-many fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FORMS_TESTS"] = "ROWSTORE REFERENCE"

# redirects_tests tests django.contrib.redirects application
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_REDIRECTS"] = "ROWSTORE REFERENCE"

# flatpages_tests tests django.contrib.flatpages application
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FLATPAGES"] = "ROWSTORE REFERENCE"

# migration file is aldready present with automatically generated intermediary model
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_SITES_FRAMEWORK"] = "ROWSTORE REFERENCE"

#  unique keys and many-to-many
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_MODEL_OPTIONS"] = "ROWSTORE REFERENCE"

# unique keys
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH_TESTS"] = "ROWSTORE REFERENCE"

# abstract models
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_MANY_TO_MANY"] = "ROWSTORE REFERENCE"

# models with unique keys and m2m fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FIXTURES_REGRESS"] = "ROWSTORE REFERENCE"

# deprecation module using django apps for testing Django’s deprecation policy
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FLATPAGES"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_REDIRECTS"] = "ROWSTORE REFERENCE"

# M2M field present with custom through
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_CHANGELIST"] = "ROWSTORE REFERENCE"

# m2m-related issue
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_DELETE"] = "ROWSTORE REFERENCE"

# lot of m2m fields
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_UNMANAGED_MODELS"] = "ROWSTORE REFERENCE"

# OneToOne relationships, disable enforced unique
os.environ["DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE_QUERIES"] = "1"


def create_databases():
    """Drops and recreates the required test databases to ensure they are empty."""
    print("--- Resetting test databases ---")
    password = os.environ.get("SINGLESTORE_PASSWORD", "")
    databases_to_create = ["test_django_db", "test_django_db_other"]

    try:
        with s2.connect(
            host="127.0.0.1", port=3306, user="root", password=password,
        ) as conn:
            with conn.cursor() as cur:
                for db_name in databases_to_create:
                    print(f"Dropping and recreating database '{db_name}' to ensure it is empty.")
                    cur.execute(f"DROP DATABASE IF EXISTS `{db_name}`;")
                    cur.execute(f"CREATE DATABASE `{db_name}`;")
        print("--- Test databases are ready ---")
    except Exception as e:
        print(f"FATAL: Failed to reset databases: {e}")
        sys.exit(1)


def setup_module(module):
    """Runs a setup SQL script for the given module if it exists."""
    sql_file = f"scripts/setup_sections/{module}_setup.sql"
    print(f"Checking for setup script: {sql_file}")
    if not os.path.exists(sql_file):
        # No setup script for this module.
        return

    print(f"--- Setting up for module '{module}' in both databases ---")
    password = os.environ.get("SINGLESTORE_PASSWORD", "")
    databases = ["test_django_db", "test_django_db_other"]

    try:
        with open(sql_file, 'r') as f:
            sql_script = f.read()

        sql_statements = [s.strip() for s in sql_script.split(';') if s.strip()]

        for db_name in databases:
            print(f"Executing setup script for module '{module}' in database '{db_name}'")
            with s2.connect(
                host="127.0.0.1",
                port=3306,
                user="root",
                password=password,
                database=db_name,
            ) as conn:
                with conn.cursor() as cur:
                    for statement in sql_statements:
                        cur.execute(statement)
            print(f"Successfully executed setup for module '{module}' in '{db_name}'.")
    except Exception as e:
        print(f"Failed to execute setup for module '{module}': {e}")
        sys.exit(1)


def run_group(modules, need_keep_db):
    print(f"Running modules: {modules}")
    failed = []
    for module in modules:
        create_databases()
        setup_module(module)

        print(f"--- Running tests for module: {module} ---")
        cmd = [
            f"{DJANGO_HOME}/tests/runtests.py",
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
