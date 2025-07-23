import json
import os
import sys

DEFAULT_NUM_GROUPS_FOR_TESTS = 5


def get_test_modules(tests_root):
    subdirs_to_skip = {"import_error_package", "test_runner_apps", "__pycache__", "requirements", "gis_tests"}
    test_modules = []
    for item in os.listdir(tests_root):
        full_path = os.path.join(tests_root, item)
        if not os.path.isdir(full_path) or item in subdirs_to_skip:
            continue
        test_modules.append(item)
    return test_modules


def split_into_groups(modules, num_groups):
    groups = [[] for _ in range(num_groups)]
    for i, module in enumerate(modules):
        groups[i % num_groups].append(module)
    return groups


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tests_dir = sys.argv[1]
    else:
        tests_dir = "tests"

    if not os.path.isdir(tests_dir):
        print(f"Tests directory not found: {tests_dir}")
        sys.exit(1)

    modules = get_test_modules(tests_dir)
    num_groups = int(os.environ.get("NUM_GROUPS", DEFAULT_NUM_GROUPS_FOR_TESTS))
    groups = split_into_groups(modules, num_groups)
    matrix = {"include": [{"group": i, "modules": groups[i]} for i in range(num_groups)]}
    print(json.dumps(matrix))
