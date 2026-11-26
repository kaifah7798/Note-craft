import base64
from pathlib import Path
import streamlit as st
from ui_study import render_study_tab
from ui_pyq import render_pyq_tab
from ui_test import render_test_tab
from ui_dashboard import render_dashboard_tab

LOGO_PATH = Path("logo.png")  
st.set_page_config(
    page_title="NoteCraft AI",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "NC",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def get_logo_html(size: int = 56, margin_bottom: int = 10) -> str:
    if LOGO_PATH.exists():
        b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        ext = LOGO_PATH.suffix.lstrip(".").lower() or "png"
        return (
            f'<img src="data:image/{ext};base64,{b64}" '
            f'style="width:{size}px; height:{size}px; border-radius:10px; object-fit:contain; margin-bottom:{margin_bottom}px;" />'
        )
    return (
        f'<div style="width:{size}px; height:{size}px; background:#111827; color:#FFFFFF; '
        f'border-radius:10px; display:inline-flex; align-items:center; justify-content:center; '
        f'font-weight:700; font-size:14px; margin-bottom:{margin_bottom}px;">NC</div>'
    )


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stApp {
        background-color: #F9FAFB;
        color: #111827;
    }
    .mono {
        font-family: 'JetBrains Mono', monospace;
    }
    .nc-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 500;
        background: #F3F4F6;
        color: #374151;
        border: 1px solid #E5E7EB;
    }
    .nc-badge-green {
        background: #ECFDF5;
        color: #065F46;
        border-color: #A7F3D0;
    }
    .nc-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10B981;
        display: inline-block;
    }
    div.stButton > button[kind="primary"] {
        background-color: #111827;
        color: #FFFFFF;
        border: 1px solid #111827;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.15s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1F2937;
        border-color: #1F2937;
        transform: translateY(-1px);
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 14px;
        border-color: #E5E7EB;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

YEAR_OPTIONS = ["1st Year", "2nd Year", "3rd Year", "4th Year"]

CYCLE_SEM_MAP = {
    "1st Year": ["Physics Cycle", "Chemistry Cycle"],
    "2nd Year": ["3rd Semester", "4th Semester"],
    "3rd Year": ["5th Semester", "6th Semester"],
    "4th Year": ["7th Semester", "8th Semester"],
}

FIRST_YEAR_BRANCHES = [
    "CSE & Allied (CSE, ISE, AIML, AIDS, CSE-AIML, CSE-Cyber)",
    "Electrical & Electronics (ECE, EEE, EIE, ETE, Medical Electronics)",
    "Civil",
    "Mechanical (ME, IEM, CH)",
]

SENIOR_BRANCHES = [
    "CSE",
    "ISE",
    "AIML",
    "AIDS",
    "CSE-AIML",
    "CSE-Cyber",
    "ECE",
    "EEE",
    "EIE",
    "ETE",
    "Medical Electronics",
    "ME",
    "Civil",
    "Chemical",
    "Biotechnology",
    "IEM",
]


def render_onboarding():
    st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.markdown(
            f"""
            <div style="text-align:center; margin-bottom:24px;">
                {get_logo_html(56, margin_bottom=10)}
                <div class="mono" style="font-size:11px; color:#6B7280; letter-spacing:0.06em; margin-bottom:6px;">
                    MSRIT · Team NetRunners · WHACKiest 2026
                </div>
                <div style="font-size:30px; font-weight:700; color:#111827; letter-spacing:-0.02em;">
                    NoteCraft AI
                </div>
                <div style="font-size:14px; color:#6B7280; margin-top:4px;">
                    Connect classroom lectures, teacher emphasis &amp; RIT NoteBook PYQs in one workspace.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown(
                """
                <div style="font-size:17px; font-weight:600; color:#111827; margin-bottom:4px;">
                    Configure Your Academic Context
                </div>
                <div style="font-size:13px; color:#6B7280; margin-bottom:16px;">
                    Your Drive catalog, PYQ vault, and Weakness Dashboard automatically adapt to this.
                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)
            year = c1.selectbox("Year", YEAR_OPTIONS, key="onboard_year")

            cycle_options = CYCLE_SEM_MAP[year]
            cycle = c2.selectbox("Cycle / Semester", cycle_options, key="onboard_cycle")

            branch_options = FIRST_YEAR_BRANCHES if year == "1st Year" else SENIOR_BRANCHES
            branch = st.selectbox("Branch", branch_options, key="onboard_branch")

            st.write("")
            if st.button("Enter Workspace →", type="primary", use_container_width=True):
                st.session_state["profile"] = {
                    "year": year,
                    "cycle": cycle,
                    "branch": branch,
                }
                st.rerun()


def render_workspace(profile: dict):
    h1, h2 = st.columns([3.5, 1], vertical_alignment="center")
    with h1:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
                {get_logo_html(34, margin_bottom=0)}
                <div>
                    <span style="font-size:18px; font-weight:700; color:#111827;">NoteCraft AI</span>
                    <span class="nc-badge" style="margin-left:8px;">
                        {profile['year']} · {profile['cycle']} · {profile['branch']}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with h2:
        if st.button("Switch Context", use_container_width=True):
            st.session_state.pop("profile", None)
            st.rerun()

    tab_study, tab_pyq, tab_test, tab_dash = st.tabs(
        ["Study Pack", "PYQ Vault", "Test Me", "Analytics"]
    )

    with tab_study:
        render_study_tab(profile)
    with tab_pyq:
        render_pyq_tab(profile)
    with tab_test:
        render_test_tab(profile)
    with tab_dash:
        render_dashboard_tab(profile)


if "profile" not in st.session_state:
    render_onboarding()
else:
    render_workspace(st.session_state["profile"])

st.markdown(
    """
    <div style="text-align:center; margin-top:40px; padding:16px 0; border-top:1px solid #E5E7EB;">
        <div class="mono" style="font-size:11px; font-weight:600; color:#374151; letter-spacing:0.08em;">
            BUILT BY TEAM NETRUNNERS
        </div>
        <div style="font-size:12px; color:#6B7280; margin-top:6px; line-height:1.8;">
            <strong>Members &amp; Contacts:</strong><br>
            Ayush Aryan — ayushxtraa@gmail.com<br>
            Kaif Ahmed — kaifah7798@gmail.com<br>
            Manas Gulwani — manasgulwani14@gmail.com<br>
            Vaibhav Gupta — guptau976@gmail.com
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
