# run_tests.py
import unittest


def run_smoke_tests():
    print("Running \033[93msmoke\033[0m💨 tests")
    loader = unittest.TestLoader()
    suite = loader.discover('tests/smoke')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def run_e2e_tests():
    print("Running \033[93me2e\033[0m🔚²🔚 tests")
    loader = unittest.TestLoader()
    suite = loader.discover('tests/e2e')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Run Selenium tests.")
    parser.add_argument('--smoke', action='store_true', help="Run smoke tests")
    parser.add_argument('--e2e', action='store_true', help="Run e2e tests")

    args = parser.parse_args()

    tests_to_run = []

    if args.smoke:
        tests_to_run.append(run_smoke_tests)

    if args.e2e:
        tests_to_run.append(run_e2e_tests)

    if not tests_to_run:
        tests_to_run.append(run_smoke_tests)
        tests_to_run.append(run_e2e_tests)

    for test in tests_to_run:
        test()
