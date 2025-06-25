import json
import sys

def run_group(group_id, modules):
    print(f"Running group {group_id} with modules: {modules}")
    for module in modules:
        print(f"Running module: {module}")
        # Add logic to run the module here

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_group.py <group_id>")
        sys.exit(1)

    group_id = int(sys.argv[1])
    with open("matrix.json") as f:
        matrix = json.load(f)
        modules = next(group["modules"] for group in matrix["include"] if group["group"] == group_id)
    run_group(group_id, modules)
