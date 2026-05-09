import streamlit as st

st.set_page_config(
    page_title="Home – Multi-Page App",
    page_icon="🏠",
    layout="wide",
)

st.markdown(
    """
    <style>
    .hero-title {
        font-size: 3rem; font-weight: 900; letter-spacing: -1px;
        background: linear-gradient(90deg, #1a5276, #8e44ad, #c0392b, #f39c12);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .hero-sub {
        font-size: 1.15rem; color: #5d6d7e; margin-top: 8px; font-weight: 400;
    }
    .page-card {
        border-radius: 16px; padding: 22px 20px; margin-bottom: 14px;
        border-left: 5px solid; box-shadow: 0 4px 18px rgba(0,0,0,0.07);
        background: white;
    }
    .card-title { font-size: 1.1rem; font-weight: 800; margin-bottom: 4px; }
    .card-desc  { font-size: 0.9rem; color: #5d6d7e; }
    .badge {
        display: inline-block; padding: 2px 10px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 700; margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='hero-title'>🏠 Multi-Page Application</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-sub'>A collection of 10 powerful tools — AI, Speech, Vision & more.<br>"
    "Use the <b>sidebar</b> to navigate between pages.</div>",
    unsafe_allow_html=True,
)
st.markdown("")
st.info("👈 **Select any page from the sidebar** to get started.")
st.markdown("---")

st.markdown("### 📋 Available Pages")

PAGES = [
    {"num":1,  "icon":"🏢",  "title":"Hierarchy Manager",       "desc":"View & manage an 8-level org chart. Add members up to Level 5.",                    "tags":[("✅ Built","#27ae60","#eafaf1")],           "color":"#1a5276"},
    {"num":2,  "icon":"🎙️", "title":"Speech to Text",           "desc":"Record voice, transcribe, and test accuracy with word-by-word comparison.",          "tags":[("✅ Built","#27ae60","#eafaf1")],           "color":"#117a65"},
    {"num":3,  "icon":"🎭",  "title":"Speech Emotion Analyzer",  "desc":"Speak and detect 😡 Angry, 😊 Happy, 😢 Sad or 😐 Neutral via keyword AI.",         "tags":[("✅ Built","#27ae60","#eafaf1")],           "color":"#8e44ad"},
    {"num":4,  "icon":"🖼️", "title":"Background Remover",       "desc":"Camera capture + remove background locally using U2Net AI. No paid API.",            "tags":[("✅ Built","#27ae60","#eafaf1")],           "color":"#e67e22"},
    {"num":5,  "icon":"❓",  "title":"Coming Soon",              "desc":"Tell us what you would like on Page 5!",                                              "tags":[("🔜 Pending","#7f8c8d","#f2f3f4")],        "color":"#bdc3c7"},
    {"num":6,  "icon":"❓",  "title":"Coming Soon",              "desc":"Tell us what you would like on Page 6!",                                              "tags":[("🔜 Pending","#7f8c8d","#f2f3f4")],        "color":"#bdc3c7"},
    {"num":7,  "icon":"❓",  "title":"Coming Soon",              "desc":"Tell us what you would like on Page 7!",                                              "tags":[("🔜 Pending","#7f8c8d","#f2f3f4")],        "color":"#bdc3c7"},
    {"num":8,  "icon":"❓",  "title":"Coming Soon",              "desc":"Tell us what you would like on Page 8!",                                              "tags":[("🔜 Pending","#7f8c8d","#f2f3f4")],        "color":"#bdc3c7"},
    {"num":9,  "icon":"❓",  "title":"Coming Soon",              "desc":"Tell us what you would like on Page 9!",                                              "tags":[("🔜 Pending","#7f8c8d","#f2f3f4")],        "color":"#bdc3c7"},
    {"num":10, "icon":"❓",  "title":"Coming Soon",              "desc":"Tell us what you would like on Page 10!",                                             "tags":[("🔜 Pending","#7f8c8d","#f2f3f4")],        "color":"#bdc3c7"},
]

cols = st.columns(2, gap="large")
for i, page in enumerate(PAGES):
    with cols[i % 2]:
        # Build badge HTML
        tags_html = " ".join(
            "<span class='badge' style='background:" + bg + ";color:" + fg + "'>" + label + "</span>"
            for label, fg, bg in page["tags"]
        )
        color     = page["color"]
        icon      = page["icon"]
        num       = page["num"]
        title     = page["title"]
        desc      = page["desc"]

        card_html = (
            "<div class='page-card' style='border-left-color:" + color + "'>"
            "<div class='card-title' style='color:" + color + "'>"
            + icon + " Page " + str(num) + " — " + title +
            "</div>"
            "<div class='card-desc'>" + desc + "</div>"
            "<div>" + tags_html + "</div>"
            "</div>"
        )
        st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")
built = sum(1 for p in PAGES if any("Built" in t[0] for t in p["tags"]))
st.markdown("### 🚦 Progress: " + str(built) + " / " + str(len(PAGES)) + " pages built")
st.progress(built / len(PAGES))
st.caption(str(len(PAGES) - built) + " pages remaining — describe the next page to continue!")
