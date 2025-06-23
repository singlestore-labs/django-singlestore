import os
import sys
import json


def get_test_modules(tests_root):
    subdirs_to_skip = {
        "": {"import_error_package", "test_runner_apps"},
        "gis_tests": {"data"},
    }

    test_modules = []

    for item in os.listdir(tests_root):
        full_path = os.path.join(tests_root, item)
        if not os.path.isdir(full_path):
            continue
        if item in subdirs_to_skip.get("", set()):
            continue
        if item == "__pycache__" or item == "requirements":
            continue
        test_modules.append(item)

    return test_modules

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tests_dir = sys.argv[1]
    else:
        tests_dir = "tests"

    if not os.path.isdir(tests_dir):
        print(f"Tests directory not found: {tests_dir}")
        sys.exit(1)

    modules = get_test_modules(tests_dir)
    matrix = {"include": [{"module": m} for m in modules]}
    print(json.dumps(matrix))
