"""
app.py -- CST College Student Management System (CSMS)
A small Flask web application implementing the Lab 1 SRS:
  1. Student Login
  2. Student Registration (payment / drug test / period)
  3. Tuition Payment upload
  4. Result Viewing

All validation / business rules live in validators.py so that they
can be unit tested independently of Flask (see tests/test_validators.py).
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import validators

app = Flask(__name__)
app.secret_key = "csms-lab2-secret-key"

# ---------------------------------------------------------------------------
# In-memory "database" (for demo purposes only)
# ---------------------------------------------------------------------------
STUDENTS_DB = {
    "02240360": "Passw0rd1",   # Sonam Choki demo account
    "02230123": "Abcdef12",
}

STUDENT_STATE = {
    "02240360": {
        "tuition_paid": False,
        "drug_test_verified": True,
        "registered_modules": [],
        "is_registered": False,
        "results": [
            {"module_code": "SWE302", "module_title": "Software Testing & QA", "grade": "A"},
            {"module_code": "SWE301", "module_title": "Software Engineering", "grade": "B+"},
        ],
    },
    "02230123": {
        "tuition_paid": True,
        "drug_test_verified": True,
        "registered_modules": ["SWE302"],
        "is_registered": True,
        "results": [
            {"module_code": "SWE302", "module_title": "Software Testing & QA", "grade": "A-"},
        ],
    },
}

REGISTRATION_PERIOD_OPEN = True


def current_student():
    sid = session.get("student_id")
    return sid, STUDENT_STATE.get(sid)


@app.route("/")
def index():
    if session.get("student_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# 1. Login
# ---------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        sid = request.form.get("student_id", "")
        pw = request.form.get("password", "")
        ok, msg = validators.login(sid, pw, STUDENTS_DB)
        if ok:
            session["student_id"] = sid.strip()
            flash(msg, "success")
            return redirect(url_for("dashboard"))
        error = msg
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    sid, state = current_student()
    if not sid:
        return redirect(url_for("login"))
    return render_template("dashboard.html", student_id=sid, state=state)


# ---------------------------------------------------------------------------
# 3. Tuition Payment
# ---------------------------------------------------------------------------
@app.route("/payment", methods=["GET", "POST"])
def payment():
    sid, state = current_student()
    if not sid:
        return redirect(url_for("login"))

    result = None
    if request.method == "POST":
        method = request.form.get("method", "")
        txn = request.form.get("txn_number", "")
        file = request.files.get("screenshot")
        filename = file.filename if file else ""

        ok, msg = validators.submit_payment(method, filename, txn)
        if ok:
            # Simulate the college back-office verifying the transfer.
            verification = validators.verify_payment(
                upload_complete=True, verified_by_college=True
            )
            if verification["receipt_generated"]:
                state["tuition_paid"] = True
            result = {"ok": True, "message": verification["message"]}
        else:
            result = {"ok": False, "message": msg}

    return render_template("payment.html", student_id=sid, state=state, result=result)


# ---------------------------------------------------------------------------
# 2. Registration
# ---------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    sid, state = current_student()
    if not sid:
        return redirect(url_for("login"))

    eligible, elig_msg = validators.check_registration_eligibility(
        state["tuition_paid"], state["drug_test_verified"], REGISTRATION_PERIOD_OPEN
    )
    result = None
    if request.method == "POST":
        module_code = request.form.get("module_code", "")
        if not eligible:
            result = {"ok": False, "message": elig_msg}
        else:
            ok, msg = validators.register_module(state["registered_modules"], module_code)
            if ok:
                state["is_registered"] = True
            result = {"ok": ok, "message": msg}

    return render_template(
        "register.html",
        student_id=sid,
        state=state,
        eligible=eligible,
        elig_msg=elig_msg,
        result=result,
    )


# ---------------------------------------------------------------------------
# 4. Result Viewing
# ---------------------------------------------------------------------------
@app.route("/results")
def results():
    sid, state = current_student()
    if not sid:
        return redirect(url_for("login"))
    ok, data = validators.get_results(state["is_registered"], state["results"])
    return render_template("results.html", student_id=sid, ok=ok, data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
