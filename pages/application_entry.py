import streamlit as st
import random
import string
import uuid
from datetime import date, timedelta

# ─── Page Config ─────────────────────────────────────────────────────────────
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

# ─── Generate Random Application ─────────────────────────────────────────────
def random_date(start_year=1985, end_year=2000):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def random_join_date():
    start = date(2020, 1, 1)
    end   = date.today()
    return start + timedelta(days=random.randint(0, (end - start).days))

def gen_phone():
    return "+91 " + str(random.randint(7000000000, 9999999999))

def gen_email(first, last):
    domains = ["gmail.com","company.in","techcorp.com","work.io","enterprise.net"]
    return first.lower() + "." + last.lower() + str(random.randint(10,99)) + "@" + random.choice(domains)

def gen_app_id():
    return "APP-" + str(date.today().year) + "-" + "".join(random.choices(string.digits, k=5))

def generate_application():
    first      = random.choice(FIRST_NAMES)
    last       = random.choice(LAST_NAMES)
    dept       = random.choice(DEPARTMENTS)
    desig      = random.choice(DESIGNATIONS)
    dob        = random_date()
    doj        = random_join_date()
    num_courses= random.randint(2, 4)
    courses    = random.sample(COURSES, num_courses)
    num_skills = random.randint(3, 5)
    skills     = random.sample(SKILLS_POOL, num_skills)
    salary     = random.choice([35000,45000,55000,65000,75000,90000,110000,130000])
    exp_years  = random.randint(0, 12)
    work_mode  = random.choice(WORK_MODES)
    emp_type   = random.choice(EMP_TYPES)
    city       = random.choice(CITIES)
    country    = random.choice(COUNTRIES)
    phone      = gen_phone()
    email      = gen_email(first, last)
    app_id     = gen_app_id()

    return {
        "app_id":      app_id,
        "first_name":  first,
        "last_name":   last,
        "full_name":   first + " " + last,
        "email":       email,
        "phone":       phone,
        "dob":         str(dob.strftime("%d %B %Y")),
        "dob_raw":     str(dob),
        "department":  dept,
        "designation": desig,
        "doj":         str(doj.strftime("%d %B %Y")),
        "work_mode":   work_mode,
        "emp_type":    emp_type,
        "city":        city,
        "country":     country,
        "salary":      str(salary),
        "experience":  str(exp_years),
        "courses":     courses,
        "skills":      skills,
    }

# ─── Session State ────────────────────────────────────────────────────────────
# Generate new application ONLY on first page load, not on every rerun
if "current_app" not in st.session_state or st.session_state.get("load_new", False):
    st.session_state.current_app  = generate_application()
    st.session_state.load_new     = False
    st.session_state.submit_result = None   # clear previous result

if "approved_apps" not in st.session_state:
    st.session_state.approved_apps = []
if "submit_result" not in st.session_state:
    st.session_state.submit_result = None

app = st.session_state.current_app

