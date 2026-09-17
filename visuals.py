"""
CancerGuard AI - Visual components.
CSS styling and embedded React components.
"""

import json
import streamlit as st


def _render_html(html, height):
    """Render raw HTML, supporting both old and new Streamlit APIs."""
    if hasattr(st, "iframe"):
        st.iframe(html, height=height)
    else:
        import streamlit.components.v1 as components
        components.html(html, height=height)


# =====================================================
# GLOBAL CSS THEME
# =====================================================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #FDF2F8 0%, #F8FAFC 45%, #F1F5F9 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

.stApp, .stApp p, .stApp li, .stApp span, .stApp label,
.stApp div[data-testid="stMarkdownContainer"] {
    color: #0F172A;
}

h1 {
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0F172A !important;
}

h2, h3, h4 {
    font-weight: 700;
    color: #1E293B !important;
}

.stApp [data-testid="stCaptionContainer"] {
    color: #64748B !important;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border: 1px solid #EC4899 !important;
    box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.18) !important;
}

.stTextInput input::placeholder {
    color: #94A3B8 !important;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stSlider label,
.stMultiSelect label,
.stRadio label,
.stCheckbox label {
    color: #334155 !important;
    font-weight: 600;
}

.stTextInput button svg {
    fill: #475569 !important;
}

.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #BE185D 0%, #9D174D 100%);
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
    box-shadow: none;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 26px rgba(190, 24, 93, 0.14);
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] div {
    color: #0F172A !important;
}

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 12px;
    font-weight: 700;
    border: none;
    padding: 0.55rem 1.4rem;
    background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%);
    color: #FFFFFF !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(190, 24, 93, 0.35);
    color: #FFFFFF !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #FFFFFF;
    padding: 8px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    flex-wrap: wrap;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-weight: 600;
    padding: 8px 16px;
    color: #475569 !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%);
    color: #FFFFFF !important;
}

.stTabs [aria-selected="true"] p {
    color: #FFFFFF !important;
}

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px;
}

div[data-testid="stExpander"] {
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    background: #FFFFFF;
}

.stChatMessage {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
}

.app-footer {
    text-align: center;
    padding: 24px;
    color: #64748B;
    font-size: 14px;
}
</style>
"""


# =====================================================
# ANIMATED BACKGROUND (safe - cannot cover content)
# =====================================================
ANIMATED_BACKGROUND = """
<style>
[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(
            circle at 15% 20%,
            rgba(236, 72, 153, 0.12) 0%,
            rgba(236, 72, 153, 0) 42%
        ),
        radial-gradient(
            circle at 85% 75%,
            rgba(124, 58, 237, 0.12) 0%,
            rgba(124, 58, 237, 0) 45%
        ),
        radial-gradient(
            circle at 50% 50%,
            rgba(56, 189, 248, 0.08) 0%,
            rgba(56, 189, 248, 0) 38%
        );
    background-attachment: fixed;
    background-size: 220% 220%;
    animation: bgDrift 34s ease-in-out infinite alternate;
}

@keyframes bgDrift {
    0%   { background-position: 0% 0%, 100% 100%, 50% 50%; }
    50%  { background-position: 30% 25%, 70% 65%, 35% 60%; }
    100% { background-position: 12% 40%, 85% 30%, 60% 40%; }
}

@media (prefers-reduced-motion: reduce) {
    [data-testid="stAppViewContainer"] {
        animation: none;
    }
}
</style>
"""


# =====================================================
# HERO BANNER
# =====================================================
def hero_banner(title, subtitle, tagline, height=250):
    """Render an animated gradient hero header."""
    html = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
      body {{ margin: 0; font-family: 'Inter', sans-serif; }}
      @keyframes gradientMove {{
          0%   {{ background-position: 0% 50%; }}
          50%  {{ background-position: 100% 50%; }}
          100% {{ background-position: 0% 50%; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
          .hb-wrap {{ animation: none; }}
      }}
      .hb-wrap {{
          background: linear-gradient(120deg, #BE185D, #7C3AED, #0EA5E9);
          background-size: 300% 300%;
          animation: gradientMove 14s ease infinite;
          border-radius: 22px;
          padding: 42px 34px;
          color: white;
          box-shadow: 0 18px 40px rgba(124, 58, 237, 0.26);
      }}
    </style>

    <div class="hb-wrap">
        <div style="font-size: 13px; letter-spacing: 3px;
                    text-transform: uppercase; opacity: 0.85;">
            {tagline}
        </div>
        <div style="font-size: 42px; font-weight: 800;
                    margin-top: 10px; line-height: 1.1;">
            {title}
        </div>
        <div style="font-size: 17px; margin-top: 12px;
                    opacity: 0.92; max-width: 640px;">
            {subtitle}
        </div>
    </div>
    """
    _render_html(html, height)


