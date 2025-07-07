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

os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_CONTENTTYPES"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_SITES"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_PREFETCH_RELATED"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_M2M_RECURSIVE"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_ADMIN_VIEWS"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FOREIGN_OBJECT"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_AUTH_TESTS"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_MANY_TO_MANY"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_FIXTURES_REGRESS"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_TABLE_STORAGE_TYPE_DELETE"] = "ROWSTORE REFERENCE"
os.environ["DJANGO_SINGLESTORE_NOT_ENFORCED_UNIQUE_QUERIES"] = "1"


def run_group(modules):
    print(f"Running modules: {modules}")
    failed = []
    for module in modules:
        print(f"Running module: {module}")
        cmd = [
            "./testrepo/tests/runtests.py",
            "--settings=singlestore_settings",
            "--noinput",
            "-v", "3",
            module,
            "--keepdb",
        ]
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
    if len(sys.argv) != 2:
        print("Usage: python run_group.py <modules_json>")
        sys.exit(1)

    modules = json.loads(sys.argv[1])
    run_group(modules)