# ─── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.page-title {
    font-size:2rem; font-weight:900;
    background:linear-gradient(90deg,#1a3a5c,#8e44ad);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.section-header {
    font-size:1rem; font-weight:800; color:#1a5276;
    border-left:4px solid #1a5276; padding-left:10px; margin:14px 0 8px 0;
}
.info-para {
    background:#fdfefe; border:1.5px solid #d5d8dc;
    border-radius:12px; padding:18px 22px; margin:8px 0;
    line-height:1.9; font-size:0.97rem; color:#1a252f;
}
.highlight { font-weight:800; color:#1a5276; }
.course-badge {
    display:inline-block; background:#eaf4fb; color:#1a5276;
    border:1.5px solid #aed6f1; border-radius:20px;
    padding:4px 14px; margin:3px; font-size:0.82rem; font-weight:700;
}
.skill-badge {
    display:inline-block; background:#f5eef8; color:#6c3483;
    border:1.5px solid #d7bde2; border-radius:20px;
    padding:4px 14px; margin:3px; font-size:0.82rem; font-weight:700;
}
.approved-banner {
    background:linear-gradient(135deg,#eafaf1,#d5f5e3);
    border:2px solid #27ae60; border-radius:16px; padding:20px 28px;
    text-align:center; font-size:1.1rem; font-weight:700; color:#1e8449;
    margin:12px 0;
}
.rejected-banner {
    background:linear-gradient(135deg,#fdedec,#fad7d3);
    border:2px solid #e74c3c; border-radius:16px; padding:20px 28px;
    text-align:center; font-size:1.1rem; font-weight:700; color:#c0392b;
    margin:12px 0;
}
.app-card {
    background:white; border-radius:14px; padding:18px;
    box-shadow:0 4px 16px rgba(0,0,0,0.07); margin-bottom:10px;
    border-left:5px solid #27ae60;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("<div class='page-title'>📋 Employee Application Validator</div>", unsafe_allow_html=True)
st.markdown("Read the employee details carefully, then fill in the form below to validate and approve the application.")
st.markdown("---")

main_col, side_col = st.columns([3, 2], gap="large")

# ══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN – APPLICATION DETAILS (READ ONLY)
# ══════════════════════════════════════════════════════════════════════════════
with main_col:
    st.markdown("### 📄 Application Details to Validate")
    st.caption("Application ID: **" + app["app_id"] + "**  |  Read the paragraphs below carefully before filling the form.")

    # Para 1 – Personal Details
    courses_str = ", ".join(["**" + c + "**" for c in app["courses"]])
    skills_str  = ", ".join(["**" + s + "**" for s in app["skills"]])

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

    # Para 2 – Employment
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

    # Para 3 – Courses
    st.markdown("#### 📚 Mandatory Courses to be Completed")
    badges = "".join("<span class='course-badge'>" + c + "</span>" for c in app["courses"])
    st.markdown(
        "<div class='info-para'>"
        "As part of the onboarding process, the employee is required to complete the following "
        "mandatory training courses: " + badges +
        ". These courses must be completed within the first 90 days of joining. "
        "Failure to complete these courses may result in a review of the employment status."
        "</div>",
        unsafe_allow_html=True,
    )

    # Para 4 – Skills
    st.markdown("#### 🛠️ Declared Skills")
    skill_badges = "".join("<span class='skill-badge'>" + s + "</span>" for s in app["skills"])
    st.markdown(
        "<div class='info-para'>"
        "The applicant has declared the following key skills: " + skill_badges + ". "
        "The hiring team has reviewed these skills and found them relevant to the applied role. "
        "Further skill assessments may be conducted during the probation period."
        "</div>",
        unsafe_allow_html=True,
    )

    # Load new application button
    st.markdown("")
    if st.button("🔄 Load New Application", type="secondary"):
        st.session_state.load_new = True
        st.session_state.submit_result = None
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN – VALIDATION FORM
# ══════════════════════════════════════════════════════════════════════════════
with side_col:
    st.markdown("### ✍️ Fill & Validate")
    st.caption("Type the exact details from the application paragraphs on the left.")

    # Show result banner if submitted
    if st.session_state.submit_result == "approved":
        st.markdown(
            "<div class='approved-banner'>✅ APPROVED!<br>"
            "<span style='font-size:0.9rem;font-weight:500'>Application stored successfully.</span></div>",
            unsafe_allow_html=True,
        )
    elif st.session_state.submit_result == "rejected":
        st.markdown(
            "<div class='rejected-banner'>❌ REJECTED!<br>"
            "<span style='font-size:0.9rem;font-weight:500'>One or more fields don't match. Please try again.</span></div>",
            unsafe_allow_html=True,
        )

    with st.form("validate_form"):
        st.markdown("<div class='section-header'>👤 Personal Details</div>", unsafe_allow_html=True)
        v_fullname = st.text_input("Full Name *", placeholder="First and Last name")
        v_email    = st.text_input("Email Address *", placeholder="applicant@email.com")
        v_phone    = st.text_input("Phone Number *", placeholder="+91 XXXXXXXXXX")
        v_city     = st.text_input("City *", placeholder="City name")

        st.markdown("<div class='section-header'>💼 Employment Details</div>", unsafe_allow_html=True)
        v_desig    = st.text_input("Designation *", placeholder="Role / Title")
        v_dept     = st.text_input("Department *", placeholder="Department name")
        v_emptype  = st.selectbox("Employment Type *", ["","Full-Time","Part-Time","Contract","Intern"])
        v_workmode = st.selectbox("Work Mode *", ["","On-site","Remote","Hybrid"])
        v_salary   = st.text_input("Expected Salary (₹) *", placeholder="Numbers only")
        v_exp      = st.text_input("Years of Experience *", placeholder="e.g. 5")

        st.markdown("<div class='section-header'>📚 Courses</div>", unsafe_allow_html=True)
        st.caption("Select all mandatory courses mentioned in the application:")
        v_courses = []
        for course in COURSES:
            if st.checkbox(course, key="chk_" + course):
                v_courses.append(course)

        submit_btn = st.form_submit_button("✅ Submit & Validate", type="primary", use_container_width=True)

    # ── Validation Logic ──────────────────────────────────────────────────────
    if submit_btn:
        errors = []

        def norm(s): return s.strip().lower()

        if norm(v_fullname) != norm(app["full_name"]):
            errors.append("❌ **Full Name** doesn't match.")
        if norm(v_email) != norm(app["email"]):
            errors.append("❌ **Email** doesn't match.")
        if norm(v_phone.replace(" ","")) != norm(app["phone"].replace(" ","")):
            errors.append("❌ **Phone** doesn't match.")
        if norm(v_city) != norm(app["city"]):
            errors.append("❌ **City** doesn't match.")
        if norm(v_desig) != norm(app["designation"]):
            errors.append("❌ **Designation** doesn't match.")
        if norm(v_dept) != norm(app["department"]):
            errors.append("❌ **Department** doesn't match.")
        if v_emptype != app["emp_type"]:
            errors.append("❌ **Employment Type** doesn't match.")
        if v_workmode != app["work_mode"]:
            errors.append("❌ **Work Mode** doesn't match.")
        if norm(v_salary) != norm(app["salary"]):
            errors.append("❌ **Salary** doesn't match.")
        if norm(v_exp) != norm(app["experience"]):
            errors.append("❌ **Experience** doesn't match.")

        selected_set = set(v_courses)
        required_set = set(app["courses"])
        if selected_set != required_set:
            missing = required_set - selected_set
            extra   = selected_set - required_set
            if missing:
                errors.append("❌ **Courses** — missed: " + ", ".join(missing))
            if extra:
                errors.append("❌ **Courses** — extra selected: " + ", ".join(extra))

        if errors:
            st.session_state.submit_result = "rejected"
            for e in errors:
                st.markdown(e)
        else:
            st.session_state.submit_result = "approved"
            # Store approved record
            st.session_state.approved_apps.append({**app})
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM – APPROVED APPLICATIONS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("### ✅ Approved Applications This Session (" + str(len(st.session_state.approved_apps)) + ")")

if not st.session_state.approved_apps:
    st.caption("No approved applications yet. Validate an application above to see it here.")
else:
    for i, a in enumerate(reversed(st.session_state.approved_apps)):
        idx = len(st.session_state.approved_apps) - i
        with st.expander("✅ #" + str(idx) + "  |  " + a["app_id"] + "  —  " + a["full_name"] + "  |  " + a["department"], expanded=(i==0)):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**📧 Email:** " + a["email"])
                st.markdown("**📞 Phone:** " + a["phone"])
                st.markdown("**🏙️ City:** " + a["city"] + ", " + a["country"])
            with c2:
                st.markdown("**💼 Role:** " + a["designation"])
                st.markdown("**🏢 Dept:** " + a["department"])
                st.markdown("**📋 Type:** " + a["emp_type"] + " | " + a["work_mode"])
            with c3:
                st.markdown("**💰 Salary:** ₹" + a["salary"])
                st.markdown("**📅 Joining:** " + a["doj"])
                st.markdown("**⏳ Exp:** " + a["experience"] + " years")
            course_badges = "".join("<span class='course-badge'>" + c + "</span>" for c in a["courses"])
            st.markdown("**📚 Courses:** " + course_badges, unsafe_allow_html=True)
