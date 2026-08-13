"""
run_tests_with_coverage.py
---------------------------
Runs the unittest suite in tests/test_validators.py against
validators.py and prints:
  1. Standard unittest verbose output (PASS/FAIL per test).
  2. A statement-coverage report for validators.py, in a format
     modelled on coverage.py's console report (Name / Stmts / Miss / Cover).

The `coverage` and `pytest` PyPI packages are not installable in this
offline environment, so coverage is measured directly with Python's
built-in `sys.settrace` mechanism, tracking every executable source
line of validators.py that gets hit while the test suite runs.
"""

import io
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

TARGET_MODULE = "validators"
TARGET_FILE = os.path.join(ROOT, "validators.py")


def get_executable_lines(filename):
    """Return the set of line numbers in filename that are executable
    Python statements (skips blanks, comments, docstrings-as-statements
    are still counted since they do execute)."""
    import ast

    with open(filename, "r") as f:
        source = f.read()
    tree = ast.parse(source, filename=filename)
    lines = set()

    class Visitor(ast.NodeVisitor):
        def generic_visit(self, node):
            if hasattr(node, "lineno") and isinstance(
                node,
                (
                    ast.stmt,
                ),
            ):
                lines.add(node.lineno)
            super().generic_visit(node)

    Visitor().visit(tree)
    return lines


def main():
    executable_lines = get_executable_lines(TARGET_FILE)
    hit_lines = set()

    def tracer(frame, event, arg):
        if event == "line" and frame.f_code.co_filename == TARGET_FILE:
            hit_lines.add(frame.f_lineno)
        return tracer

    # Enable the tracer BEFORE anything imports validators.py, so that
    # its module-level statements (constants, regex compiles, etc.)
    # are counted too -- not just the function bodies exercised later.
    sys.settrace(tracer)

    if TARGET_MODULE in sys.modules:
        import importlib
        importlib.reload(sys.modules[TARGET_MODULE])

    # --- discover & run the unittest suite, capturing its normal output ---
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.join(ROOT, "tests"), pattern="test_*.py")

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)

    result = runner.run(suite)
    sys.settrace(None)

    test_output = stream.getvalue()
    print(test_output)

    # --- build the coverage.py-style report ---
    missed = sorted(executable_lines - hit_lines)
    covered = executable_lines & hit_lines
    total = len(executable_lines)
    pct = round(100 * len(covered) / total, 1) if total else 100.0

    print("=" * 70)
    print("COVERAGE REPORT  (statement coverage, custom stdlib tracer)")
    print("=" * 70)
    print(f"{'Name':<20}{'Stmts':>8}{'Miss':>8}{'Cover':>9}")
    print("-" * 70)
    name = "validators.py"
    print(f"{name:<20}{total:>8}{len(missed):>8}{str(pct)+'%':>9}")
    print("-" * 70)
    print(f"{'TOTAL':<20}{total:>8}{len(missed):>8}{str(pct)+'%':>9}")
    if missed:
        print(f"\nMissing lines: {missed}")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}   Failures: {len(result.failures)}   "
          f"Errors: {len(result.errors)}")
    print("RESULT:", "ALL TESTS PASSED ✅" if result.wasSuccessful() else "SOME TESTS FAILED ❌")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
