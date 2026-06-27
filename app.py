import streamlit as st
import pandas as pd
import plotly.express as px

from pdf_reader import extract_text_from_pdf, clean_text
from skills_extractor import extract_skills, get_skill_summary
from job_matcher import match_all_jobs, get_top_match
from interview_prep import generate_interview_questions, get_total_question_count
from resume_scorer import score_resume

# ─── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── DARK THEME PALETTE: "Raw Black / Violet Glow" ────────────
BG          = "#040406"   # Near-black page background
PANEL       = "#0b0b10"   # Card / panel background
PANEL_2     = "#101018"   # Slightly lighter panel
TEXT        = "#f5f5f8"   # Near-white text
TEXT_DIM    = "#92929e"   # Muted gray text
TEXT_FAINT  = "#5d5d68"   # Faint labels
ACCENT      = "#7c5cff"   # Violet accent
ACCENT_2    = "#9b7bff"   # Lighter violet
SUCCESS     = "#3ddc97"   # Green (kept readable on dark)
WARNING     = "#f6ad55"   # Amber
DANGER      = "#ff6b6b"   # Red
BORDER      = "rgba(255,255,255,.08)"
BORDER_BR   = "rgba(255,255,255,.16)"

# ─── FULL CSS ──────────────────────────────────────────────────
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');

/* ── Reset & Base ── */
html, body, .stApp {{
    background-color: {BG} !important;
    font-family: 'Inter', sans-serif !important;
    color: {TEXT} !important;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background-color: {PANEL} !important;
    border-right: 1px solid {BORDER} !important;
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
}}

/* ── Hide default streamlit header/footer ── */
#MainMenu, footer, header {{visibility: hidden;}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background-color: {PANEL};
    padding: 8px;
    border-radius: 12px;
    border: 1px solid {BORDER};
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 500;
    color: {TEXT_DIM} !important;
    background: transparent;
    transition: all 0.3s ease;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: {TEXT} !important;
    background: rgba(124,92,255,0.08) !important;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_2}) !important;
    color: white !important;
}}

/* ── Upload box ── */
[data-testid="stFileUploader"] {{
    background: {PANEL};
    border: 2px dashed {ACCENT} !important;
    border-radius: 14px;
    padding: 12px;
    transition: all 0.3s ease;
}}

[data-testid="stFileUploader"]:hover {{
    border-color: {ACCENT_2} !important;
    background: rgba(124,92,255,0.04);
}}

[data-testid="stFileUploader"] small, [data-testid="stFileUploader"] span {{
    color: {TEXT_DIM} !important;
}}

/* ── Expander ── */
.streamlit-expanderHeader {{
    background-color: {PANEL} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: {TEXT} !important;
    transition: all 0.2s ease;
}}

.streamlit-expanderHeader:hover {{
    background-color: rgba(124,92,255,0.06) !important;
    border-color: {ACCENT} !important;
}}

.streamlit-expanderContent {{
    background-color: {PANEL} !important;
    border: 1px solid {BORDER} !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_2}) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    min-height: 44px !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(124,92,255,0.35) !important;
}}

/* ── Sliders ── */
.stSlider {{
    padding: 10px 0;
}}

/* ── Custom Classes ── */

.card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 24px 28px;
    margin: 12px 0;
    transition: all 0.3s ease;
}}

.card:hover {{
    border-color: {ACCENT};
    box-shadow: 0 4px 20px rgba(124,92,255,0.12);
}}

.stat-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 24px 28px;
    text-align: center;
    transition: all 0.3s ease;
}}

.stat-card:hover {{
    border-color: {ACCENT};
    box-shadow: 0 8px 28px rgba(124,92,255,0.18);
}}

.stat-num {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: {ACCENT_2};
    line-height: 1;
    margin: 0;
}}

.stat-label {{
    font-size: 12px;
    color: {TEXT_DIM};
    margin-top: 8px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.section-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: {TEXT};
    margin: 16px 0 20px 0;
}}

.skill-tag {{
    display: inline-block;
    background-color: rgba(124,92,255,0.1);
    color: {ACCENT_2};
    border: 1px solid rgba(124,92,255,0.3);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    margin: 4px 3px;
    transition: all 0.2s ease;
}}

.skill-tag:hover {{
    background-color: {ACCENT};
    color: white;
    transform: translateY(-2px);
}}

