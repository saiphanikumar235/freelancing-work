import streamlit as st
import pandas as pd
import re
import random
import string
from datetime import date
from PIL import Image
import io
import base64

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Employee Registration", page_icon="🏢", layout="wide")

# ─── Session State ────────────────────────────────────────────────────────────
if "employees" not in st.session_state:
    st.session_state.employees = []
if "last_submitted" not in st.session_state:
    st.session_state.last_submitted = None

# ─── Helpers ─────────────────────────────────────────────────────────────────
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email) is not None

def is_valid_phone(phone):
    return re.match(r"^\+?[\d\s\-\(\)]{7,15}$", phone) is not None

def generate_app_number():
    prefix = "EMP"
    year   = str(date.today().year)
    rand   = "".join(random.choices(string.digits, k=6))
    return prefix + "-" + year + "-" + rand

def pil_to_b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

# ─── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.page-title {
    font-size:2rem; font-weight:900;
    background:linear-gradient(90deg,#1a3a5c,#1a5276,#117a65);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.section-header {
    font-size:1.05rem; font-weight:800; color:#1a5276;
    border-left:4px solid #1a5276; padding-left:10px;
    margin:18px 0 10px 0;
}
.approval-card {
    background:linear-gradient(135deg,#eafaf1,#d5f5e3);
    border:2px solid #27ae60; border-radius:20px;
    padding:32px 36px; text-align:center;
    box-shadow:0 8px 30px rgba(39,174,96,0.15);
    animation: popIn 0.5s ease;
}
@keyframes popIn {
    0%  { transform:scale(0.9); opacity:0; }
    100%{ transform:scale(1);   opacity:1; }
}
.app-number {
    font-size:1.6rem; font-weight:900; letter-spacing:3px;
    color:#1a5276; background:#eaf4fb; border:2px dashed #1a5276;
    border-radius:12px; padding:10px 24px; display:inline-block;
    margin:12px 0;
}
.detail-row {
    display:flex; justify-content:space-between;
    padding:8px 0; border-bottom:1px solid #d5e8d4;
    font-size:0.95rem;
}
.detail-label { color:#5d6d7e; font-weight:600; }
.detail-value { color:#1a252f; font-weight:700; }
.field-required { color:#e74c3c; font-size:0.75rem; margin-left:4px; }
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("<div class='page-title'>🏢 Employee Registration Form</div>", unsafe_allow_html=True)
st.markdown("Fill in the details below to register a new employee. All fields marked **\\*** are required.")
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_form, tab_records = st.tabs(["📝  Registration Form", "📋  Registered Employees"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – REGISTRATION FORM
# ══════════════════════════════════════════════════════════════════════════════
with tab_form:

    # ── Show Approval Card if just submitted ─────────────────────────────────
    if st.session_state.last_submitted:
        emp = st.session_state.last_submitted
        photo_html = ""
        if emp.get("photo_b64"):
            photo_html = (
                "<img src='data:image/png;base64," + emp["photo_b64"] + "' "
                "style='width:110px;height:110px;border-radius:50%;object-fit:cover;"
                "border:4px solid #27ae60;margin-bottom:12px'/>"
            )

        details_html = ""
        detail_fields = [
            ("Application No.",  emp["app_number"]),
            ("Full Name",        emp["full_name"]),
            ("Email",            emp["email"]),
            ("Phone",            emp["phone"]),
            ("Department",       emp["department"]),
            ("Designation",      emp["designation"]),
            ("Date of Joining",  emp["doj"]),
            ("Employee Type",    emp["emp_type"]),
        ]
        for label, value in detail_fields:
            details_html += (
                "<div class='detail-row'>"
                "<span class='detail-label'>" + label + "</span>"
                "<span class='detail-value'>" + str(value) + "</span>"
                "</div>"
            )

        st.markdown(
            "<div class='approval-card'>"
            + photo_html +
            "<div style='font-size:2.5rem'>✅</div>"
            "<div style='font-size:1.5rem;font-weight:900;color:#1e8449;margin:6px 0'>"
            "Registration Successful!</div>"
            "<div style='font-size:1rem;color:#5d6d7e;margin-bottom:12px'>"
            "📧 We have sent a mail for approval with the following details:</div>"
            "<div class='app-number'>" + emp["app_number"] + "</div>"
            "<div style='font-size:1.1rem;font-weight:800;color:#1a5276;margin:10px 0'>"
            "Welcome, " + emp["full_name"] + "! 🎉</div>"
            "<div style='text-align:left;max-width:480px;margin:16px auto 0'>"
            + details_html +
            "</div></div>",
            unsafe_allow_html=True,
        )

        st.markdown("")
        if st.button("➕ Register Another Employee", type="primary"):
            st.session_state.last_submitted = None
            st.rerun()

    else:
        # ── FORM ─────────────────────────────────────────────────────────────
        with st.form("emp_reg_form", clear_on_submit=False):

            # Personal Information
            st.markdown("<div class='section-header'>👤 Personal Information</div>", unsafe_allow_html=True)
            p1, p2, p3 = st.columns(3)
            with p1:
                first_name = st.text_input("First Name *")
                gender     = st.selectbox("Gender *", ["Male", "Female", "Other"])
            with p2:
                last_name  = st.text_input("Last Name *")
                dob        = st.date_input("Date of Birth *", value=date(1995, 1, 1),
                                           min_value=date(1950,1,1), max_value=date(2005,12,31))
            with p3:
                email      = st.text_input("Email Address *", placeholder="name@company.com")
                phone      = st.text_input("Phone Number *", placeholder="+91 9876543210")

            # Address
            st.markdown("<div class='section-header'>🏠 Address Details</div>", unsafe_allow_html=True)
            a1, a2, a3 = st.columns(3)
            with a1:
                address  = st.text_input("Street Address")
            with a2:
                city     = st.text_input("City *")
            with a3:
                country  = st.selectbox("Country *", [
                    "India","United States","United Kingdom","Canada","Australia",
                    "Germany","France","Singapore","UAE","Other"
                ])

            # Employment Details
            st.markdown("<div class='section-header'>💼 Employment Details</div>", unsafe_allow_html=True)
            e1, e2, e3 = st.columns(3)
            with e1:
                department = st.selectbox("Department *", [
                    "Engineering","Finance","Operations","Human Resources",
                    "Marketing","Sales","Design","Legal","Product","Support"
                ])
                emp_type   = st.selectbox("Employment Type *", [
                    "Full-Time","Part-Time","Contract","Intern","Freelancer"
                ])
            with e2:
                designation = st.text_input("Designation / Role *", placeholder="e.g. Software Engineer")
                salary      = st.text_input("Expected Salary (₹/month)", placeholder="e.g. 50000")
            with e3:
                doj         = st.date_input("Date of Joining *", value=date.today())
                work_mode   = st.selectbox("Work Mode *", ["On-site","Remote","Hybrid"])

            # Skills & Notes
            st.markdown("<div class='section-header'>🛠️ Skills & Additional Info</div>", unsafe_allow_html=True)
            sk1, sk2 = st.columns(2)
            with sk1:
                skills = st.text_area("Key Skills", placeholder="e.g. Python, SQL, Project Management", height=90)
            with sk2:
                notes  = st.text_area("Additional Notes", height=90)

            # Photo Capture
            st.markdown("<div class='section-header'>📷 Employee Photo</div>", unsafe_allow_html=True)
            st.caption("Take a live photo using your device camera below (optional but recommended).")
            photo = st.camera_input("Capture Photo", label_visibility="collapsed")

            st.markdown("")
            submitted = st.form_submit_button("📨 Submit Registration", type="primary", use_container_width=True)

        # ── Validation & Save ─────────────────────────────────────────────────
        if submitted:
            errors = []
            if not first_name.strip():   errors.append("First Name is required.")
            if not last_name.strip():    errors.append("Last Name is required.")
            if not email.strip():        errors.append("Email is required.")
            elif not is_valid_email(email): errors.append("Invalid email format.")
            if not phone.strip():        errors.append("Phone is required.")
            elif not is_valid_phone(phone): errors.append("Invalid phone format.")
            if not city.strip():         errors.append("City is required.")
            if not designation.strip():  errors.append("Designation is required.")

            if errors:
                for err in errors:
                    st.error("❌ " + err)
            else:
                # Process photo
                photo_b64 = ""
                if photo:
                    img = Image.open(photo).convert("RGB")
                    # Crop to square
                    w, h = img.size
                    side = min(w, h)
                    left = (w - side) // 2
                    top  = (h - side) // 2
                    img  = img.crop((left, top, left+side, top+side)).resize((200,200), Image.LANCZOS)
                    photo_b64 = pil_to_b64(img)

                record = {
                    "app_number":   generate_app_number(),
                    "full_name":    first_name.strip() + " " + last_name.strip(),
                    "first_name":   first_name.strip(),
                    "last_name":    last_name.strip(),
                    "email":        email.strip(),
                    "phone":        phone.strip(),
                    "gender":       gender,
                    "dob":          str(dob),
                    "address":      address.strip(),
                    "city":         city.strip(),
                    "country":      country,
                    "department":   department,
                    "designation":  designation.strip(),
                    "emp_type":     emp_type,
                    "doj":          str(doj),
                    "work_mode":    work_mode,
                    "salary":       salary.strip(),
                    "skills":       skills.strip(),
                    "notes":        notes.strip(),
                    "photo_b64":    photo_b64,
                }
                st.session_state.employees.append(record)
                st.session_state.last_submitted = record
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – VIEW REGISTERED EMPLOYEES
# ══════════════════════════════════════════════════════════════════════════════
with tab_records:
    st.markdown("#### 📋 Registered Employees This Session")

    if not st.session_state.employees:
        st.info("No employees registered yet. Use the **Registration Form** tab to add employees.")
    else:
        st.success(str(len(st.session_state.employees)) + " employee(s) registered this session.")

        for i, emp in enumerate(st.session_state.employees):
            with st.expander("🧑‍💼 " + emp["full_name"] + "  |  " + emp["app_number"] + "  |  " + emp["department"], expanded=False):
                rc1, rc2, rc3 = st.columns([1, 2, 2])

                with rc1:
                    if emp.get("photo_b64"):
                        st.markdown(
                            "<img src='data:image/png;base64," + emp["photo_b64"] + "' "
                            "style='width:100%;border-radius:12px;border:3px solid #1a5276'/>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            "<div style='background:#eaf4fb;border-radius:12px;padding:30px;"
                            "text-align:center;font-size:3rem;border:2px solid #aed6f1'>👤</div>",
                            unsafe_allow_html=True,
                        )

                with rc2:
                    st.markdown("**🔖 App Number:** " + emp["app_number"])
                    st.markdown("**📧 Email:** " + emp["email"])
                    st.markdown("**📞 Phone:** " + emp["phone"])
                    st.markdown("**⚧ Gender:** " + emp["gender"])
                    st.markdown("**🎂 DOB:** " + emp["dob"])
                    st.markdown("**🏙️ City:** " + emp["city"] + ", " + emp["country"])

                with rc3:
                    st.markdown("**💼 Designation:** " + emp["designation"])
                    st.markdown("**🏢 Department:** " + emp["department"])
                    st.markdown("**📅 Joining:** " + emp["doj"])
                    st.markdown("**🖥️ Work Mode:** " + emp["work_mode"])
                    st.markdown("**📋 Type:** " + emp["emp_type"])
                    if emp.get("salary"):
                        st.markdown("**💰 Salary:** ₹" + emp["salary"])
                    if emp.get("skills"):
                        st.markdown("**🛠️ Skills:** " + emp["skills"])

        st.markdown("---")
        # Download CSV (exclude photos)
        df_export = pd.DataFrame([
            {k: v for k, v in e.items() if k != "photo_b64"}
            for e in st.session_state.employees
        ])
        csv_data = df_export.to_csv(index=False).encode("utf-8")
        col_dl, col_clr = st.columns([1, 3])
        with col_dl:
            st.download_button("⬇️ Download as CSV", data=csv_data,
                               file_name="employees.csv", mime="text/csv",
                               type="primary", use_container_width=True)
        with col_clr:
            if st.button("🗑️ Clear All Records", type="secondary"):
                st.session_state.employees = []
                st.session_state.last_submitted = None
                st.rerun()
