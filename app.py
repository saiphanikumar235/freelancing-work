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
.hero-sub { font-size:1.1rem; color:#5d6d7e; margin-top:8px; }
.page-card {
    border-radius:16px; padding:20px 20px 10px 20px; margin-bottom:4px;
    border-left:5px solid; box-shadow:0 4px 18px rgba(0,0,0,0.07);
    background:white;
}
.card-num   { font-size:0.72rem; font-weight:700; color:#aab7b8; text-transform:uppercase; letter-spacing:1px; }
.card-icon  { font-size:1.8rem; margin:4px 0; }
.card-title { font-size:1.05rem; font-weight:900; margin:4px 0; }
.card-desc  { font-size:0.86rem; color:#5d6d7e; line-height:1.6; }
.card-tags  { margin-top:8px; }
.badge {
    display:inline-block; padding:2px 9px; border-radius:20px;
    font-size:0.72rem; font-weight:700; margin:2px;
}
.progress-wrap {
    background:#eaecee; border-radius:10px; height:12px; overflow:hidden; margin:6px 0 2px 0;
}
.progress-fill {
    height:100%; border-radius:10px;
    background:linear-gradient(90deg,#1a5276,#27ae60);
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='hero-title'>🏠 Multi-Page Application</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-sub'>10 powerful tools — AI, Speech, Vision, Forms & more.<br>"
    "👈 Use the <b>sidebar</b> or click any card below to navigate.</div>",
    unsafe_allow_html=True,
)
st.markdown("")
st.markdown("---")

# ── Page Definitions ──────────────────────────────────────────────────────────
PAGES = [
    {
        "num": 1, "icon": "🏢", "title": "Hierarchy Manager",
        "file": "pages/1_Hierarchy_Manager.py",
        "desc": "View an 8-level org chart. Add members up to Level 5 only. Session-added members appear live in the chart.",
        "tags": [("✅ Built","#27ae60","#eafaf1"),("Graphviz Chart","#1a5276","#eaf4fb"),("Session Storage","#8e44ad","#f5eef8")],
        "color": "#1a5276", "tech": "graphviz · pandas",
    },
    {
        "num": 2, "icon": "🎙️", "title": "Speech to Text",
        "file": "pages/2_Speech_to_Text.py",
        "desc": "Record voice via mic, convert to text, test accuracy against reference phrases with word-by-word comparison. Copy to clipboard.",
        "tags": [("✅ Built","#27ae60","#eafaf1"),("Google Speech API","#1a5276","#eaf4fb"),("Free Tier","#117a65","#eafaf1")],
        "color": "#117a65", "tech": "audio-recorder-streamlit · SpeechRecognition",
    },
    {
        "num": 3, "icon": "🎭", "title": "Speech Emotion Analyzer",
        "file": "pages/3_Speech_Emotion_Analyzer.py",
        "desc": "Speak freely and detect 😡 Angry, 😊 Happy, 😢 Sad or 😐 Neutral using keyword AI. Score bars, emoji card, session history.",
        "tags": [("✅ Built","#27ae60","#eafaf1"),("No Paid API","#8e44ad","#f5eef8"),("Keyword AI","#e67e22","#fef9e7")],
        "color": "#8e44ad", "tech": "audio-recorder-streamlit · SpeechRecognition",
    },
    {
        "num": 4, "icon": "🖼️", "title": "Background Remover",
        "file": "pages/4_Background_Remover.py",
        "desc": "Capture or upload a photo. Background removed instantly using OpenCV GrabCut — 100% local, no model download, no paid API.",
        "tags": [("✅ Built","#27ae60","#eafaf1"),("100% Local","#1a5276","#eaf4fb"),("OpenCV GrabCut","#c0392b","#fdedec")],
        "color": "#e67e22", "tech": "opencv-python-headless · Pillow",
    },
    {
        "num": 5, "icon": "📝", "title": "Employee Registration",
        "file": "pages/5_Employee_Registration.py",
        "desc": "Full registration form with personal info, employment details, skills and live camera photo. Generates random App No. and approval card on submit.",
        "tags": [("✅ Built","#27ae60","#eafaf1"),("Camera Capture","#1a5276","#eaf4fb"),("Random App No.","#f39c12","#fef9e7")],
        "color": "#1a5276", "tech": "Pillow · pandas",
    },
    {
        "num": 6, "icon": "📋", "title": "Application Validator",
        "file": "pages/6_Application_Validator.py",
        "desc": "Random employee application shown as paragraphs. Read & fill matching boxes section by section. Validate, approve, and download as CSV or JSON.",
        "tags": [("✅ Built","#27ae60","#eafaf1"),("Random Generation","#8e44ad","#f5eef8"),("CSV / JSON Export","#117a65","#eafaf1")],
        "color": "#6c3483", "tech": "pandas · json",
    },
    {
        "num": 7,  "icon": "❓", "title": "Coming Soon", "file": None,
        "desc": "Describe what you want on Page 7 and it will be built next.",
        "tags": [("🔜 Pending","#7f8c8d","#f2f3f4")], "color": "#bdc3c7", "tech": "",
    },
    {
        "num": 8,  "icon": "❓", "title": "Coming Soon", "file": None,
        "desc": "Describe what you want on Page 8 and it will be built next.",
        "tags": [("🔜 Pending","#7f8c8d","#f2f3f4")], "color": "#bdc3c7", "tech": "",
    },
    {
        "num": 9,  "icon": "❓", "title": "Coming Soon", "file": None,
        "desc": "Describe what you want on Page 9 and it will be built next.",
        "tags": [("🔜 Pending","#7f8c8d","#f2f3f4")], "color": "#bdc3c7", "tech": "",
    },
    {
        "num": 10, "icon": "❓", "title": "Coming Soon", "file": None,
        "desc": "Describe what you want on Page 10 and it will be built next.",
        "tags": [("🔜 Pending","#7f8c8d","#f2f3f4")], "color": "#bdc3c7", "tech": "",
    },
]

# ── Cards Grid ────────────────────────────────────────────────────────────────
st.markdown("### 📋 All Pages — click any card to open")
cols = st.columns(2, gap="large")

for i, page in enumerate(PAGES):
    with cols[i % 2]:
        color = page["color"]

        tags_html = "".join(
            "<span class='badge' style='background:" + bg + ";color:" + fg + "'>" + label + "</span>"
            for label, fg, bg in page["tags"]
        )
        tech_html = (
            "<div style='margin-top:6px;font-size:0.76rem;color:#aab7b8'>🔧 " + page["tech"] + "</div>"
            if page.get("tech") else ""
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

        # Clickable navigation button directly under card
        if page["file"]:
            st.page_link(
                page["file"],
                label="🚀 Go to " + page["title"],
                use_container_width=True,
            )
        else:
            st.button(
                "🔜 Coming Soon",
                key="btn_p" + str(page["num"]),
                disabled=True,
                use_container_width=True,
            )

        st.markdown("")   # spacing between cards

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
        "<div style='text-align:right;font-size:2.2rem;font-weight:900;color:#1a5276'>"
        + str(pct) + "%</div>",
        unsafe_allow_html=True,
    )
st.caption(str(len(PAGES) - built) + " pages remaining — describe the next page to continue building!")