.cat-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {TEXT_FAINT};
    margin: 20px 0 10px 0;
}}

.top-banner {{
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_2} 100%);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 24px;
    color: white;
    box-shadow: 0 16px 40px rgba(124,92,255,0.3);
}}

.top-banner * {{ color: white !important; }}

.top-banner-title {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    opacity: 0.85;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 0;
}}

.top-banner-role {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    margin: 12px 0 4px;
}}

.top-banner-score {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 56px;
    font-weight: 700;
    margin: 8px 0;
    line-height: 1;
}}

.top-banner-desc {{
    font-size: 14px;
    opacity: 0.9;
    margin: 12px 0 0;
}}

.job-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-left: 4px solid {ACCENT};
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 14px;
    transition: all 0.3s ease;
}}

.job-card:hover {{
    box-shadow: 0 8px 28px rgba(124,92,255,0.18);
    border-left-color: {ACCENT_2};
}}

.prog-bg {{
    background: rgba(124,92,255,0.1);
    border-radius: 10px;
    height: 10px;
    width: 100%;
    margin: 12px 0;
    overflow: hidden;
}}

.prog-fill {{
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, {ACCENT}, {ACCENT_2});
    transition: width 0.5s ease;
}}

.tip-card {{
    background: rgba(246,173,85,0.08);
    border: 1px solid rgba(246,173,85,0.3);
    border-left: 4px solid {WARNING};
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 13px;
    color: #fbd38d;
    line-height: 1.6;
}}

.missing-tag {{
    display: inline-block;
    background: rgba(255,107,107,0.1);
    color: {DANGER};
    border: 1px solid rgba(255,107,107,0.35);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin: 4px 2px;
    font-weight: 500;
}}

.have-tag {{
    display: inline-block;
    background: rgba(61,220,151,0.1);
    color: {SUCCESS};
    border: 1px solid rgba(61,220,151,0.35);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin: 4px 2px;
    font-weight: 500;
}}

.q-card {{
    background: rgba(124,92,255,0.05);
    border: 1px solid {BORDER};
    border-left: 4px solid {ACCENT};
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 14px;
    color: {TEXT};
    line-height: 1.7;
}}

/* ── Hero panel (the "device screen" landing look) ── */
.hero-wrap {{
    position: relative;
    margin-bottom: 28px;
}}

.hero-glow {{
    position: absolute;
    top: -120px; left: 50%;
    width: 900px; height: 420px;
    transform: translateX(-50%);
    background: radial-gradient(ellipse at center, rgba(124,92,255,.32) 0%, rgba(124,92,255,.08) 40%, transparent 70%);
    filter: blur(40px);
    pointer-events: none;
    z-index: 0;
}}

.hero-panel {{
    position: relative;
    z-index: 1;
    background: linear-gradient(165deg, {PANEL_2} 0%, {PANEL} 55%, #060608 100%);
    border: 1px solid {BORDER};
    border-radius: 24px;
    padding: 44px 48px;
    box-shadow: 0 50px 100px -40px rgba(0,0,0,.7);
}}

.hero-eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {TEXT_FAINT};
    border: 1px solid {BORDER};
    padding: 7px 14px;
    border-radius: 999px;
    margin-bottom: 22px;
}}

.hero-eyebrow span {{ color: {ACCENT_2}; }}

.hero-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 44px;
    line-height: 1.08;
    letter-spacing: -1px;
    margin-bottom: 16px;
    max-width: 720px;
}}

.hero-title .grad {{
    background: linear-gradient(135deg, {ACCENT_2}, #ff8bd8 90%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.hero-sub {{
    font-size: 15px;
    line-height: 1.65;
    color: {TEXT_DIM};
    max-width: 560px;
}}

.live-pill {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(124,92,255,0.12);
    border: 1px solid rgba(124,92,255,.3);
    padding: 6px 14px 6px 10px;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: .5px;
    color: {ACCENT_2};
    margin-bottom: 24px;
}}

.live-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: {ACCENT};
    animation: pulse 1.8s ease-out infinite;
}}

@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(124,92,255,.55); }}
    70% {{ box-shadow: 0 0 0 8px rgba(124,92,255,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(124,92,255,0); }}
}}

