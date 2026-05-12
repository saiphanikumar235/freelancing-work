import streamlit as st
import random
import string
from datetime import date, timedelta

st.set_page_config(page_title="Application Validator", page_icon="📋", layout="wide")

# ─── Data Pools ──────────────────────────────────────────────────────────────
FIRST_NAMES  = ["Arjun","Priya","Rahul","Sneha","Vikram","Ananya","Rohan","Divya",
                "Kiran","Meera","Sanjay","Pooja","Aditya","Lakshmi","Nikhil","Kavya",
                "Ravi","Deepa","Suresh","Nisha","James","Emily","Michael","Sarah",
                "David","Emma","Chris","Olivia","Daniel","Sophia"]
LAST_NAMES   = ["Kumar","Sharma","Patel","Singh","Reddy","Nair","Iyer","Mehta",
                "Joshi","Gupta","Shah","Verma","Mishra","Rao","Pillai","Smith",
                "Johnson","Williams","Brown","Jones","Davis","Miller","Wilson","Moore"]
DEPARTMENTS  = ["Engineering","Finance","Operations","Human Resources",
                "Marketing","Sales","Design","Legal","Product Management","Data Science"]
DESIGNATIONS = ["Software Engineer","Senior Analyst","Team Lead","Project Manager",
                "Business Analyst","QA Engineer","DevOps Engineer","UI/UX Designer",
                "Data Scientist","HR Specialist","Financial Analyst","Legal Advisor"]
WORK_MODES   = ["On-site","Remote","Hybrid"]
EMP_TYPES    = ["Full-Time","Part-Time","Contract","Intern"]
CITIES       = ["Bengaluru","Mumbai","Hyderabad","Chennai","Pune","Delhi","Kolkata",
                "Ahmedabad","Vijayawada","Jaipur","Surat","Lucknow"]
COUNTRIES    = ["India","United States","United Kingdom","Canada","Australia","Germany"]
COURSES = [
    "Python for Data Science","Machine Learning Fundamentals","AWS Cloud Practitioner",
    "Agile Project Management","Leadership & Communication","Cybersecurity Essentials",
    "Advanced Excel & Power BI","Docker & Kubernetes","React & Frontend Development",
    "SQL & Database Design","REST API Development","Figma UI/UX Design",
    "Financial Modelling","HR Analytics","Digital Marketing Strategy",
    "Java Spring Boot","Data Structures & Algorithms","Prompt Engineering with AI",
]
SKILLS_POOL = ["Python","SQL","Java","React","Excel","Tableau","Figma","AWS",
               "Docker","Kubernetes","Communication","Leadership","Data Analysis",
               "Machine Learning","Project Management","Agile","REST APIs","Git"]

# ─── Generators ──────────────────────────────────────────────────────────────
def random_date(sy=1985, ey=2000):
    s = date(sy, 1, 1); e = date(ey, 12, 31)
    return s + timedelta(days=random.randint(0, (e-s).days))

def random_join_date():
    s = date(2020,1,1); e = date.today()
    return s + timedelta(days=random.randint(0, (e-s).days))

def gen_phone():
    return "+91 " + str(random.randint(7000000000, 9999999999))

def gen_email(first, last):
    domains = ["gmail.com","company.in","techcorp.com","work.io","enterprise.net"]
    return first.lower() + "." + last.lower() + str(random.randint(10,99)) + "@" + random.choice(domains)

def gen_app_id():
    return "APP-" + str(date.today().year) + "-" + "".join(random.choices(string.digits, k=5))

def generate_application():
    first = random.choice(FIRST_NAMES)
    last  = random.choice(LAST_NAMES)
    dob   = random_date()
    doj   = random_join_date()
    return {
        "app_id":      gen_app_id(),
        "first_name":  first,
        "last_name":   last,
        "full_name":   first + " " + last,
        "email":       gen_email(first, last),
        "phone":       gen_phone(),
        "dob":         dob.strftime("%d %B %Y"),
        "department":  random.choice(DEPARTMENTS),
        "designation": random.choice(DESIGNATIONS),
        "doj":         doj.strftime("%d %B %Y"),
        "work_mode":   random.choice(WORK_MODES),
        "emp_type":    random.choice(EMP_TYPES),
        "city":        random.choice(CITIES),
        "country":     random.choice(COUNTRIES),
        "salary":      str(random.choice([35000,45000,55000,65000,75000,90000,110000,130000])),
        "experience":  str(random.randint(0, 12)),
        "courses":     random.sample(COURSES, random.randint(2,4)),
        "skills":      random.sample(SKILLS_POOL, random.randint(3,5)),
    }

