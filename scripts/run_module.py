#!/usr/bin/env python3

import os
import sys
import subprocess

def run_sql_setup(module_name):
    sql_path = f"scripts/sql_setup/{module_name}.sql"
    if os.path.exists(sql_path):
        print(f"Running setup SQL for '{module_name}' from {sql_path}")
        try:
            subprocess.run(
                f"mysql -h 127.0.0.1 -P 3307 -u root --password=root < {sql_path}",
                shell=True,
                check=True,
                executable='/bin/bash'
            )
        except subprocess.CalledProcessError as e:
            print(f"SQL setup failed for '{module_name}': {e}")
            sys.exit(1)
    else:
        print(f"No SQL setup needed for '{module_name}'")

def run_test_module(module_name):
    settings_file = f"tests/singlestore_settings_{module_name}.py"
    settings = f"singlestore_settings_{module_name}" if os.path.exists(settings_file) else "singlestore_settings"

    print(f"Running tests for module: {module_name}")
    print(f"Using settings: {settings}")

    cmd = [
        "python", "tests/runtests.py",
        "--settings", settings,
        "--noinput", "-v", "3", module_name
    ]

    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Tests failed for module: {module_name}")
        sys.exit(result.returncode)
    else:
        print(f"Tests passed for module: {module_name}")

def main():
    if len(sys.argv) < 2:
        print("Usage: run_module.py <module1> [<module2> ...]")
        sys.exit(1)

    modules = sys.argv[1:]
    for module in modules:
        run_sql_setup(module)
        run_test_module(module)

if __name__ == "__main__":
    main()
