"""
CancerGuard AI - Image library.

All images are from Unsplash under the Unsplash License,
which permits free commercial and non-commercial use.
Images are chosen to be non-distressing and to avoid
implying clinical care or diagnosis.
"""

import streamlit as st


def _render_html(html, height):
    """Render raw HTML, supporting both old and new Streamlit APIs."""
    if hasattr(st, "iframe"):
        st.iframe(html, height=height)
    else:
        import streamlit.components.v1 as components
        components.html(html, height=height)


# =====================================================
# IMAGE URLS
# =====================================================
IMAGES = {
    "hero_health": (
        "https://images.unsplash.com/photo-1505576399279-565b52d4ac71"
        "?w=1400&q=80"
    ),
    "prevention": (
        "https://images.unsplash.com/photo-1490645935967-10de6ba17061"
        "?w=1200&q=80"
    ),
    "vegetables": (
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd"
        "?w=1200&q=80"
    ),
    "walking": (
        "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8"
        "?w=1200&q=80"
    ),
    "running": (
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b"
        "?w=1200&q=80"
    ),
    "water": (
        "https://images.unsplash.com/photo-1548839140-29a749e1cf4d"
        "?w=1200&q=80"
    ),
    "sleep": (
        "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55"
        "?w=1200&q=80"
    ),
    "sunlight": (
        "https://images.unsplash.com/photo-1500534623283-312aade485b7"
        "?w=1200&q=80"
    ),
    "education": (
        "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f"
        "?w=1200&q=80"
    ),
    "library": (
        "https://images.unsplash.com/photo-1507842217343-583bb7270b66"
        "?w=1200&q=80"
    ),
    "research": (
        "https://images.unsplash.com/photo-1576086213369-97a306d36557"
        "?w=1200&q=80"
    ),
    "laboratory": (
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b"
        "?w=1200&q=80"
    ),
    "data": (
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
        "?w=1200&q=80"
    ),
    "community": (
        "https://images.unsplash.com/photo-1529156069898-49953e39b3ac"
        "?w=1200&q=80"
    ),
    "support": (
        "https://images.unsplash.com/photo-1516726817505-f5ed825624d8"
        "?w=1200&q=80"
    ),
    "hands": (
        "https://images.unsplash.com/photo-1521791136064-7986c2920216"
        "?w=1200&q=80"
    ),
    "sunrise": (
        "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8"
        "?w=1200&q=80"
    ),
    "path": (
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e"
        "?w=1200&q=80"
    ),
    "goals": (
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173"
        "?w=1200&q=80"
    ),
    "clinic": (
        "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d"
        "?w=1200&q=80"
    )
}


# =====================================================
# BANNER WITH IMAGE
# =====================================================
def image_banner(image_key, title, subtitle="", height=260):
    """Render a full-width image banner with an overlay caption."""
    url = IMAGES.get(image_key, IMAGES["hero_health"])

    sub = (
        f"<div style='font-size:16px;margin-top:10px;"
        f"opacity:.94;max-width:640px;line-height:1.6;'>{subtitle}</div>"
        if subtitle else ""
    )

    html = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
      body {{ margin: 0; font-family: 'Inter', sans-serif; }}
      .ib-wrap {{
          position: relative;
          border-radius: 16px;
          overflow: hidden;
          height: {height - 20}px;
      }}
      .ib-img {{
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
      }}
      .ib-overlay {{
          position: absolute;
          inset: 0;
          background: linear-gradient(
              90deg,
              rgba(190,24,93,.93) 0%,
              rgba(157,23,77,.80) 45%,
              rgba(124,58,237,.45) 100%
          );
          display: flex;
          flex-direction: column;
          justify-content: center;
          padding: 0 40px;
          color: #FFFFFF;
      }}
      .ib-title {{
          font-size: 34px;
          font-weight: 800;
          line-height: 1.15;
      }}
    </style>

    <div class="ib-wrap">
      <img class="ib-img" src="{url}" alt="">
      <div class="ib-overlay">
        <div class="ib-title">{title}</div>
        {sub}
      </div>
    </div>
    """
    _render_html(html, height)


# =====================================================
# IMAGE CARD GRID
# =====================================================
def image_cards(cards, height=340):
    """
    Render a grid of image cards.

    cards: list of dicts with keys
        image, tag, title, description
    """
    cards_html = ""

    for card in cards:
        url = IMAGES.get(card["image"], IMAGES["hero_health"])
        cards_html += f"""
        <div class="ic-card">
            <div class="ic-imgwrap">
                <img class="ic-img" src="{url}" alt="">
            </div>
            <div class="ic-body">
                <div class="ic-tag">{card['tag']}</div>
                <div class="ic-title">{card['title']}</div>
                <div class="ic-desc">{card['description']}</div>
            </div>
        </div>
        """

    html = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
      body {{ margin: 0; font-family: 'Inter', sans-serif; }}
      .ic-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 18px;
      }}
      .ic-card {{
          background: #FFFFFF;
          border: 1px solid #E2E8F0;
          border-radius: 16px;
          overflow: hidden;
          transition: box-shadow .22s ease, transform .22s ease;
      }}
      .ic-card:hover {{
          box-shadow: 0 10px 26px rgba(190,24,93,.18);
          transform: translateY(-4px);
      }}
      .ic-imgwrap {{ height: 148px; overflow: hidden; }}
      .ic-img {{
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
          transition: transform .5s ease;
      }}
      .ic-card:hover .ic-img {{ transform: scale(1.07); }}
      .ic-body {{ padding: 16px 18px 20px; }}
      .ic-tag {{
          font-size: 11px;
          letter-spacing: 1.6px;
          text-transform: uppercase;
          color: #BE185D;
          font-weight: 700;
      }}
      .ic-title {{
          font-size: 18px;
          font-weight: 800;
          color: #0F172A;
          margin-top: 7px;
      }}
      .ic-desc {{
          font-size: 13.5px;
          color: #64748B;
          margin-top: 7px;
          line-height: 1.55;
      }}
    </style>

    <div class="ic-grid">{cards_html}</div>
    """
    _render_html(html, height)


# =====================================================
# SIMPLE FRAMED IMAGE
# =====================================================
def framed_image(image_key, caption="", height=300):
    """Render a single image with a caption bar."""
    url = IMAGES.get(image_key, IMAGES["hero_health"])

    cap = (
        f"<div class='fi-cap'>{caption}</div>"
        if caption else ""
    )

    html = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
      body {{ margin: 0; font-family: 'Inter', sans-serif; }}
      .fi-wrap {{
          border: 1px solid #E2E8F0;
          border-radius: 16px;
          overflow: hidden;
          background: #FFFFFF;
      }}
      .fi-img {{
          width: 100%;
          height: {height - 62}px;
          object-fit: cover;
          display: block;
      }}
      .fi-cap {{
          padding: 11px 16px;
          font-size: 13px;
          color: #64748B;
          border-top: 3px solid #EC4899;
          background: #F8FAFC;
      }}
    </style>

    <div class="fi-wrap">
      <img class="fi-img" src="{url}" alt="">
      {cap}
    </div>
    """
    _render_html(html, height)