import json
import sys
import subprocess

def run_group(modules):
    print(f"Running modules: {modules}")
    for module in modules:
        print(f"Running module: {module}")
        cmd = [
            "./testrepo/tests/runtests.py",
            "--settings=singlestore_settings",
            "--noinput",
            "-v", "3",
            module,
            "--keepdb"
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Module {module} failed with error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_group.py <modules_json>")
        sys.exit(1)

    modules = json.loads(sys.argv[1])
    run_group(modules)