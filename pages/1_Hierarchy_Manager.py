import streamlit as st
import graphviz
import pandas as pd

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Hierarchy Manager", page_icon="🏢", layout="wide")

# ─── Session State Init ──────────────────────────────────────────────────────
if "custom_members" not in st.session_state:
    st.session_state.custom_members = []

# ─── Hardcoded 8-Level Hierarchy ─────────────────────────────────────────────
HARDCODED_HIERARCHY = [
    # Level 1 – CEO
    {"id": "1",  "name": "James Carter",    "title": "Chief Executive Officer (CEO)",        "level": 1, "parent_id": None, "department": "Executive"},
    # Level 2 – C-Suite
    {"id": "2",  "name": "Sophia Turner",   "title": "Chief Technology Officer (CTO)",       "level": 2, "parent_id": "1",  "department": "Technology"},
    {"id": "3",  "name": "Robert King",     "title": "Chief Financial Officer (CFO)",        "level": 2, "parent_id": "1",  "department": "Finance"},
    {"id": "4",  "name": "Linda Hayes",     "title": "Chief Operating Officer (COO)",        "level": 2, "parent_id": "1",  "department": "Operations"},
    # Level 3 – VPs
    {"id": "5",  "name": "Daniel Park",     "title": "VP of Engineering",                    "level": 3, "parent_id": "2",  "department": "Engineering"},
    {"id": "6",  "name": "Emily Nguyen",    "title": "VP of Finance",                        "level": 3, "parent_id": "3",  "department": "Finance"},
    {"id": "7",  "name": "Marcus Reed",     "title": "VP of Operations",                     "level": 3, "parent_id": "4",  "department": "Operations"},
    # Level 4 – Managers
    {"id": "8",  "name": "Priya Sharma",    "title": "Engineering Manager",                  "level": 4, "parent_id": "5",  "department": "Engineering"},
    {"id": "9",  "name": "Tom Bradley",     "title": "Finance Manager",                      "level": 4, "parent_id": "6",  "department": "Finance"},
    {"id": "10", "name": "Anna Collins",    "title": "Operations Manager",                   "level": 4, "parent_id": "7",  "department": "Operations"},
    # Level 5 – Team Leads
    {"id": "11", "name": "Kevin Zhao",      "title": "Team Lead – Backend",                  "level": 5, "parent_id": "8",  "department": "Engineering"},
    {"id": "12", "name": "Sara Lopez",      "title": "Team Lead – Frontend",                 "level": 5, "parent_id": "8",  "department": "Engineering"},
    {"id": "13", "name": "Mike Jensen",     "title": "Team Lead – QA",                       "level": 5, "parent_id": "8",  "department": "Engineering"},
    # Level 6 – Senior Devs
    {"id": "14", "name": "Raj Patel",       "title": "Senior Backend Developer",             "level": 6, "parent_id": "11", "department": "Engineering"},
    {"id": "15", "name": "Julia White",     "title": "Senior Frontend Developer",            "level": 6, "parent_id": "12", "department": "Engineering"},
    {"id": "16", "name": "Chris Moore",     "title": "Senior QA Engineer",                   "level": 6, "parent_id": "13", "department": "Engineering"},
    # Level 7 – Developers
    {"id": "17", "name": "Nadia Ali",       "title": "Backend Developer",                    "level": 7, "parent_id": "14", "department": "Engineering"},
    {"id": "18", "name": "Oliver Grant",    "title": "Frontend Developer",                   "level": 7, "parent_id": "15", "department": "Engineering"},
    # Level 8 – Juniors / Interns
    {"id": "19", "name": "Tina Brooks",     "title": "Junior Developer",                     "level": 8, "parent_id": "17", "department": "Engineering"},
    {"id": "20", "name": "Sam Hughes",      "title": "Intern – Software",                    "level": 8, "parent_id": "18", "department": "Engineering"},
]

# ─── Level colors ────────────────────────────────────────────────────────────
LEVEL_COLORS = {
    1: ("#c0392b", "white"),   # CEO – deep red
    2: ("#1a5276", "white"),   # C-Suite – navy
    3: ("#1f618d", "white"),   # VP – blue
    4: ("#117a65", "white"),   # Manager – green
    5: ("#d4ac0d", "black"),   # Lead – gold
    6: ("#6c3483", "white"),   # Senior – purple
    7: ("#935116", "white"),   # Mid – brown
    8: ("#616a6b", "white"),   # Junior/Intern – gray
}

