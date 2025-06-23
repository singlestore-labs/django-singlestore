import os
import subprocess
from multiprocessing import Pool


TEST_MODULES = [d for d in os.listdir("tests") if os.path.isdir(os.path.join("tests", d))]
TEST_MODULES = [t for t in TEST_MODULES if t != "requirements" and t != "__pycache__"]
MAX_NUM_TEST_MODULES = 80
DEFAULT_OUT_FILE = "django_test_results/results.txt"
DEFAULT_SETTINGS = "singlestore_settings"


def run_single_test(module_name, out_file=None, settings=None):
    print(f"Running tests for {module_name}")
    if out_file is None:
        out_file = f"django_test_results/{module_name}.txt"
    if settings is None:
        settings = f"singlestore_settings_{module_name}"
    cmd = f"./tests/runtests.py --settings={settings} --noinput -v 3 {module_name} >> {out_file} 2>&1"
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    print(result.returncode)
    return result


def run_all_tests():

    with Pool(6) as workers:
        results = workers.map(run_single_test, TEST_MODULES)
    print(results)


def run_chunked_tests():
    current_tests = []
    for t in TEST_MODULES:
        current_tests.append(t)
        if len(current_tests) >= MAX_NUM_TEST_MODULES:
            module_name = " ".join(current_tests)
            run_single_test(module_name, DEFAULT_OUT_FILE, DEFAULT_SETTINGS)
            current_tests = []

    if len(current_tests) > 0:
        run_single_test(module_name, DEFAULT_OUT_FILE, DEFAULT_SETTINGS)


def analyze_results():
    ok_list = []
    fail_list = []
    total_tests = 0
    for f_name in os.listdir("django_test_results"):
        ok = False
        with open(os.path.join("django_test_results", f_name), "r") as f:
            all_lines = list(f.readlines())
            for ln in all_lines:
                if " tests in " in ln:
                    tokens = ln.strip().split(" ")
                    total_tests += int(tokens[1])
            lines = [line.strip() for line in all_lines[-3:]]
            lines = [line for line in lines if len(line)]

            for ln in lines:
                if "OK" in ln:
                    ok_list.append((f_name, lines))
                    ok = True
                    break
            if not ok:
                result = None
                for ln in lines:
                    if "FAILED" in ln:
                        result = ln
                fail_list.append((f_name, result))

    for elem in fail_list:
        print(elem)
    print(f"Total tests {total_tests}")


if __name__ == "__main__":
    analyze_results()
    # run_all_tests()
    # run_chunked_tests()