</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 16px 0 24px 0; text-align:center;">
        <div style="font-size:40px; margin-bottom:12px;">🎯</div>
        <h2 style="color:{ACCENT_2}; margin:8px 0 4px; font-size:20px; font-weight:700; font-family:'Space Grotesk',sans-serif;">AI Job Assistant</h2>
        <p style="color:{TEXT_FAINT}; font-size:12px; margin:0; font-weight:500;">Career Intelligence v1.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"<p style='color:{TEXT_DIM}; font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:0.8px;'>⚙️ Settings</p>", unsafe_allow_html=True)

    max_jobs = st.slider("Maximum job matches", 2, 6, 4, help="Show up to 6 job recommendations")
    q_per_skill = st.slider("Questions per skill", 2, 5, 3, help="Generate 2-5 interview questions")

    st.divider()

    st.markdown(f"""
    <div style="background:rgba(124,92,255,0.08); 
                border:1px solid {BORDER}; border-radius:10px; padding:14px 16px;">
        <p style="color:{ACCENT_2}; font-size:13px; font-weight:700; margin:0 0 8px; text-transform:uppercase; letter-spacing:0.5px;">💡 Tips</p>
        <ul style="color:{TEXT_DIM}; font-size:12px; margin:0; padding-left:18px; line-height:1.8;">
            <li>PDF must contain selectable text</li>
            <li>Scanned images won't work</li>
            <li>List skills clearly</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
    <div style="text-align:center;">
        <p style="color:{TEXT_FAINT}; font-size:11px; margin:0; font-weight:500;">Built with Python & Streamlit</p>
        <p style="color:{TEXT_FAINT}; font-size:11px; margin:6px 0 0; font-weight:500;">University of Punjab 🎓</p>
    </div>
    """, unsafe_allow_html=True)


# ─── DARK HERO (the "device screen" landing block) ────────────
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-glow"></div>
    <div class="hero-panel">
        <div class="live-pill">
            <span class="live-dot"></span> LIVE
        </div>
        <div class="hero-eyebrow">AI-POWERED <span>·</span> CAREER INTELLIGENCE</div>
        <h1 class="hero-title">Your Resume, <span class="grad">Read Like a Recruiter Would.</span></h1>
        <p class="hero-sub">
            Upload one PDF and get everything a hiring manager would notice — your real skills,
            how you stack up against live job roles, a hard score out of 100, and the exact
            interview questions you should be ready for.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── FILE UPLOAD ───────────────────────────────────────────────