LEVEL_LABELS = {
    1: "Level 1 – CEO",
    2: "Level 2 – C-Suite",
    3: "Level 3 – VP",
    4: "Level 4 – Manager",
    5: "Level 5 – Team Lead",
    6: "Level 6 – Senior",
    7: "Level 7 – Developer",
    8: "Level 8 – Junior / Intern",
}

# ─── Helper Functions ─────────────────────────────────────────────────────────
def get_all_members():
    return HARDCODED_HIERARCHY + st.session_state.custom_members


def build_graph(members):
    g = graphviz.Digraph("OrgChart")
    g.attr(
        rankdir="TB",
        splines="ortho",
        nodesep="0.6",
        ranksep="0.8",
        bgcolor="transparent",
        fontname="Helvetica",
    )
    g.attr("node", shape="box", style="filled,rounded", fontname="Helvetica", fontsize="11", margin="0.25,0.15")
    g.attr("edge", color="#95a5a6", arrowsize="0.8")

    # Group nodes by level for rank alignment
    level_map: dict[int, list] = {}
    for m in members:
        level_map.setdefault(m["level"], []).append(m)

    for level, nodes in sorted(level_map.items()):
        fill, font = LEVEL_COLORS.get(level, ("#ecf0f1", "black"))
        with g.subgraph() as s:
            s.attr(rank="same")
            for m in nodes:
                lvl_label = LEVEL_LABELS.get(m["level"], f"Level {m['level']}")
                label = f"{m['name']}\n{m['title']}\n{lvl_label}"
                s.node(m["id"], label=label, fillcolor=fill, fontcolor=font)

    for m in members:
        if m["parent_id"]:
            g.edge(m["parent_id"], m["id"])

    return g


def next_id(all_members):
    all_ids = [int(m["id"]) for m in all_members if str(m["id"]).isdigit()]
    return str(max(all_ids) + 1) if all_ids else "100"


# ─── UI: Header ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .page-title {
        font-size: 2rem; font-weight: 800; letter-spacing: -0.5px;
        background: linear-gradient(90deg, #1a5276, #c0392b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .level-badge {
        display: inline-block; padding: 3px 10px; border-radius: 12px;
        font-size: 0.78rem; font-weight: 600; margin: 2px;
    }
    </style>
    <div class='page-title'>🏢 Organization Hierarchy Manager</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ─── Option Selector ──────────────────────────────────────────────────────────
