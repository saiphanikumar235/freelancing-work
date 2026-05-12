import streamlit as st

st.set_page_config(
    page_title="Multi-Page App",
    page_icon="🏠",
    layout="wide",
)

st.markdown("""
<style>
.hero-title {
    font-size:3rem; font-weight:900; letter-spacing:-1px;
    background:linear-gradient(90deg,#1a5276,#8e44ad,#c0392b,#f39c12);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    line-height:1.2;
}
.hero-sub {
    font-size:1.1rem; color:#5d6d7e; margin-top:8px;
}
.page-card {
    border-radius:16px; padding:22px 20px; margin-bottom:14px;
    border-left:5px solid; box-shadow:0 4px 18px rgba(0,0,0,0.07);
    background:white;
}
.card-icon   { font-size:2rem; margin-bottom:6px; }
.card-num    { font-size:0.75rem; font-weight:700; color:#aab7b8; text-transform:uppercase; letter-spacing:1px; }
.card-title  { font-size:1.05rem; font-weight:900; margin:4px 0; }
.card-desc   { font-size:0.88rem; color:#5d6d7e; line-height:1.6; }
.card-tags   { margin-top:10px; }
.badge {
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:0.73rem; font-weight:700; margin:2px;
}
.progress-wrap {
    background:#eaecee; border-radius:10px; height:12px;
    overflow:hidden; margin:6px 0 2px 0;
}
.progress-fill {
    height:100%; border-radius:10px;
    background:linear-gradient(90deg,#1a5276,#27ae60);
    transition:width 0.5s ease;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='hero-title'>🏠 Multi-Page Application</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-sub'>A collection of 10 powerful tools built with Streamlit — "
    "AI, Speech, Vision, Forms & more.<br>👈 Use the <b>sidebar</b> to navigate between pages.</div>",
    unsafe_allow_html=True,
)
st.markdown("")
st.info("👈 **Select any page from the sidebar** to get started.")
st.markdown("---")

# ── Page Definitions ──────────────────────────────────────────────────────────
PAGES = [
    {
        "num": 1, "icon": "🏢", "title": "Hierarchy Manager",
        "desc": (
            "View an 8-level organisation chart with hardcoded employee data. "
            "Add new members up to Level 5 only — deeper levels are blocked. "
            "Session-added members appear live in the chart."
        ),
        "tags": [
            ("✅ Built",           "#27ae60", "#eafaf1"),
            ("Graphviz Chart",     "#1a5276", "#eaf4fb"),
            ("Session Storage",    "#8e44ad", "#f5eef8"),
        ],
        "color": "#1a5276",
        "tech":  "graphviz · pandas",
    },
    {
        "num": 2, "icon": "🎙️", "title": "Speech to Text",
        "desc": (
            "Record your voice using the device mic and convert speech to text. "
            "Test accuracy against 15 reference phrases across Easy / Medium / Hard levels "
            "with colour-coded word-by-word comparison. Copy transcript to clipboard."
        ),
        "tags": [
            ("✅ Built",           "#27ae60", "#eafaf1"),
            ("Google Speech API",  "#1a5276", "#eaf4fb"),
            ("Free Tier",          "#117a65", "#eafaf1"),
        ],
        "color": "#117a65",
        "tech":  "audio-recorder-streamlit · SpeechRecognition",
    },
    {
        "num": 3, "icon": "🎭", "title": "Speech Emotion Analyzer",
        "desc": (
            "Speak naturally and detect your emotion — 😡 Angry, 😊 Happy, 😢 Sad, or 😐 Neutral. "
            "Uses keyword matching with intensifiers and negation logic. "
            "No paid API — 100% rule-based. Shows emoji, score bars and matched keywords."
        ),
        "tags": [
            ("✅ Built",       "#27ae60", "#eafaf1"),
            ("No Paid API",   "#8e44ad", "#f5eef8"),
            ("Keyword AI",    "#e67e22", "#fef9e7"),
        ],
        "color": "#8e44ad",
        "tech":  "audio-recorder-streamlit · SpeechRecognition",
    },
    {
        "num": 4, "icon": "🖼️", "title": "Background Remover",
        "desc": (
            "Capture a photo using your device camera or upload an image. "
            "The background is removed instantly using OpenCV GrabCut — "
            "runs fully locally with no model download and no paid API. "
            "Download as PNG (transparent), JPG (white/black bg), or with a custom colour/image background."
        ),
        "tags": [
            ("✅ Built",          "#27ae60", "#eafaf1"),
            ("100% Local",        "#1a5276", "#eaf4fb"),
            ("OpenCV GrabCut",    "#c0392b", "#fdedec"),
            ("No Paid API",       "#8e44ad", "#f5eef8"),
        ],
        "color": "#e67e22",
        "tech":  "opencv-python-headless · Pillow",
    },
    {
        "num": 5, "icon": "📝", "title": "Employee Registration Form",
        "desc": (
            "Full employee onboarding registration form with personal info, address, "
            "employment details, skills, and a live camera photo capture. "
            "On submit, generates a random Application Number and shows an approval card "
            "confirming a mail has been sent. All records stored in session."
        ),
        "tags": [
            ("✅ Built",          "#27ae60", "#eafaf1"),
            ("Camera Capture",    "#1a5276", "#eaf4fb"),
            ("Session Storage",   "#117a65", "#eafaf1"),
            ("Random App No.",    "#f39c12", "#fef9e7"),
        ],
        "color": "#1a5276",
        "tech":  "Pillow · pandas",
    },
    {
        "num": 6, "icon": "📋", "title": "Application Validator",
        "desc": (
            "A randomly generated employee application is shown as paragraphs on the page. "
            "Read each section and fill in the matching form boxes below it. "
            "On submit, every field is validated against the generated data — "
            "approved applications are stored in session and can be downloaded as CSV or JSON."
        ),
        "tags": [
            ("✅ Built",          "#27ae60", "#eafaf1"),
            ("Random Generation", "#8e44ad", "#f5eef8"),
            ("Field Validation",  "#c0392b", "#fdedec"),
            ("CSV / JSON Export", "#117a65", "#eafaf1"),
        ],
        "color": "#6c3483",
        "tech":  "pandas · json",
    },
    {
        "num": 7,  "icon": "❓", "title": "Coming Soon",
        "desc":  "Describe what you want on Page 7 and it will be built next.",
        "tags":  [("🔜 Pending", "#7f8c8d", "#f2f3f4")],
        "color": "#bdc3c7", "tech": "",
    },
    {
        "num": 8,  "icon": "❓", "title": "Coming Soon",
        "desc":  "Describe what you want on Page 8 and it will be built next.",
        "tags":  [("🔜 Pending", "#7f8c8d", "#f2f3f4")],
        "color": "#bdc3c7", "tech": "",
    },
    {
        "num": 9,  "icon": "❓", "title": "Coming Soon",
        "desc":  "Describe what you want on Page 9 and it will be built next.",
        "tags":  [("🔜 Pending", "#7f8c8d", "#f2f3f4")],
        "color": "#bdc3c7", "tech": "",
    },
    {
        "num": 10, "icon": "❓", "title": "Coming Soon",
        "desc":  "Describe what you want on Page 10 and it will be built next.",
        "tags":  [("🔜 Pending", "#7f8c8d", "#f2f3f4")],
        "color": "#bdc3c7", "tech": "",
    },
]

# ── Page Cards Grid ───────────────────────────────────────────────────────────
st.markdown("### 📋 All Pages")
cols = st.columns(2, gap="large")

for i, page in enumerate(PAGES):
    with cols[i % 2]:
        color = page["color"]
        tags_html = "".join(
            "<span class='badge' style='background:" + bg + ";color:" + fg + "'>" + label + "</span>"
            for label, fg, bg in page["tags"]
        )
        tech_html = ""
        if page.get("tech"):
            tech_html = (
                "<div style='margin-top:8px;font-size:0.78rem;color:#aab7b8'>"
                "🔧 " + page["tech"] + "</div>"
            )

        st.markdown(
            "<div class='page-card' style='border-left-color:" + color + "'>"
            "<div class='card-num'>Page " + str(page["num"]) + "</div>"
            "<div class='card-icon'>" + page["icon"] + "</div>"
            "<div class='card-title' style='color:" + color + "'>" + page["title"] + "</div>"
            "<div class='card-desc'>" + page["desc"] + "</div>"
            "<div class='card-tags'>" + tags_html + "</div>"
            + tech_html +
            "</div>",
            unsafe_allow_html=True,
        )

# ── Progress ──────────────────────────────────────────────────────────────────
built = sum(1 for p in PAGES if any("Built" in t[0] for t in p["tags"]))
pct   = int((built / len(PAGES)) * 100)

st.markdown("---")
st.markdown("### 🚦 Build Progress")

prog_col, stat_col = st.columns([4, 1])
with prog_col:
    st.markdown(
        "<div class='progress-wrap'>"
        "<div class='progress-fill' style='width:" + str(pct) + "%'></div>"
        "</div>"
        "<div style='font-size:0.82rem;color:#7f8c8d'>" + str(built) + " of " + str(len(PAGES)) + " pages built</div>",
        unsafe_allow_html=True,
    )
with stat_col:
    st.markdown(
        "<div style='text-align:right;font-size:2rem;font-weight:900;color:#1a5276'>" + str(pct) + "%</div>",
        unsafe_allow_html=True,
    )

st.caption(str(len(PAGES) - built) + " pages remaining — describe the next page to continue building!")
