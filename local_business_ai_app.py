"""
LOCAL BUSINESS AI — Session 4 Demo App
Developer : Emre Yildiz
Mentor    : Ahsan K., data_analytica

Run: streamlit run local_business_ai_app.py
"""

import streamlit as st
import requests
import time
import json

# ── Page Setup ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Local Business AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Design System ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

/* ── Reset & Base ── */
* { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #f0ede8; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1a1a1a !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #e8e4dc !important; }
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stTextArea > div > div > textarea,
[data-testid="stSidebar"] .stSelectbox > div > div > div {
    background: #2a2a2a !important;
    border: 1px solid #3a3a3a !important;
    color: #e8e4dc !important;
    border-radius: 6px !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Top Banner ── */
.top-banner {
    background: #1a1a1a;
    color: #e8e4dc;
    padding: 28px 36px 24px;
    margin: -1rem -1rem 2rem -1rem;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
}
.banner-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 6px;
}
.banner-sub {
    font-size: 0.85rem;
    color: #888;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}
.banner-tag {
    background: #e8ff3c;
    color: #1a1a1a;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 2px;
    margin-top: 4px;
    display: inline-block;
}

/* ── Stat Cards ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 24px;
}
.stat-card {
    background: #1a1a1a;
    color: #e8e4dc;
    padding: 20px 22px;
    border-radius: 8px;
}
.stat-number {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #e8ff3c;
    line-height: 1;
}
.stat-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #888;
    margin-top: 6px;
    font-weight: 500;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #1a1a1a;
}
.section-icon {
    background: #1a1a1a;
    color: #e8ff3c;
    width: 36px;
    height: 36px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a1a;
    letter-spacing: -0.02em;
}
.section-badge {
    background: #e8ff3c;
    color: #1a1a1a;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
    margin-left: auto;
}

/* ── Lead Cards ── */
.lead-card {
    background: white;
    border: 1px solid #e0ddd8;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: border-color 0.15s;
}
.lead-card:hover { border-color: #1a1a1a; }
.lead-avatar {
    background: #1a1a1a;
    color: #e8ff3c;
    width: 38px;
    height: 38px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    font-weight: 700;
    flex-shrink: 0;
}
.lead-name { font-weight: 700; font-size: 0.9rem; color: #1a1a1a; }
.lead-meta { font-size: 0.78rem; color: #888; margin-top: 2px; }
.lead-email {
    margin-left: auto;
    font-family: 'Fira Code', monospace;
    font-size: 0.75rem;
    color: #555;
    background: #f5f2ee;
    padding: 3px 10px;
    border-radius: 4px;
}

/* ── AI Output Cards ── */
.ai-output {
    background: #1a1a1a;
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 12px;
}
.ai-output-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #2a2a2a;
}
.ai-output-to {
    font-family: 'Fira Code', monospace;
    font-size: 0.78rem;
    color: #888;
}
.ai-output-text {
    color: #e8e4dc;
    font-size: 0.88rem;
    line-height: 1.7;
}
.ai-chip {
    background: #e8ff3c;
    color: #1a1a1a;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 2px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── SMS Card ── */
.sms-card {
    background: white;
    border: 1px solid #e0ddd8;
    border-radius: 12px;
    padding: 20px;
    max-width: 360px;
    margin: 0 auto;
}
.sms-header {
    text-align: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #e0ddd8;
}
.sms-business {
    font-weight: 700;
    font-size: 0.85rem;
    color: #1a1a1a;
}
.sms-number { font-size: 0.72rem; color: #888; margin-top: 2px; }
.sms-bubble {
    background: #1a1a1a;
    color: #e8e4dc;
    padding: 14px 16px;
    border-radius: 16px 16px 4px 16px;
    font-size: 0.88rem;
    line-height: 1.6;
    margin-bottom: 8px;
}
.sms-timestamp {
    font-size: 0.68rem;
    color: #aaa;
    text-align: right;
}

/* ── Chat ── */
.chat-msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 8px 0;
}
.chat-msg-bot {
    display: flex;
    justify-content: flex-start;
    margin: 8px 0;
}
.chat-bubble-user {
    background: #1a1a1a;
    color: #e8e4dc;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    font-size: 0.88rem;
    max-width: 72%;
    line-height: 1.5;
}
.chat-bubble-bot {
    background: white;
    color: #1a1a1a;
    border: 1px solid #e0ddd8;
    padding: 10px 16px;
    border-radius: 18px 18px 18px 4px;
    font-size: 0.88rem;
    max-width: 72%;
    line-height: 1.5;
}

/* ── Buttons ── */
.stButton > button {
    background: #1a1a1a !important;
    color: #e8ff3c !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    padding: 10px 22px !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Code note ── */
.code-note {
    background: #fff8dc;
    border: 1px solid #e8cc5a;
    border-left: 3px solid #e8cc5a;
    border-radius: 6px;
    padding: 12px 16px;
    font-size: 0.8rem;
    color: #5a4a00;
    margin: 12px 0;
    font-family: 'Fira Code', monospace;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid #d0cdc8 !important;
    border-radius: 6px !important;
    font-family: 'Syne', sans-serif !important;
    background: white !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #1a1a1a !important;
    box-shadow: none !important;
}

/* ── Misc ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid #d0cdc8;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    color: #888 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    font-family: 'Syne', sans-serif !important;
    letter-spacing: 0.02em !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #1a1a1a !important;
    border-bottom: 2px solid #1a1a1a !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def call_groq(api_key, system_prompt, user_message, max_tokens=350):
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile",
                  "messages": [{"role": "system", "content": system_prompt},
                                {"role": "user",   "content": user_message}],
                  "temperature": 0.7, "max_tokens": max_tokens},
            timeout=20
        )
        data = r.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        return f"API Error: {data.get('error', {}).get('message', 'Unknown')}"
    except Exception as e:
        return f"Connection error: {e}"


def fetch_leads(count=5):
    leads = []
    for i in range(1, count + 1):
        try:
            raw = requests.get(
                f"https://jsonplaceholder.typicode.com/users/{i}", timeout=5
            ).json()
            leads.append({
                "id": i,
                "name":    raw.get("name", "Unknown"),
                "email":   raw.get("email", ""),
                "company": raw.get("company", {}).get("name", "Unknown Co."),
                "city":    raw.get("address", {}).get("city", "Unknown"),
                "initials": raw.get("name", "?")[0].upper()
            })
        except:
            pass
    return leads


# ── Business Info Templates (updates when dropdown changes) ──────────────────
BIZ_TEMPLATES = {
    "Plumbing & Emergency Repair": {
        "name": "Visser Plumbing",
        "city": "Amsterdam",
        "info": """Business: Visser Plumbing, Amsterdam
Services: Emergency plumbing, pipe repair, boiler installation, drain unblocking
Hours: Mon–Fri 8am–6pm | Sat 9am–2pm | Sun closed
Emergency: 24/7 for burst pipes and urgent leaks
Response: Within 2 hours for emergencies | Same-day for standard jobs
Pricing: Free quote | No call-out fee for estimates"""
    },
    "Electrical Services": {
        "name": "Spark Electrical",
        "city": "Rotterdam",
        "info": """Business: Spark Electrical, Rotterdam
Services: Wiring, fuse board upgrades, EV charger installation, fault finding, lighting
Hours: Mon–Fri 7:30am–5:30pm | Sat 8am–1pm | Sun closed
Emergency: 24/7 callout for power failures and electrical faults
Response: Same-day for emergencies | Next-day for standard
Pricing: Free quote | Fixed-price jobs available"""
    },
    "Dental Practice": {
        "name": "Smile Studio",
        "city": "Utrecht",
        "info": """Business: Smile Studio Dental Practice, Utrecht
Services: Check-ups, teeth whitening, fillings, extractions, implants, Invisalign
Hours: Mon–Fri 8am–6pm | Sat 9am–1pm | Sun closed
Emergency: Same-day slots available for dental pain and broken teeth
New patients: Welcome — book online or call
Pricing: NHS and private options available | Free consultation for implants"""
    },
    "Physiotherapy Clinic": {
        "name": "Motion Physio",
        "city": "The Hague",
        "info": """Business: Motion Physiotherapy Clinic, The Hague
Services: Sports injuries, back and neck pain, post-surgery rehab, massage therapy
Hours: Mon–Fri 7am–8pm | Sat 8am–3pm | Sun closed
Appointments: Online booking available | Same-week slots usually available
Session length: 30 or 60 minutes
Pricing: From €55 per session | Health insurance accepted"""
    },
    "Hair Salon & Beauty": {
        "name": "Studio Noir",
        "city": "Amsterdam",
        "info": """Business: Studio Noir Hair & Beauty, Amsterdam
Services: Haircuts, colour, balayage, keratin treatments, nails, eyebrow threading
Hours: Tue–Sat 9am–7pm | Sun 10am–5pm | Mon closed
Booking: Walk-ins welcome if available | Online booking recommended
Team: 6 senior stylists | All colour treatments by appointment
Pricing: Cuts from €35 | Colour from €75 | Free consultation for first colour"""
    },
    "Auto Repair Shop": {
        "name": "AutoFix Garage",
        "city": "Eindhoven",
        "info": """Business: AutoFix Garage, Eindhoven
Services: MOT/APK, servicing, brakes, tyres, diagnostics, bodywork, air conditioning
Hours: Mon–Fri 8am–6pm | Sat 8am–2pm | Sun closed
Turnaround: Most jobs same-day | Courtesy car available on request
Brands: All makes and models | Specialists in German and Japanese vehicles
Pricing: Free diagnostic check | No hidden charges | Written quote before any work"""
    },
    "Personal Training & Gym": {
        "name": "Peak Performance",
        "city": "Groningen",
        "info": """Business: Peak Performance Gym & PT, Groningen
Services: Personal training, group classes, nutrition coaching, body transformation
Hours: Mon–Fri 6am–10pm | Sat–Sun 7am–8pm
Membership: Monthly rolling | No long contracts | Day passes available
Personal training: 1-on-1 and small group sessions | First session free
Classes: HIIT, yoga, spin, strength — full schedule online"""
    },
    "Restaurant & Catering": {
        "name": "Casa Mia",
        "city": "Maastricht",
        "info": """Business: Casa Mia Italian Restaurant, Maastricht
Services: Dine-in, takeaway, private dining, catering for events
Hours: Tue–Sun 12pm–10pm | Mon closed | Kitchen closes 9:30pm
Reservations: Recommended for weekends | Walk-ins welcome weekdays
Capacity: 60 covers | Private room for up to 20 guests
Menu: Fresh pasta, wood-fired pizza, seasonal specials | Vegetarian options available"""
    }
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px;">
        <div style="font-size:1.3rem; font-weight:800; letter-spacing:-0.03em;">
            ⚡ Configuration
        </div>
        <div style="font-size:0.72rem; color:#888; text-transform:uppercase;
                    letter-spacing:0.08em; margin-top:4px;">
            Session 4 · data_analytica
        </div>
    </div>
    """, unsafe_allow_html=True)

    groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    if groq_key:
        st.markdown('<div style="color:#e8ff3c; font-size:0.8rem; font-weight:700;">✓ API KEY SET</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#888; font-size:0.78rem;">console.groq.com → free key</div>',
                    unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2a2a2a; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem; color:#888; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">Business Profile</div>',
                unsafe_allow_html=True)

    biz_type = st.selectbox("Service Type", list(BIZ_TEMPLATES.keys()))

    # Track dropdown changes — forces text area to re-render and clears chat
    if st.session_state.get("last_biz_type") != biz_type:
        st.session_state["last_biz_type"] = biz_type
        st.session_state["chat"] = []

    template = BIZ_TEMPLATES[biz_type]
    biz_name = st.text_input("Business Name", value=template["name"])
    biz_city = st.text_input("City", value=template["city"])

    st.markdown("<hr style='border-color:#2a2a2a; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.72rem; color:#666; line-height:1.7;">
        Developer: <span style="color:#e8ff3c; font-weight:700;">Emre Yildiz</span><br>
        Session 4 of 14<br>
        Engine: llama-3.3-70b-versatile<br>
        Status: <span style="color:#e8ff3c;">● live</span>
    </div>
    """, unsafe_allow_html=True)

    lead_count = st.slider("Leads to fetch", 1, 10, 5)


# ── Top Banner ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-banner">
    <div>
        <div class="banner-title">Local Business AI</div>
        <div class="banner-sub">{biz_name} · {biz_city}</div>
        <div class="banner-tag">Session 4 Capstone · Built by Emre Yildiz</div>
    </div>
    <div style="text-align:right; padding-top:4px;">
        <div style="font-size:0.72rem; color:#555; text-transform:uppercase;
                    letter-spacing:0.1em;">Powered by</div>
        <div style="font-size:1rem; font-weight:800; color:#e8ff3c;
                    letter-spacing:-0.02em;">LLaMA 3.3 · 70B</div>
        <div style="font-size:0.7rem; color:#555; margin-top:2px;">via Groq · free tier</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-number">4</div>
        <div class="stat-label">AI Tools Built</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">~80</div>
        <div class="stat-label">Lines of Logic</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">€300+</div>
        <div class="stat-label">Client Value / Setup</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">∞</div>
        <div class="stat-label">Clients, One Script</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋  Lead Scraping",
    "✉  AI Outreach",
    "📱  Missed Call",
    "💬  Chat Responder"
])


# ════════════════════════════════════════════════════════════════════
# TAB 1 — LEAD SCRAPING
# ════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">📋</div>
        <div class="section-title">Lead Scraping</div>
        <div class="section-badge">Tool 1 of 4</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#555; font-size:0.88rem; margin-bottom:20px; line-height:1.6;">
        Fetches real business contacts from the internet automatically.
        In a live system, this connects to Google Maps API or LinkedIn —
        same code, just a different URL.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍  Fetch Leads Now", key="fetch"):
        with st.spinner("Calling the API..."):
            leads = fetch_leads(lead_count)
            st.session_state["leads"] = leads
            time.sleep(0.4)

        st.markdown(f"""
        <div style="color:#1a1a1a; font-size:0.8rem; font-weight:700;
                    text-transform:uppercase; letter-spacing:0.08em;
                    margin-bottom:12px;">
            ✅ {len(leads)} contacts fetched for {biz_name}
        </div>
        """, unsafe_allow_html=True)

        for lead in leads:
            st.markdown(f"""
            <div class="lead-card">
                <div class="lead-avatar">{lead['initials']}</div>
                <div>
                    <div class="lead-name">{lead['name']}</div>
                    <div class="lead-meta">{lead['company']} · {lead['city']}</div>
                </div>
                <div class="lead-email">{lead['email']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="code-note">
        # The code behind this:<br>
        requests.get(url).json()  ← 1 line to fetch a contact<br>
        for i in range(count): fetch_lead(i)  ← loop for the full list
        </div>
        """, unsafe_allow_html=True)

    elif "leads" not in st.session_state:
        st.markdown("""
        <div style="background:white; border:1.5px dashed #d0cdc8; border-radius:8px;
                    padding:40px; text-align:center; color:#aaa; font-size:0.88rem;">
            Press "Fetch Leads Now" to pull live contact data from the API
        </div>
        """, unsafe_allow_html=True)
    else:
        leads = st.session_state["leads"]
        for lead in leads:
            st.markdown(f"""
            <div class="lead-card">
                <div class="lead-avatar">{lead['initials']}</div>
                <div>
                    <div class="lead-name">{lead['name']}</div>
                    <div class="lead-meta">{lead['company']} · {lead['city']}</div>
                </div>
                <div class="lead-email">{lead['email']}</div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 2 — AI OUTREACH
# ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">✉</div>
        <div class="section-title">AI-Personalised Outreach</div>
        <div class="section-badge">Tool 2 of 4</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#555; font-size:0.88rem; margin-bottom:20px; line-height:1.6;">
        AI writes a unique, personalised cold email for every contact.
        Not a template — each message mentions the company name and city specifically.
    </div>
    """, unsafe_allow_html=True)

    if not groq_key:
        st.warning("Add your Groq API key in the sidebar to generate outreach.")
    elif "leads" not in st.session_state:
        st.warning("Fetch leads first in the Lead Scraping tab.")
    else:
        leads = st.session_state["leads"]
        selected = st.multiselect(
            "Select contacts:",
            options=[f"{l['name']} — {l['company']}" for l in leads],
            default=[f"{l['name']} — {l['company']}" for l in leads[:3]]
        )

        if st.button("✉  Generate AI Outreach", key="outreach"):
            selected_names = [s.split(" — ")[0] for s in selected]
            targets = [l for l in leads if l["name"] in selected_names]

            system_prompt = (
                f"You are a B2B outreach specialist for {biz_name}. "
                f"Write warm, specific cold emails for {biz_type} services. "
                f"Under 80 words. NO generic openers like 'I hope this finds you well'. "
                f"Mention company and city. One clear CTA. "
                f"Sound like a real person, not a template."
            )

            for lead in targets:
                with st.spinner(f"Writing for {lead['name']}..."):
                    msg = call_groq(
                        groq_key, system_prompt,
                        f"Write outreach for:\nName: {lead['name']}\n"
                        f"Company: {lead['company']}\nCity: {lead['city']}\n"
                        f"Service: {biz_type}"
                    )

                import html as _html
                safe_msg = _html.escape(msg).replace('\n', '<br>')
                st.markdown(f"""
                <div class="ai-output">
                    <div class="ai-output-header">
                        <div class="ai-chip">AI Generated</div>
                        <div class="ai-output-to">TO: {lead['email']}</div>
                    </div>
                    <div class="ai-output-text">{safe_msg}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="code-note">
            # Behind every message above:<br>
            ask_ai(system_prompt=OUTREACH_PROMPT, user_message=contact_data)<br>
            # That's it. The loop runs it for every contact automatically.
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 3 — MISSED CALL
# ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">📱</div>
        <div class="section-title">Missed-Call Text-Back</div>
        <div class="section-badge">Tool 3 of 4</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#555; font-size:0.88rem; margin-bottom:20px; line-height:1.6;">
        When a business misses a call, this AI sends an automatic SMS reply.
        In production: Twilio detects the missed call and triggers this function.
        No human needed.
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        caller  = st.text_input("Caller Name",  value="Jan de Boer")
        phone   = st.text_input("Phone Number", value="+31 6 9876 5432")
    with col_b:
        call_t  = st.text_input("Time of Call", value="14:32")
        urgency = st.radio("Urgency", ["Standard enquiry", "URGENT — emergency"],
                           horizontal=True)

    if not groq_key:
        st.warning("Add your Groq API key in the sidebar.")
    elif st.button("📱  Generate SMS Reply", key="sms"):
        is_urgent = "URGENT" in urgency
        system_prompt = (
            f"You write short SMS replies for {biz_name}. "
            f"Max 50 words. Use caller's first name only. "
            f"{'For urgent: promise callback within 30 minutes. Acknowledge urgency immediately.' if is_urgent else 'Friendly and warm. Promise callback within the hour.'} "
            f"Sign off as: The {biz_name} Team. "
            f"Sound human and local, not corporate."
        )
        context = "URGENT emergency call — acknowledge immediately." if is_urgent else "Standard enquiry."

        with st.spinner("Generating SMS..."):
            reply = call_groq(
                groq_key, system_prompt,
                f"{biz_name} missed a call from {caller} at {call_t}. {context}",
                max_tokens=120
            )

        # Show as phone SMS bubble
        _, col_mid, _ = st.columns([1, 2, 1])
        with col_mid:
            st.markdown(f"""
            <div class="sms-card">
                <div class="sms-header">
                    <div style="font-size:1.4rem; margin-bottom:6px;">📱</div>
                    <div class="sms-business">{biz_name}</div>
                    <div class="sms-number">{phone}</div>
                    {'<div style="margin-top:6px;"><span style="background:#ff3c3c;color:white;font-size:0.65rem;font-weight:700;padding:2px 8px;border-radius:2px;letter-spacing:0.06em;">URGENT</span></div>' if is_urgent else ''}
                </div>
                <div class="sms-bubble">{reply}</div>
                <div class="sms-timestamp">{call_t} · Sent automatically</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="code-note" style="margin-top:16px;">
        # This fires automatically in production:<br>
        # Twilio webhook → handle_missed_call(caller, phone, time) → SMS sent<br>
        # Zero human involvement. Runs 24/7.
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 4 — CHAT RESPONDER
# ════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">💬</div>
        <div class="section-title">AI Chat Responder</div>
        <div class="section-badge">Tool 4 of 4</div>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_chat = st.columns([1, 1.4])

    with col_info:
        st.markdown("""
        <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.08em; color:#1a1a1a; margin-bottom:8px;">
            Business Knowledge Base
        </div>
        """, unsafe_allow_html=True)

        biz_info = st.text_area(
            "Business info (AI uses this as context)",
            value=template["info"],
            height=200,
            key=f"biz_info_{biz_type}",
            label_visibility="collapsed"
        )

        st.markdown("""
        <div class="code-note">
        Edit this box and re-ask a question.<br>
        Watch how the AI changes its answers.<br>
        Try putting something completely made up in here 👀
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.08em; color:#1a1a1a; margin:16px 0 8px;">
            Quick Questions
        </div>
        """, unsafe_allow_html=True)

        quick_qs = [
            "Do you work weekends?",
            "Emergency — how fast?",
            "Do you charge for quotes?",
            "What services do you offer?"
        ]
        for q in quick_qs:
            if st.button(q, key=f"q_{q}", use_container_width=True):
                st.session_state["pending_q"] = q

    with col_chat:
        st.markdown("""
        <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.08em; color:#1a1a1a; margin-bottom:12px;">
            Live Chat
        </div>
        """, unsafe_allow_html=True)

        if "chat" not in st.session_state:
            st.session_state["chat"] = []

        # Display chat
        chat_html = ""
        for msg in st.session_state["chat"]:
            if msg["role"] == "user":
                chat_html += f'<div class="chat-msg-user"><div class="chat-bubble-user">{msg["text"]}</div></div>'
            else:
                chat_html += f'<div class="chat-msg-bot"><div class="chat-bubble-bot">{msg["text"]}</div></div>'

        if chat_html:
            st.markdown(f"""
            <div id="chat-box" style="background:white; border:1px solid #e0ddd8; border-radius:10px;
                        padding:16px; min-height:200px; max-height:340px;
                        overflow-y:auto; margin-bottom:12px;">
                {chat_html}
                <div id="chat-end"></div>
            </div>
            <script>
                const el = window.parent.document.getElementById('chat-end');
                if (el) el.scrollIntoView();
            </script>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:white; border:1.5px dashed #d0cdc8; border-radius:10px;
                        padding:40px; text-align:center; color:#bbb; font-size:0.85rem;
                        margin-bottom:12px;">
                Type a question or use a quick button ←
            </div>
            """, unsafe_allow_html=True)

        if "input_counter" not in st.session_state:
            st.session_state["input_counter"] = 0

        user_input = st.text_input("Message", placeholder="Ask the chatbot...",
                                   key=f"chat_input_{st.session_state['input_counter']}",
                                   label_visibility="collapsed")
        c1, c2 = st.columns([3, 1])
        with c1:
            send = st.button("Send", key="send_chat", use_container_width=True)
        with c2:
            if st.button("Clear", key="clear_chat", use_container_width=True):
                st.session_state["chat"] = []
                st.rerun()

        # Process message
        q = st.session_state.pop("pending_q", None) or (user_input if send and user_input else None)

        if q:
            if not groq_key:
                st.warning("Add your Groq API key in the sidebar.")
            else:
                st.session_state["chat"].append({"role": "user", "text": q})
                system_prompt = (
                    f"You are the AI assistant for {biz_name} in {biz_city}. "
                    f"Here is information about the business:\n{biz_info}\n"
                    f"Be helpful, conversational, and engaging. "
                    f"Keep responses under 80 words."
                )
                with st.spinner(""):
                    ans = call_groq(groq_key, system_prompt, q, max_tokens=150)
                st.session_state["chat"].append({"role": "bot", "text": ans})
                st.session_state["input_counter"] += 1
                st.rerun()