option = st.radio(
    "**Select an option:**",
    [
        "📊  Option 1 – View Organization Hierarchy",
        "➕  Option 2 – Add New Member",
        "👥  Option 3 – Members Added This Session",
    ],
    horizontal=True,
    label_visibility="visible",
)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# OPTION 1 – View Hierarchy
# ══════════════════════════════════════════════════════════════════════════════
if option.startswith("📊"):
    st.subheader("📊 Full Organization Chart")

    all_members = get_all_members()

    # Legend
    with st.expander("🎨 Level Color Legend", expanded=False):
        cols = st.columns(4)
        for i, (lvl, (fill, font)) in enumerate(LEVEL_COLORS.items()):
            with cols[i % 4]:
                st.markdown(
                    f"<span class='level-badge' style='background:{fill};color:{font}'>"
                    f"{LEVEL_LABELS[lvl]}</span>",
                    unsafe_allow_html=True,
                )

    # Session-added badge
    if st.session_state.custom_members:
        st.success(f"✅ Showing **{len(st.session_state.custom_members)}** session-added member(s) in the chart below.")

    st.graphviz_chart(build_graph(all_members), use_container_width=True)

    # Table view
    with st.expander("📋 View as Table", expanded=False):
        df = pd.DataFrame(all_members)[["level", "name", "title", "department"]]
        df.columns = ["Level", "Name", "Title", "Department"]
        df["Level Label"] = df["Level"].map(LEVEL_LABELS)
        df = df.sort_values("Level").reset_index(drop=True)
        st.dataframe(df[["Level", "Level Label", "Name", "Title", "Department"]], use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# OPTION 2 – Add New Member
# ══════════════════════════════════════════════════════════════════════════════
elif option.startswith("➕"):
    st.subheader("➕ Add a New Member")

    st.info(
        "**Rule:** Members can only be added up to **Level 5 (Team Lead)**. "
        "If your selected parent is at Level 5 or deeper, the addition will be blocked."
    )

    all_members = get_all_members()

    # Only parents at level 1–4 can have children (child will be level 2–5)
    eligible_parents = sorted(
        [m for m in all_members if m["level"] <= 4],
        key=lambda x: (x["level"], x["name"]),
    )

    if not eligible_parents:
        st.warning("No eligible parent nodes found.")
    else:
        parent_labels = [
            f"[L{m['level']}] {m['name']}  —  {m['title']}"
            for m in eligible_parents
        ]
        parent_map = dict(zip(parent_labels, eligible_parents))

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("👤 Full Name", placeholder="e.g. Alex Morgan")
            title = st.text_input("💼 Job Title", placeholder="e.g. Backend Developer")

        with col2:
            department = st.selectbox(
                "🏬 Department",
                ["Engineering", "Finance", "Operations", "HR", "Marketing", "Sales", "Design", "Legal"],
            )
            parent_label = st.selectbox("🔗 Reports To (Parent Node)", parent_labels)

        # Preview the resulting level
        selected_parent = parent_map[parent_label]
        resulting_level = selected_parent["level"] + 1
        allowed = resulting_level <= 5

        st.markdown("#### 📌 Preview")
        pcol1, pcol2, pcol3 = st.columns(3)
        pcol1.metric("Parent Level", f"Level {selected_parent['level']}")
        pcol2.metric("New Member Level", f"Level {resulting_level}")
        pcol3.metric(
            "Status",
            "✅ Allowed" if allowed else "❌ Blocked",
            delta=LEVEL_LABELS.get(resulting_level, "") if allowed else "Exceeds Level 5 limit",
            delta_color="normal" if allowed else "inverse",
        )

        st.markdown("")

        if st.button("➕ Add Member", type="primary", disabled=not allowed):
            if not name.strip() or not title.strip():
                st.error("⚠️ Please fill in **Full Name** and **Job Title**.")
            else:
                new_member = {
                    "id": next_id(all_members),
                    "name": name.strip(),
                    "title": title.strip(),
                    "level": resulting_level,
                    "parent_id": selected_parent["id"],
                    "department": department,
                }
                st.session_state.custom_members.append(new_member)
                st.success(
                    f"🎉 **{name}** added successfully as *{title}* "
                    f"at **{LEVEL_LABELS[resulting_level]}** under **{selected_parent['name']}**!"
                )
                st.balloons()

        if not allowed:
            st.error(
                f"❌ Cannot add a member at **Level {resulting_level}**. "
                f"**{selected_parent['name']}** is already at Level {selected_parent['level']}, "
                f"which would place the new member beyond the allowed limit of Level 5."
            )


# ══════════════════════════════════════════════════════════════════════════════
# OPTION 3 – View Session-Added Members
# ══════════════════════════════════════════════════════════════════════════════
elif option.startswith("👥"):
    st.subheader("👥 Members Added This Session")

    if not st.session_state.custom_members:
        st.info("No members have been added yet in this session. Use **Option 2** to add members.")
    else:
        st.success(f"**{len(st.session_state.custom_members)}** member(s) added this session.")

        df = pd.DataFrame(st.session_state.custom_members)[
            ["level", "name", "title", "department", "parent_id"]
        ]

        # Resolve parent name
        id_to_name = {m["id"]: m["name"] for m in get_all_members()}
        df["parent_name"] = df["parent_id"].map(id_to_name)
        df["level_label"] = df["level"].map(LEVEL_LABELS)
        df = df.rename(columns={
            "level": "Level", "name": "Name", "title": "Title",
            "department": "Department", "level_label": "Level Label", "parent_name": "Reports To"
        })
        st.dataframe(
            df[["Level", "Level Label", "Name", "Title", "Department", "Reports To"]],
            use_container_width=True,
        )

        # Mini chart of just the new additions in context
        if st.checkbox("🔍 Preview chart with session members highlighted"):
            st.graphviz_chart(build_graph(get_all_members()), use_container_width=True)

        st.markdown("---")
        if st.button("🗑️ Clear All Session Members", type="secondary"):
            st.session_state.custom_members = []
            st.rerun()