# =====================================================
# COMPACT DASHBOARD STRIP
# =====================================================
def dashboard_strip(username, stats, height=185):
    """
    Compact welcome bar with inline stats.

    stats: list of dicts with keys
        label, value, percent
    """
    items = ""

    for stat in stats:
        items += f"""
        <div class="ds-item">
            <div class="ds-val">{stat['value']}</div>
            <div class="ds-lab">{stat['label']}</div>
            <div class="ds-track">
                <div class="ds-fill"
                     style="width:{stat['percent']}%"></div>
            </div>
        </div>
        """

    html = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
      body {{ margin: 0; font-family: 'Inter', sans-serif; }}

      .ds-wrap {{
          background: linear-gradient(120deg, #BE185D, #7C3AED, #0EA5E9);
          background-size: 280% 280%;
          animation: dsShift 18s ease infinite;
          border-radius: 18px;
          padding: 22px 26px;
          color: #FFFFFF;
          display: flex;
          align-items: center;
          gap: 26px;
          flex-wrap: wrap;
          box-shadow: 0 12px 30px rgba(124,58,237,.24);
      }}

      .ds-hello {{ flex: 1 1 200px; min-width: 190px; }}

      .ds-name {{
          font-size: 24px;
          font-weight: 800;
          line-height: 1.15;
      }}

      .ds-sub {{
          font-size: 13px;
          opacity: .88;
          margin-top: 4px;
      }}

      .ds-stats {{
          display: flex;
          gap: 14px;
          flex-wrap: wrap;
      }}

      .ds-item {{
          background: rgba(255,255,255,.15);
          border: 1px solid rgba(255,255,255,.24);
          border-radius: 12px;
          padding: 12px 16px;
          min-width: 106px;
      }}

      .ds-val {{
          font-size: 23px;
          font-weight: 800;
          line-height: 1;
      }}

      .ds-lab {{
          font-size: 11px;
          letter-spacing: 1.1px;
          text-transform: uppercase;
          opacity: .86;
          margin-top: 5px;
      }}

      .ds-track {{
          margin-top: 9px;
          height: 5px;
          border-radius: 99px;
          background: rgba(255,255,255,.28);
          overflow: hidden;
      }}

      .ds-fill {{
          height: 100%;
          background: #FFFFFF;
          border-radius: 99px;
          animation: dsGrow 1.1s cubic-bezier(.22,1,.36,1);
      }}

      @keyframes dsShift {{
          0%   {{ background-position: 0% 50%; }}
          50%  {{ background-position: 100% 50%; }}
          100% {{ background-position: 0% 50%; }}
      }}

      @keyframes dsGrow {{
          from {{ width: 0; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
          .ds-wrap, .ds-fill {{ animation: none; }}
      }}
    </style>

    <div class="ds-wrap">
      <div class="ds-hello">
        <div class="ds-name">Welcome back, {username}</div>
        <div class="ds-sub">Track your habits and build awareness.</div>
      </div>
      <div class="ds-stats">{items}</div>
    </div>
    """
    _render_html(html, height)


# =====================================================
# REACT STAT CARDS
# =====================================================
def react_stat_cards(cards, height=230):
    """
    Render animated stat cards using React.

    cards: list of dicts with keys
        label, value, unit, percent, color
    """
    payload = json.dumps(cards)

    html = f"""
    <div id="cg-stats"></div>

    <script crossorigin
        src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin
        src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

    <style>
      body {{ margin: 0; font-family: 'Inter', system-ui, sans-serif; }}
      .cg-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
          gap: 16px;
      }}
      .cg-card {{
          border-radius: 18px;
          padding: 20px;
          color: white;
          overflow: hidden;
          box-shadow: 0 10px 26px rgba(15,23,42,0.16);
          transition: transform .25s ease, box-shadow .25s ease;
      }}
      .cg-card:hover {{
          transform: translateY(-6px);
          box-shadow: 0 18px 36px rgba(15,23,42,0.24);
      }}
      .cg-label {{
          font-size: 12px;
          letter-spacing: 1.4px;
          text-transform: uppercase;
          opacity: .88;
      }}
      .cg-value {{
          font-size: 34px;
          font-weight: 800;
          margin-top: 8px;
          line-height: 1;
      }}
      .cg-unit {{ font-size: 14px; opacity: .85; margin-left: 5px; }}
      .cg-track {{
          margin-top: 16px;
          height: 7px;
          border-radius: 99px;
          background: rgba(255,255,255,.28);
          overflow: hidden;
      }}
      .cg-fill {{
          height: 100%;
          border-radius: 99px;
          background: white;
          transition: width 1.1s cubic-bezier(.22,1,.36,1);
      }}
    </style>

    <script>
      const cards = {payload};
      const e = React.createElement;

      function Card(props) {{
        const [w, setW] = React.useState(0);
        const [n, setN] = React.useState(0);

        React.useEffect(() => {{
          const t = setTimeout(() => setW(props.percent), 120);
          return () => clearTimeout(t);
        }}, []);

        React.useEffect(() => {{
          let frame = 0;
          const total = 34;
          const id = setInterval(() => {{
            frame++;
            setN(Math.round(props.value * (frame / total)));
            if (frame >= total) {{
              setN(props.value);
              clearInterval(id);
            }}
          }}, 18);
          return () => clearInterval(id);
        }}, []);

        return e('div', {{
            className: 'cg-card',
            style: {{ background: props.color }}
          }},
          e('div', {{ className: 'cg-label' }}, props.label),
          e('div', {{ className: 'cg-value' }},
            n,
            e('span', {{ className: 'cg-unit' }}, props.unit)
          ),
          e('div', {{ className: 'cg-track' }},
            e('div', {{ className: 'cg-fill', style: {{ width: w + '%' }} }})
          )
        );
      }}

      function Grid() {{
        return e('div', {{ className: 'cg-grid' }},
          cards.map((c, i) => e(Card, Object.assign({{ key: i }}, c)))
        );
      }}

      ReactDOM.createRoot(
        document.getElementById('cg-stats')
      ).render(e(Grid));
    </script>
    """
    _render_html(html, height)


# =====================================================
# REACT PROGRESS RINGS
# =====================================================
def react_progress_rings(rings, height=220):
    """
    Render animated circular progress rings using React.

    rings: list of dicts with keys
        label, percent, color
    """
    payload = json.dumps(rings)

    html = f"""
    <div id="cg-rings"></div>

    <script crossorigin
        src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin
        src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

    <style>
      body {{ margin: 0; font-family: 'Inter', system-ui, sans-serif; }}
      .cg-rings {{
          display: flex;
          flex-wrap: wrap;
          gap: 26px;
          justify-content: center;
      }}
      .cg-ring-item {{ text-align: center; }}
      .cg-ring-label {{
          margin-top: 10px;
          font-size: 13px;
          font-weight: 600;
          color: #334155;
      }}
    </style>

    <script>
      const rings = {payload};
      const e = React.createElement;
      const R = 52;
      const C = 2 * Math.PI * R;

      function Ring(props) {{
        const [p, setP] = React.useState(0);

        React.useEffect(() => {{
          const t = setTimeout(() => setP(props.percent), 150);
          return () => clearTimeout(t);
        }}, []);

        const offset = C - (p / 100) * C;

        return e('div', {{ className: 'cg-ring-item' }},
          e('svg', {{ width: 130, height: 130 }},
            e('circle', {{
              cx: 65, cy: 65, r: R, fill: 'none',
              stroke: '#E2E8F0', strokeWidth: 12
            }}),
            e('circle', {{
              cx: 65, cy: 65, r: R, fill: 'none',
              stroke: props.color, strokeWidth: 12,
              strokeLinecap: 'round',
              strokeDasharray: C,
              strokeDashoffset: offset,
              transform: 'rotate(-90 65 65)',
              style: {{
                transition: 'stroke-dashoffset 1.2s cubic-bezier(.22,1,.36,1)'
              }}
            }}),
            e('text', {{
              x: 65, y: 72, textAnchor: 'middle',
              fontSize: 24, fontWeight: 800, fill: '#0F172A'
            }}, Math.round(p) + '%')
          ),
          e('div', {{ className: 'cg-ring-label' }}, props.label)
        );
      }}

      function Rings() {{
        return e('div', {{ className: 'cg-rings' }},
          rings.map((r, i) => e(Ring, Object.assign({{ key: i }}, r)))
        );
      }}

      ReactDOM.createRoot(
        document.getElementById('cg-rings')
      ).render(e(Rings));
    </script>
    """
    _render_html(html, height)


# =====================================================
# TABLE RENDERER (no pyarrow required)
# =====================================================
def render_table(dataframe):
    """Render a DataFrame as an HTML table without pyarrow."""
    html = dataframe.to_html(
        index=False,
        border=0,
        classes="cg-table",
        escape=True
    )

    style = """
    <style>
    .cg-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }
    .cg-table th {
        background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%);
        color: #FFFFFF;
        text-align: left;
        padding: 11px 13px;
        font-weight: 700;
    }
    .cg-table td {
        padding: 10px 13px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A;
        background: #FFFFFF;
    }
    .cg-table tr:nth-child(even) td {
        background: #F8FAFC;
    }
    .cg-table tr:hover td {
        background: #FDF2F8;
    }
    </style>
    """

    st.markdown(style + html, unsafe_allow_html=True)


# =====================================================
# PLOTLY THEME HELPER
# =====================================================
def style_chart(fig):
    """Apply a consistent clean theme to any Plotly figure."""
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Inter, sans-serif", size=13, color="#334155"),
        title_font=dict(size=17, color="#0F172A"),
        margin=dict(l=20, r=20, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=12),
        showlegend=False
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#E2E8F0")
    return fig