"""
test_validators.py
-------------------
Automated unit tests for the CSMS validation / business-logic layer
(validators.py), written to satisfy the Lab 2 requirement:

    "develop automated unit tests to verify that your implementation
    satisfies the requirements [of the Lab 1 SRS]."

The test suite is organised to mirror Lab 1 Part B:
    - EquivalencePartitioning*   -> Activity 1
    - BoundaryValue*             -> Activity 2
    - DecisionTable*             -> Activity 3
    - TestCaseDesign*            -> Activity 4 (>= 15 traceable cases,
                                     each docstring references a TC id
                                     and requirement, matching the table
                                     students were asked to submit)

Run with:
    python3 -m unittest -v tests.test_validators
or use tools/run_tests_with_coverage.py for a coverage report.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import validators as v


# ===========================================================================
# Activity 1 — Equivalence Partitioning
# ===========================================================================
class EquivalencePartitioningStudentID(unittest.TestCase):
    """R1, R2 — Student ID equivalence classes."""

    def test_valid_8_digits(self):
        self.assertTrue(v.validate_student_id("02230123")[0])

    def test_invalid_too_short(self):
        self.assertFalse(v.validate_student_id("2230123")[0])

    def test_invalid_contains_letters(self):
        self.assertFalse(v.validate_student_id("0223ABCD")[0])

    def test_invalid_too_long(self):
        self.assertFalse(v.validate_student_id("022301234")[0])

    def test_invalid_empty(self):
        self.assertFalse(v.validate_student_id("")[0])

    def test_invalid_none(self):
        self.assertFalse(v.validate_student_id(None)[0])


class EquivalencePartitioningPassword(unittest.TestCase):
    """R3, R4 — Password equivalence classes (length + character types)."""

    def test_valid_password(self):
        self.assertTrue(v.validate_password("Passw0rd")[0])

    def test_invalid_below_min_length(self):
        self.assertFalse(v.validate_password("Pas0rd")[0])  # 6 chars

    def test_invalid_above_max_length(self):
        self.assertFalse(v.validate_password("Passw0rdExtra1")[0])  # 14 chars

    def test_invalid_missing_uppercase(self):
        self.assertFalse(v.validate_password("passw0rd")[0])

    def test_invalid_missing_lowercase(self):
        self.assertFalse(v.validate_password("PASSW0RD")[0])

    def test_invalid_missing_number(self):
        self.assertFalse(v.validate_password("Password")[0])

    def test_invalid_empty(self):
        self.assertFalse(v.validate_password("")[0])


class EquivalencePartitioningPaymentScreenshot(unittest.TestCase):
    """R6 — Payment screenshot: file type + presence."""

    def test_valid_jpg(self):
        self.assertTrue(v.validate_payment_screenshot("receipt.jpg")[0])

    def test_valid_jpeg(self):
        self.assertTrue(v.validate_payment_screenshot("receipt.jpeg")[0])

    def test_valid_png(self):
        self.assertTrue(v.validate_payment_screenshot("receipt.PNG")[0])  # case-insensitive

    def test_invalid_pdf_extension(self):
        self.assertFalse(v.validate_payment_screenshot("receipt.pdf")[0])

    def test_invalid_no_extension(self):
        self.assertFalse(v.validate_payment_screenshot("receipt")[0])

    def test_invalid_missing_file(self):
        self.assertFalse(v.validate_payment_screenshot("")[0])
        self.assertFalse(v.validate_payment_screenshot(None)[0])


class EquivalencePartitioningTransactionNumber(unittest.TestCase):
    """R7 — Transaction number: 3 digits - 9 digits (13 chars)."""

    def test_valid_format(self):
        self.assertTrue(v.validate_transaction_number("123-123456789")[0])

    def test_invalid_missing_hyphen(self):
        self.assertFalse(v.validate_transaction_number("123123456789")[0])

    def test_invalid_letters_in_number(self):
        self.assertFalse(v.validate_transaction_number("12A-123456789")[0])

    def test_invalid_too_short(self):
        self.assertFalse(v.validate_transaction_number("123-12345678")[0])

    def test_invalid_empty(self):
        self.assertFalse(v.validate_transaction_number("")[0])


# ===========================================================================
# Activity 2 — Boundary Value Analysis
# ===========================================================================
class BoundaryValueStudentID(unittest.TestCase):
    """R2 boundaries: 7 / 8 / 9 digits."""

    def test_7_digits_invalid(self):
        self.assertFalse(v.validate_student_id("1234567")[0])

    def test_8_digits_valid(self):
        self.assertTrue(v.validate_student_id("12345678")[0])

    def test_9_digits_invalid(self):
        self.assertFalse(v.validate_student_id("123456789")[0])


class BoundaryValuePassword(unittest.TestCase):
    """R4 boundaries: 7,8,9 (lower) and 11,12,13 (upper). Content otherwise valid."""

    def test_7_chars_invalid(self):
        self.assertFalse(v.validate_password("Pas0rdA")[0])          # 7

    def test_8_chars_valid(self):
        self.assertTrue(v.validate_password("Passw0rd")[0])          # 8

    def test_9_chars_valid(self):
        self.assertTrue(v.validate_password("Passw0rd9")[0])         # 9

    def test_11_chars_valid(self):
        self.assertTrue(v.validate_password("Passw0rd991")[0])       # 11

    def test_12_chars_valid(self):
        self.assertTrue(v.validate_password("Passw0rd9912")[0])      # 12

    def test_13_chars_invalid(self):
        self.assertFalse(v.validate_password("Passw0rd99123")[0])    # 13


class BoundaryValueTransactionNumber(unittest.TestCase):
    """R7 boundaries: 12 / 13 / 14 characters around the fixed format."""

    def test_12_chars_one_digit_short_invalid(self):
        self.assertFalse(v.validate_transaction_number("123-12345678")[0])  # 12

    def test_13_chars_correct_pattern_valid(self):
        self.assertTrue(v.validate_transaction_number("123-123456789")[0])  # 13

    def test_14_chars_one_digit_too_many_invalid(self):
        self.assertFalse(v.validate_transaction_number("123-1234567890")[0])  # 14


# ===========================================================================
# Activity 3 — Decision Table Testing (registration eligibility)
# ===========================================================================
class DecisionTableRegistration(unittest.TestCase):
    """All 8 combinations of Payment / Drug Test / Period, exact messages."""

    def test_TNN_all_true_allowed(self):
        ok, msg = v.check_registration_eligibility(True, True, True)
        self.assertTrue(ok)
        self.assertEqual(msg, "Registration Allowed")

    def test_row2_payment_fail_only(self):
        ok, msg = v.check_registration_eligibility(False, True, True)
        self.assertFalse(ok)
        self.assertEqual(msg, "Tuition payment not verified.")

    def test_row3_drugtest_fail_only(self):
        ok, msg = v.check_registration_eligibility(True, False, True)
        self.assertFalse(ok)
        self.assertEqual(msg, "Drug testing report not verified.")

    def test_row4_period_fail_only(self):
        ok, msg = v.check_registration_eligibility(True, True, False)
        self.assertFalse(ok)
        self.assertEqual(msg, "Registration period is closed.")

    def test_row5_payment_and_drugtest_fail_shows_payment_msg(self):
        ok, msg = v.check_registration_eligibility(False, False, True)
        self.assertFalse(ok)
        self.assertEqual(msg, "Tuition payment not verified.")

    def test_row6_payment_and_period_fail_shows_payment_msg(self):
        ok, msg = v.check_registration_eligibility(False, True, False)
        self.assertFalse(ok)
        self.assertEqual(msg, "Tuition payment not verified.")

    def test_row7_drugtest_and_period_fail_shows_drugtest_msg(self):
        ok, msg = v.check_registration_eligibility(True, False, False)
        self.assertFalse(ok)
        self.assertEqual(msg, "Drug testing report not verified.")

    def test_row8_all_false_shows_payment_msg(self):
        ok, msg = v.check_registration_eligibility(False, False, False)
        self.assertFalse(ok)
        self.assertEqual(msg, "Tuition payment not verified.")


# ===========================================================================
# Activity 4 — Test Case Design (>= 15 traceable test cases)
# ===========================================================================
class TestCaseDesign(unittest.TestCase):
    """
    Each test method corresponds to one row of the Activity 4 test-case
    table (TC01 .. TC20). The docstring states: Requirement | Input | Expected.
    """

    # ---- Login / Student ID / Password ----
    def test_TC01_R2_valid_student_id(self):
        """TC01 | R2 | Student ID = 02230123 | Accepted"""
        self.assertTrue(v.validate_student_id("02230123")[0])

    def test_TC02_R1_missing_student_id(self):
        """TC02 | R1 | Student ID = '' | Rejected: mandatory"""
        ok, msg = v.validate_student_id("")
        self.assertFalse(ok)
        self.assertIn("mandatory", msg)

    def test_TC03_R2_student_id_with_letters(self):
        """TC03 | R2 | Student ID = 0223ABCD | Rejected: digits only"""
        self.assertFalse(v.validate_student_id("0223ABCD")[0])

    def test_TC04_R4_valid_password(self):
        """TC04 | R4 | Password = Passw0rd | Accepted"""
        self.assertTrue(v.validate_password("Passw0rd")[0])

    def test_TC05_R3_missing_password(self):
        """TC05 | R3 | Password = '' | Rejected: mandatory"""
        ok, msg = v.validate_password("")
        self.assertFalse(ok)
        self.assertIn("mandatory", msg)

    def test_TC06_R4_password_too_short(self):
        """TC06 | R4 | Password = Pw0rd1 (6 chars) | Rejected: too short"""
        self.assertFalse(v.validate_password("Pw0rd1")[0])

    def test_TC07_login_success(self):
        """TC07 | R1-R4 | Correct ID + Password | Login successful"""
        db = {"02240360": "Passw0rd1"}
        ok, msg = v.login("02240360", "Passw0rd1", db)
        self.assertTrue(ok)
        self.assertEqual(msg, "Login successful.")

    def test_TC08_login_wrong_password(self):
        """TC08 | R1-R4 | Correct ID, wrong password | Login rejected"""
        db = {"02240360": "Passw0rd1"}
        ok, msg = v.login("02240360", "WrongPass9", db)
        self.assertFalse(ok)
        self.assertEqual(msg, "Incorrect Student ID or Password.")

    def test_TC08b_login_invalid_student_id_short_circuits(self):
        """TC08b | R1-R2 | Student ID = '123' | Login rejected before password is checked"""
        db = {"02240360": "Passw0rd1"}
        ok, msg = v.login("123", "Passw0rd1", db)
        self.assertFalse(ok)
        self.assertIn("Student ID", msg)

    def test_TC08c_login_invalid_password_short_circuits(self):
        """TC08c | R3-R4 | Valid ID, weak password 'weak' | Login rejected before DB lookup"""
        db = {"02240360": "Passw0rd1"}
        ok, msg = v.login("02240360", "weak", db)
        self.assertFalse(ok)
        self.assertIn("Password", msg)

    # ---- Payment screenshot / transaction number ----
    def test_TC09_R6_valid_screenshot_type(self):
        """TC09 | R6 | screenshot.png | Accepted"""
        self.assertTrue(v.validate_payment_screenshot("screenshot.png")[0])

    def test_TC10_R6_invalid_screenshot_type(self):
        """TC10 | R6 | screenshot.docx | Rejected: invalid type"""
        self.assertFalse(v.validate_payment_screenshot("screenshot.docx")[0])

    def test_TC11_R7_valid_transaction_number(self):
        """TC11 | R7 | 123-123456789 | Accepted"""
        self.assertTrue(v.validate_transaction_number("123-123456789")[0])

    def test_TC12_R7_invalid_transaction_number_format(self):
        """TC12 | R7 | 12-1234567890 (wrong grouping) | Rejected"""
        self.assertFalse(v.validate_transaction_number("12-1234567890")[0])

    # ---- Payment verification (R8, R9) ----
    def test_TC13_R8_payment_verified_generates_receipt(self):
        """TC13 | R8 | upload complete + verified by college | Receipt generated"""
        result = v.verify_payment(upload_complete=True, verified_by_college=True)
        self.assertTrue(result["receipt_generated"])
        self.assertEqual(result["status"], "verified")

    def test_TC14_R9_payment_not_verified_stays_incomplete(self):
        """TC14 | R9 | upload complete but NOT verified | Registration stays incomplete"""
        result = v.verify_payment(upload_complete=True, verified_by_college=False)
        self.assertFalse(result["receipt_generated"])
        self.assertEqual(result["status"], "incomplete")

    def test_TC15_R9_incomplete_upload_stays_incomplete(self):
        """TC15 | R9 | upload incomplete | Registration stays incomplete"""
        result = v.verify_payment(upload_complete=False, verified_by_college=True)
        self.assertFalse(result["receipt_generated"])
        self.assertEqual(result["status"], "incomplete")

    # ---- Drug testing report / duplicate module / registration conditions ----
    def test_TC16_registration_all_conditions_met(self):
        """TC16 | Activity 3 row 1 | payment=Y, drugtest=Y, period=Y | Registration Allowed"""
        ok, msg = v.check_registration_eligibility(True, True, True)
        self.assertTrue(ok)
        self.assertEqual(msg, "Registration Allowed")

    def test_TC17_duplicate_module_registration_rejected(self):
        """TC17 | Section 2 | Register SWE302 twice | Second attempt rejected"""
        modules = []
        ok1, _ = v.register_module(modules, "SWE302")
        ok2, msg2 = v.register_module(modules, "SWE302")
        self.assertTrue(ok1)
        self.assertFalse(ok2)
        self.assertIn("Duplicate registration", msg2)

    def test_TC18_module_registration_success(self):
        """TC18 | Section 2 | Register SWE301 (new module) | Registered successfully"""
        modules = ["SWE302"]
        ok, msg = v.register_module(modules, "SWE301")
        self.assertTrue(ok)
        self.assertIn("registered successfully", msg)

    # ---- Result viewing ----
    def test_TC19_result_view_registered_student(self):
        """TC19 | Section 4 | is_registered=True | Access granted"""
        ok, data = v.get_results(True, [{"module_code": "SWE302", "module_title": "SWE QA", "grade": "A"}])
        self.assertTrue(ok)
        self.assertEqual(len(data), 1)

    def test_TC20_result_view_unregistered_student_blocked(self):
        """TC20 | Section 4 | is_registered=False | Access denied"""
        ok, msg = v.get_results(False, [])
        self.assertFalse(ok)
        self.assertIn("Only registered students", msg)


# ===========================================================================
# Additional coverage: payment method (R5) and aggregate submit_payment()
# ===========================================================================
class PaymentMethodAndSubmission(unittest.TestCase):
    def test_valid_mobile_banking(self):
        self.assertTrue(v.validate_payment_method("Mobile Banking")[0])

    def test_invalid_cash_method(self):
        self.assertFalse(v.validate_payment_method("Cash")[0])

    def test_invalid_empty_method(self):
        self.assertFalse(v.validate_payment_method("")[0])

    def test_submit_payment_all_valid(self):
        ok, msg = v.submit_payment("Mobile Banking", "proof.jpg", "123-123456789")
        self.assertTrue(ok)

    def test_submit_payment_bad_method_short_circuits(self):
        ok, msg = v.submit_payment("Cash", "proof.jpg", "123-123456789")
        self.assertFalse(ok)
        self.assertIn("Mobile Banking", msg)

    def test_submit_payment_bad_screenshot(self):
        ok, msg = v.submit_payment("Mobile Banking", "proof.pdf", "123-123456789")
        self.assertFalse(ok)

    def test_submit_payment_bad_txn(self):
        ok, msg = v.submit_payment("Mobile Banking", "proof.jpg", "bad-txn")
        self.assertFalse(ok)

    def test_module_code_missing(self):
        ok, msg = v.register_module([], "")
        self.assertFalse(ok)
        self.assertIn("mandatory", msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