# ─── Session State ────────────────────────────────────────────────────────────
if "current_app" not in st.session_state or st.session_state.get("load_new", False):
    st.session_state.current_app   = generate_application()
    st.session_state.load_new      = False
    st.session_state.submit_result = None
    st.session_state.val_errors    = []
    # Change form key to force all inputs to reset
    st.session_state.form_key      = str(id(st.session_state.current_app))

if "approved_apps"  not in st.session_state: st.session_state.approved_apps  = []
if "submit_result"  not in st.session_state: st.session_state.submit_result  = None
if "val_errors"     not in st.session_state: st.session_state.val_errors     = []
if "form_key"       not in st.session_state: st.session_state.form_key       = "form_default"

app = st.session_state.current_app

# ─── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.page-title {
    font-size:2rem;font-weight:900;
    background:linear-gradient(90deg,#1a3a5c,#8e44ad);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.section-block {
    background:#f8f9fa;border-radius:16px;
    border:1.5px solid #e0e0e0;padding:22px 26px;margin:18px 0;
}
.section-title {
    font-size:1.1rem;font-weight:900;color:#1a5276;
    border-left:5px solid #1a5276;padding-left:12px;margin-bottom:14px;
}
.info-para {
    background:white;border:1.5px solid #d5d8dc;border-radius:10px;
    padding:16px 20px;line-height:1.9;font-size:0.96rem;
    color:#1a252f;margin-bottom:14px;
}
.highlight {font-weight:800;color:#1a5276;}
.course-badge {
    display:inline-block;background:#eaf4fb;color:#1a5276;
    border:1.5px solid #aed6f1;border-radius:20px;
    padding:4px 14px;margin:3px;font-size:0.82rem;font-weight:700;
}
.skill-badge {
    display:inline-block;background:#f5eef8;color:#6c3483;
    border:1.5px solid #d7bde2;border-radius:20px;
    padding:4px 14px;margin:3px;font-size:0.82rem;font-weight:700;
}
.divider-label {
    font-size:0.82rem;font-weight:700;color:#7f8c8d;
    text-transform:uppercase;letter-spacing:1px;margin:16px 0 8px 0;
}
.approved-banner {
    background:linear-gradient(135deg,#eafaf1,#d5f5e3);
    border:2px solid #27ae60;border-radius:16px;padding:24px;
    text-align:center;font-size:1.2rem;font-weight:800;color:#1e8449;margin:16px 0;
}
.rejected-banner {
    background:linear-gradient(135deg,#fdedec,#fad7d3);
    border:2px solid #e74c3c;border-radius:16px;padding:24px;
    text-align:center;font-size:1.2rem;font-weight:800;color:#c0392b;margin:16px 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("<div class='page-title'>📋 Employee Application Validator</div>", unsafe_allow_html=True)
st.markdown("Read each section carefully, then fill in the boxes below each paragraph. Submit at the end to validate.")

hc1, hc2 = st.columns([4,1])
with hc1:
    st.caption("Application ID: **" + app["app_id"] + "**")
with hc2:
    if st.button("🔄 New Application", type="secondary", use_container_width=True):
        st.session_state.load_new = True
        st.rerun()

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# FORM — Section by section (paragraph → input boxes)
# ══════════════════════════════════════════════════════════════════════════════
with st.form("validate_form_" + st.session_state.form_key):

    # ── SECTION 1: Personal Information ──────────────────────────────────────
    st.markdown("<div class='section-block'>"
        "<div class='section-title'>👤 Section 1 — Personal Information</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='info-para'>"
        "This application has been submitted by <span class='highlight'>" + app["full_name"] + "</span>, "
        "who was born on <span class='highlight'>" + app["dob"] + "</span>. "
        "The applicant can be reached at email <span class='highlight'>" + app["email"] + "</span> "
        "and phone number <span class='highlight'>" + app["phone"] + "</span>. "
        "They are currently based in <span class='highlight'>" + app["city"] + ", " + app["country"] + "</span>."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='divider-label'>✍️ Fill in the personal details from the paragraph above</div>", unsafe_allow_html=True)
    pi1, pi2 = st.columns(2)
    with pi1:
        v_fullname = st.text_input("Full Name *",      placeholder="e.g. Arjun Kumar")
        v_phone    = st.text_input("Phone Number *",   placeholder="+91 XXXXXXXXXX")
    with pi2:
        v_email    = st.text_input("Email Address *",  placeholder="applicant@email.com")
        v_city     = st.text_input("City *",           placeholder="City name only")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── SECTION 2: Employment Details ────────────────────────────────────────
    st.markdown("<div class='section-block'>"
        "<div class='section-title'>💼 Section 2 — Employment Details</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='info-para'>"
        "The employee is applying for the role of <span class='highlight'>" + app["designation"] + "</span> "
        "in the <span class='highlight'>" + app["department"] + "</span> department. "
        "The proposed employment type is <span class='highlight'>" + app["emp_type"] + "</span> "
        "with a <span class='highlight'>" + app["work_mode"] + "</span> work arrangement. "
        "The expected date of joining is <span class='highlight'>" + app["doj"] + "</span>, "
        "and the applicant has <span class='highlight'>" + app["experience"] + " years</span> of prior experience. "
        "The expected monthly salary is <span class='highlight'>₹" + app["salary"] + "</span>."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='divider-label'>✍️ Fill in the employment details from the paragraph above</div>", unsafe_allow_html=True)
    ej1, ej2, ej3 = st.columns(3)
    with ej1:
        v_desig    = st.text_input("Designation *",         placeholder="Role / Title")
        v_emptype  = st.selectbox("Employment Type *",      ["", "Full-Time", "Part-Time", "Contract", "Intern"])
    with ej2:
        v_dept     = st.text_input("Department *",          placeholder="Department name")
        v_workmode = st.selectbox("Work Mode *",            ["", "On-site", "Remote", "Hybrid"])
    with ej3:
        v_salary   = st.text_input("Expected Salary (₹) *", placeholder="Numbers only, e.g. 65000")
        v_exp      = st.text_input("Years of Experience *",  placeholder="e.g. 5")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── SECTION 3: Mandatory Courses ─────────────────────────────────────────
    badges = "".join("<span class='course-badge'>" + c + "</span>" for c in app["courses"])
    st.markdown("<div class='section-block'>"
        "<div class='section-title'>📚 Section 3 — Mandatory Courses</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='info-para'>"
        "As part of the onboarding process, the employee is required to complete the following "
        "mandatory training courses: " + badges + ". "
        "These courses must be completed within the first 90 days of joining. "
        "Failure to complete these courses may result in a review of the employment status."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='divider-label'>✍️ Select ONLY the courses mentioned in the paragraph above</div>", unsafe_allow_html=True)

    v_courses = []
    chk_cols = st.columns(3)
    for idx, course in enumerate(COURSES):
        with chk_cols[idx % 3]:
            if st.checkbox(course, key="chk_" + course):
                v_courses.append(course)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── SECTION 4: Skills (read-only, no validation) ─────────────────────────
    skill_badges = "".join("<span class='skill-badge'>" + s + "</span>" for s in app["skills"])
    st.markdown("<div class='section-block'>"
        "<div class='section-title'>🛠️ Section 4 — Declared Skills (Read Only)</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='info-para'>"
        "The applicant has declared the following key skills: " + skill_badges + ". "
        "The hiring team has reviewed these skills and found them relevant to the applied role. "
        "Further skill assessments may be conducted during the probation period. "
        "No input is required for this section — it is provided for reference only."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Submit ────────────────────────────────────────────────────────────────
    st.markdown("")
    submit_btn = st.form_submit_button("✅ Submit & Validate Application", type="primary", use_container_width=True)

# ── Validation Logic (outside form) ──────────────────────────────────────────
if submit_btn:
    def norm(s): return str(s).strip().lower()

    errors = []
    if norm(v_fullname) != norm(app["full_name"]):
        errors.append("👤 **Full Name** doesn't match.")
    if norm(v_email) != norm(app["email"]):
        errors.append("📧 **Email** doesn't match.")
    if norm(v_phone.replace(" ","")) != norm(app["phone"].replace(" ","")):
        errors.append("📞 **Phone Number** doesn't match.")
    if norm(v_city) != norm(app["city"]):
        errors.append("🏙️ **City** doesn't match.")
    if norm(v_desig) != norm(app["designation"]):
        errors.append("💼 **Designation** doesn't match.")
    if norm(v_dept) != norm(app["department"]):
        errors.append("🏢 **Department** doesn't match.")
    if v_emptype != app["emp_type"]:
        errors.append("📋 **Employment Type** doesn't match.")
    if v_workmode != app["work_mode"]:
        errors.append("🖥️ **Work Mode** doesn't match.")
    if norm(v_salary) != norm(app["salary"]):
        errors.append("💰 **Salary** doesn't match.")
    if norm(v_exp) != norm(app["experience"]):
        errors.append("⏳ **Years of Experience** doesn't match.")

    missing = set(app["courses"]) - set(v_courses)
    extra   = set(v_courses) - set(app["courses"])
    if missing:
        errors.append("📚 **Courses** — you missed: " + ", ".join(missing))
    if extra:
        errors.append("📚 **Courses** — extra selected: " + ", ".join(extra))

    st.session_state.val_errors    = errors
    st.session_state.submit_result = "approved" if not errors else "rejected"
    if not errors:
        st.session_state.approved_apps.append({**app})
    st.rerun()

# ── Result Banner ─────────────────────────────────────────────────────────────
if st.session_state.submit_result == "approved":
    st.markdown(
        "<div class='approved-banner'>"
        "✅ APPLICATION APPROVED!<br>"
        "<span style='font-size:0.95rem;font-weight:500'>All details matched. Record stored in session.</span>"
        "</div>",
        unsafe_allow_html=True,
    )
elif st.session_state.submit_result == "rejected":
    st.markdown(
        "<div class='rejected-banner'>"
        "❌ APPLICATION REJECTED — Please Fix the Errors Below<br>"
        "</div>",
        unsafe_allow_html=True,
    )
    for err in st.session_state.val_errors:
        st.markdown("&nbsp;&nbsp;• " + err)
    st.info("💡 Scroll up, correct the highlighted fields, and submit again.")

# ══════════════════════════════════════════════════════════════════════════════
# APPROVED APPLICATIONS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("### ✅ Approved Applications This Session (" + str(len(st.session_state.approved_apps)) + ")")

if not st.session_state.approved_apps:
    st.caption("No approved applications yet.")
else:
    for i, a in enumerate(reversed(st.session_state.approved_apps)):
        idx = len(st.session_state.approved_apps) - i
        with st.expander("✅ #" + str(idx) + "  |  " + a["app_id"] + "  —  " + a["full_name"] + "  |  " + a["department"], expanded=(i==0)):
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                st.markdown("**📧 Email:** " + a["email"])
                st.markdown("**📞 Phone:** " + a["phone"])
                st.markdown("**🏙️ City:** " + a["city"] + ", " + a["country"])
            with ac2:
                st.markdown("**💼 Role:** " + a["designation"])
                st.markdown("**🏢 Dept:** " + a["department"])
                st.markdown("**📋 Type:** " + a["emp_type"] + " | " + a["work_mode"])
            with ac3:
                st.markdown("**💰 Salary:** ₹" + a["salary"])
                st.markdown("**📅 Joining:** " + a["doj"])
                st.markdown("**⏳ Exp:** " + a["experience"] + " years")
            cb = "".join("<span class='course-badge'>" + c + "</span>" for c in a["courses"])
            st.markdown("**📚 Courses:** " + cb, unsafe_allow_html=True)

# ── Download Approved Applications ───────────────────────────────────────────
if st.session_state.approved_apps:
    import json, io
    import pandas as pd

    df_export = pd.DataFrame([
        {k: (", ".join(v) if isinstance(v, list) else v)
         for k, v in a.items()}
        for a in st.session_state.approved_apps
    ])

    st.markdown("#### 📥 Download Approved Applications")
    dl1, dl2 = st.columns(2)
    with dl1:
        csv_bytes = df_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download as CSV",
            data=csv_bytes,
            file_name="approved_applications.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )
    with dl2:
        json_bytes = json.dumps(st.session_state.approved_apps, indent=2).encode("utf-8")
        st.download_button(
            "⬇️ Download as JSON",
            data=json_bytes,
            file_name="approved_applications.json",
            mime="application/json",
            use_container_width=True,
        )
