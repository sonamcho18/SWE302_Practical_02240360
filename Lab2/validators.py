"""
validators.py
--------------
Core business-logic / validation layer for the CST College
Student Management System (CSMS).

Every function here implements one or more requirements from the
Lab 1 Software Requirements Specification (SRS):

    R1  Student ID is mandatory.
    R2  Student ID must be exactly 8 digits, numeric only.
    R3  Password is mandatory.
    R4  Password must be 8-12 chars, with >=1 upper, >=1 lower, >=1 digit.
    R5  Payment must be made using Mobile Banking only.
    R6  Payment screenshot mandatory, JPG/JPEG/PNG only.
    R7  Transaction number mandatory, format NNN-NNNNNNNNN (13 chars).
    R8  Verified payment upload -> electronic receipt generated.
    R9  Unverifiable / incomplete payment -> registration stays incomplete.

This module is deliberately framework-free (no Flask import) so it
can be unit tested in complete isolation, which is what Lab 2 asks
for ("develop automated unit tests ... achieving specified code
coverage").
"""

import re

ALLOWED_SCREENSHOT_EXTENSIONS = {"jpg", "jpeg", "png"}
TXN_NUMBER_PATTERN = re.compile(r"^\d{3}-\d{9}$")
STUDENT_ID_PATTERN = re.compile(r"^\d{8}$")


# ---------------------------------------------------------------------------
# 1. Student Login  (R1, R2, R3, R4)
# ---------------------------------------------------------------------------
def validate_student_id(student_id):
    """R1 + R2: mandatory, exactly 8 digits, numeric only."""
    if student_id is None or str(student_id).strip() == "":
        return False, "Student ID is mandatory."
    student_id = str(student_id).strip()
    if not student_id.isdigit():
        return False, "Student ID must contain digits only."
    if len(student_id) != 8:
        return False, "Student ID must contain exactly 8 digits."
    return True, "Valid Student ID."


def validate_password(password):
    """R3 + R4: mandatory, 8-12 chars, upper+lower+digit required."""
    if password is None or password == "":
        return False, "Password is mandatory."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if len(password) > 12:
        return False, "Password must be at most 12 characters."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    return True, "Valid Password."


def login(student_id, password, valid_credentials):
    """
    Full login flow combining R1-R4.
    valid_credentials: dict {student_id: password} representing the
    "database" of registered accounts, e.g. {"02230123": "Passw0rd"}.
    """
    id_ok, id_msg = validate_student_id(student_id)
    if not id_ok:
        return False, id_msg
    pw_ok, pw_msg = validate_password(password)
    if not pw_ok:
        return False, pw_msg
    if valid_credentials.get(str(student_id).strip()) != password:
        return False, "Incorrect Student ID or Password."
    return True, "Login successful."


# ---------------------------------------------------------------------------
# 3. Tuition Payment  (R5, R6, R7, R8, R9)
# ---------------------------------------------------------------------------
def validate_payment_method(method):
    """R5: Payment shall be made using Mobile Banking only."""
    if method is None or str(method).strip() == "":
        return False, "Payment method is mandatory."
    if str(method).strip().lower() != "mobile banking":
        return False, "Payment shall be made using Mobile Banking only."
    return True, "Valid payment method."


def validate_payment_screenshot(filename):
    """R6: screenshot mandatory, must be JPG/JPEG/PNG."""
    if filename is None or str(filename).strip() == "":
        return False, "Payment screenshot is mandatory."
    filename = str(filename).strip()
    if "." not in filename:
        return False, "Payment screenshot must have a valid file extension."
    ext = filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_SCREENSHOT_EXTENSIONS:
        return False, "Only JPG, JPEG, or PNG files are allowed."
    return True, "Valid payment screenshot."


def validate_transaction_number(txn_number):
    """R7: mandatory, format 3 digits - 9 digits (13 chars total)."""
    if txn_number is None or str(txn_number).strip() == "":
        return False, "Transaction number is mandatory."
    txn_number = str(txn_number).strip()
    if len(txn_number) != 13:
        return False, "Transaction number must be exactly 13 characters (NNN-NNNNNNNNN)."
    if not TXN_NUMBER_PATTERN.match(txn_number):
        return False, "Transaction number must follow the format NNN-NNNNNNNNN."
    return True, "Valid transaction number."


def submit_payment(method, filename, txn_number):
    """
    Aggregates R5, R6, R7 into a single 'upload payment details' step.
    Returns (ok: bool, message: str).
    """
    ok, msg = validate_payment_method(method)
    if not ok:
        return False, msg
    ok, msg = validate_payment_screenshot(filename)
    if not ok:
        return False, msg
    ok, msg = validate_transaction_number(txn_number)
    if not ok:
        return False, msg
    return True, "Payment details submitted for verification."


def verify_payment(upload_complete, verified_by_college):
    """
    R8 + R9.
    upload_complete: bool -> screenshot + txn number both valid & present
    verified_by_college: bool -> staff/back-office confirms the transfer

    Returns a dict: {"status": ..., "receipt_generated": bool, "message": ...}
    """
    if not upload_complete:
        return {
            "status": "incomplete",
            "receipt_generated": False,
            "message": "Registration remains incomplete: payment upload is incomplete.",
        }
    if not verified_by_college:
        return {
            "status": "incomplete",
            "receipt_generated": False,
            "message": "Registration remains incomplete: payment could not be verified.",
        }
    return {
        "status": "verified",
        "receipt_generated": True,
        "message": "Payment verified. Electronic receipt generated.",
    }


# ---------------------------------------------------------------------------
# 2. Student Registration  (decision table: payment / drug test / period)
# ---------------------------------------------------------------------------
def check_registration_eligibility(payment_verified, drug_test_verified, period_open):
    """
    Decision table logic (Activity 3).
    Priority when more than one condition fails:
        Payment -> Drug Testing Report -> Registration Period
    Registration allowed only when all three are True.
    """
    if payment_verified and drug_test_verified and period_open:
        return True, "Registration Allowed"
    if not payment_verified:
        return False, "Tuition payment not verified."
    if not drug_test_verified:
        return False, "Drug testing report not verified."
    return False, "Registration period is closed."


def register_module(already_registered_modules, module_code):
    """A student cannot register the same module more than once."""
    if module_code is None or str(module_code).strip() == "":
        return False, "Module code is mandatory."
    module_code = str(module_code).strip().upper()
    if module_code in {m.upper() for m in already_registered_modules}:
        return False, "Duplicate registration: module already registered."
    already_registered_modules.append(module_code)
    return True, f"Module {module_code} registered successfully."


# ---------------------------------------------------------------------------
# 4. Result Viewing
# ---------------------------------------------------------------------------
def can_view_results(is_registered):
    """Only registered students may view their semester results."""
    if not is_registered:
        return False, "Only registered students may view their semester results."
    return True, "Access granted to result page."


def get_results(is_registered, results):
    """
    results: list of dicts [{"module_code":..., "module_title":..., "grade":...}, ...]
    Returns (ok, data_or_message)
    """
    ok, msg = can_view_results(is_registered)
    if not ok:
        return False, msg
    return True, results