st.markdown(f"""
<div class="card">
    <p class="section-title">📄 Upload Your Resume</p>
    <p style="color:{TEXT_DIM}; font-size:14px; margin:0;">
        Select a PDF file to analyze — instant insights on skills, job matches, and interview prep.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    label_visibility="collapsed",
    help="Upload a PDF resume for instant analysis"
)


# ─── MAIN ──────────────────────────────────────────────────────
if uploaded_file:

    with st.spinner("📖 Reading your resume..."):
        raw  = extract_text_from_pdf(uploaded_file)
        text = clean_text(raw)

    if not text:
        st.error("❌ No text found in PDF. Please use a PDF with selectable text (not scanned images).")
        st.stop()

    word_count = len(text.split())
    st.markdown(f"""
    <div style="background:rgba(61,220,151,0.08); border:1px solid rgba(61,220,151,0.3); border-radius:10px;
                padding:14px 18px; margin:12px 0; display:flex; align-items:center; gap:12px;">
        <span style="font-size:22px;">✅</span>
        <p style="margin:0; color:{SUCCESS}; font-weight:600; font-size:15px;">
            Resume loaded successfully — Found <strong>{word_count}</strong> words!
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("🧠 Analyzing skills..."):
        skills, categories = extract_skills(text)

    # ── TABS ───────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠  Skills Analysis",
        "🎯  Job Matches",
        "📊  Resume Score",
        "💬  Interview Prep"
    ])

    # ══════════════════════════════════════════════════════════
    # TAB 1 ─ SKILLS ANALYSIS
    # ══════════════════════════════════════════════════════════
    with tab1:
        st.markdown(f"<p class='section-title'>Skills Found in Your Resume</p>", unsafe_allow_html=True)

        if not skills:
            st.warning("⚠️ No skills detected. Please ensure your resume clearly lists your skills.")
        else:
            total_s = len(skills)
            total_c = len(categories)
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""<div class="stat-card">
                    <p class="stat-num">{total_s}</p>
                    <p class="stat-label">Total Skills</p>
                </div>""", unsafe_allow_html=True)

            with c2:
                st.markdown(f"""<div class="stat-card">
                    <p class="stat-num">{total_c}</p>
                    <p class="stat-label">Categories</p>
                </div>""", unsafe_allow_html=True)

            with c3:
                st.markdown(f"""<div class="stat-card">
                    <p class="stat-num" style="font-size:32px;">💪</p>
                    <p class="stat-label">Ready to Apply!</p>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            for cat, cat_skills in categories.items():
                st.markdown(f"<p class='cat-label'>{cat}</p>", unsafe_allow_html=True)
                tags = "".join(f'<span class="skill-tag">✓ {s}</span>' for s in cat_skills)
                st.markdown(tags, unsafe_allow_html=True)

            st.divider()

            counts = {k: len(v) for k, v in categories.items()}
            fig = px.bar(
                x=list(counts.keys()),
                y=list(counts.values()),
                labels={"x": "Category", "y": "Number of Skills"},
                color=list(counts.values()),
                color_continuous_scale=[[0, "#2d2a45"], [1, ACCENT]]
            )
            fig.update_layout(
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=TEXT, family="Inter", size=12),
                coloraxis_showscale=False,
                margin=dict(t=20, b=20)
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════════════════════════
    # TAB 2 ─ JOB MATCHES
    # ══════════════════════════════════════════════════════════
    with tab2:
        st.markdown(f"<p class='section-title'>Job Match Results</p>", unsafe_allow_html=True)

        with st.spinner("Analyzing job matches..."):
            results = match_all_jobs(skills)

        top = get_top_match(results)
        if top:
            st.markdown(f"""
            <div class="top-banner">
                <p class="top-banner-title">🏆 Your Best Match</p>
                <h2 class="top-banner-role">{top['icon']} {top['job']}</h2>
                <p class="top-banner-score">{top['score']}%</p>
                <p class="top-banner-desc">{top['description']}</p>
            </div>
            """, unsafe_allow_html=True)

        for job in results[:max_jobs]:
            score_color = SUCCESS if job['score'] >= 70 else WARNING if job['score'] >= 40 else DANGER

            with st.expander(f"{job['icon']}  {job['job']} — {job['score']}% match", expanded=False):
                col_left, col_right = st.columns([3, 1])

                with col_left:
                    st.markdown(f"<p style='color:{TEXT_DIM}; font-size:14px; margin:0 0 6px;'>{job['description']}</p>",
                                unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:14px; font-weight:600; margin:0 0 10px; color:{ACCENT_2};'>💰 {job['avg_salary']}</p>",
                                unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="prog-bg">
                        <div class="prog-fill" style="width:{job['score']}%; background:{score_color};"></div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_right:
                    st.markdown(f"""
                    <div class="stat-card" style="padding:14px;">
                        <p class="stat-num" style="font-size:32px; color:{score_color};">{job['score']}%</p>
                        <p class="stat-label">{job['total_matched']}/{job['total_required']} skills</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<p style='font-weight:700; color:{SUCCESS}; font-size:14px; text-transform:uppercase; letter-spacing:0.5px;'>✅ Your Skills:</p>",
                                unsafe_allow_html=True)
                    if job['matched_skills']:
                        tags = "".join(f'<span class="have-tag">{s}</span>' for s in job['matched_skills'])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='color:{TEXT_FAINT}; font-size:13px;'>No matched skills yet</p>", unsafe_allow_html=True)

                with col2:
                    st.markdown(f"<p style='font-weight:700; color:{DANGER}; font-size:14px; text-transform:uppercase; letter-spacing:0.5px;'>❌ To Learn:</p>",
                                unsafe_allow_html=True)
                    if job['missing_skills']:
                        tags = "".join(f'<span class="missing-tag">{s}</span>' for s in job['missing_skills'][:5])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='color:{SUCCESS}; font-weight:700; font-size:14px;'>🎉 You qualify!</p>",
                                    unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 3 ─ RESUME SCORE
    # ══════════════════════════════════════════════════════════
    with tab3:
        st.markdown(f"<p class='section-title'>Resume Score & Feedback</p>", unsafe_allow_html=True)

        result = score_resume(text, skills, categories)
        grade  = result['grade'].split(' — ')[0]

        grade_color = SUCCESS if result['total_score'] >= 80 else \
                      ACCENT_2 if result['total_score'] >= 65 else \
                      WARNING if result['total_score'] >= 50 else DANGER

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="stat-card">
                <p class="stat-num" style="color:{grade_color};">{result['total_score']}</p>
                <p class="stat-label">Out of 100</p>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"""<div class="stat-card">
                <p class="stat-num" style="font-size:40px; color:{grade_color};">{grade}</p>
                <p class="stat-label">Overall Grade</p>
            </div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"""<div class="stat-card">
                <p class="stat-num">{result['word_count']}</p>
                <p class="stat-label">Words</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        fig2 = px.bar(
            x=list(result['breakdown'].keys()),
            y=list(result['breakdown'].values()),
            color=list(result['breakdown'].values()),
            color_continuous_scale=[[0, "#3a2a3a"], [1, ACCENT]],
            labels={"x": "", "y": "Points"}
        )
        fig2.update_layout(
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT, family="Inter", size=12),
            coloraxis_showscale=False,
            xaxis_tickangle=-20,
            margin=dict(t=10, b=10)
        )
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"<p class='section-title'>💡 How to Improve</p>", unsafe_allow_html=True)

        if result['feedback']:
            for tip in result['feedback']:
                st.markdown(f'<div class="tip-card">{tip}</div>',
                            unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:rgba(61,220,151,0.08); border:1px solid rgba(61,220,151,0.3); border-radius:10px; padding:14px 18px;">
                <p style="color:{SUCCESS}; font-weight:700; margin:0; font-size:15px;">🌟 Excellent Resume!</p>
                <p style="color:{SUCCESS}; font-size:13px; margin:6px 0 0; opacity:0.85;">Your resume is well-structured with no major issues.</p>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 4 ─ INTERVIEW PREP
    # ══════════════════════════════════════════════════════════
    with tab4:
        st.markdown(f"<p class='section-title'>Interview Preparation</p>", unsafe_allow_html=True)

        qs    = generate_interview_questions(skills, q_per_skill)
        total = get_total_question_count(qs)

        st.markdown(f"""
        <div style="background:rgba(124,92,255,0.08); 
                    border:1px solid {BORDER}; border-radius:10px; padding:14px 18px; margin-bottom:16px;">
            <p style="color:{ACCENT_2}; font-weight:700; font-size:15px; margin:0;">
                🎯 Generated <strong>{total}</strong> interview questions based on your skills!
            </p>
        </div>
        """, unsafe_allow_html=True)

        for skill_name, qlist in qs.items():
            with st.expander(f"📌 {skill_name.title()} — {len(qlist)} questions"):
                for i, q in enumerate(qlist, 1):
                    st.markdown(f'<div class="q-card"><strong>Q{i}.</strong> {q}</div>',
                                unsafe_allow_html=True)

# ─── NO FILE UPLOADED YET ──────────────────────────────────────
else:
    st.markdown(f"""
    <div style="text-align:center; padding:50px 20px; margin-top:10px;">
        <div style="font-size:64px; margin-bottom:18px;">📄</div>
        <h2 style="color:{TEXT}; font-size:26px; margin:0 0 12px; font-weight:700; font-family:'Space Grotesk',sans-serif;">
            Get Started
        </h2>
        <p style="color:{TEXT_DIM}; font-size:15px; max-width:450px; margin:0 auto 28px; line-height:1.7;">
            Upload your resume above to unlock intelligent career insights, job recommendations, and interview preparation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("🧠", "Skill Extraction", "Automatically identifies all your skills from resume"),
        ("🎯", "Job Matching", "Compare against 6+ roles with match percentages"),
        ("📊", "Resume Score", "Get scored out of 100 with improvement tips"),
        ("💬", "Interview Prep", "Generate practice questions for your skills"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center; padding:28px 16px; height:100%;">
                <div style="font-size:38px; margin-bottom:12px;">{icon}</div>
                <p style="font-weight:700; font-size:15px; color:{TEXT}; margin:0 0 8px; font-family:'Space Grotesk',sans-serif;">{title}</p>
                <p style="font-size:13px; color:{TEXT_DIM}; margin:0; line-height:1.6;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)