import ast
import streamlit as st
from PIIGuard import mask_pii, has_pii

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LoanIQ · AI Loan Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:           #0D0F14;
    --surface:      #13161E;
    --surface-2:    #1A1E2A;
    --border:       #252A38;
    --gold:         #C9A84C;
    --gold-light:   #E8C97A;
    --gold-dim:     rgba(201,168,76,0.15);
    --text:         #E8E6DF;
    --text-muted:   #7A7D8A;
    --user-bg:      #1C2235;
    --ai-bg:        #141820;
    --success:      #4CAF82;
    --danger:       #E05C5C;
    --warning:      #E8A84C;
    --radius:       14px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp { background-color: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

.brand {
    padding: 28px 24px 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.brand-title {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--gold) !important;
    letter-spacing: 0.5px;
    line-height: 1;
}
.brand-sub {
    font-size: 11px;
    color: var(--text-muted) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

.sidebar-section { padding: 0 20px; margin-bottom: 18px; }
.sidebar-label {
    font-size: 10px;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin-bottom: 6px;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    padding: 8px 12px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px var(--gold-dim) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--gold), #A07830) !important;
    color: #0D0F14 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    cursor: pointer !important;
    letter-spacing: 0.3px;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88 !important; }

.chip-grid { display: flex; flex-direction: column; gap: 6px; padding: 0 20px; }
.chip {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.18s;
    line-height: 1.4;
}
.chip:hover { border-color: var(--gold); color: var(--gold-light); background: var(--gold-dim); }

.chat-wrapper { display: flex; flex-direction: column; height: 100vh; background: var(--bg); }

.chat-header {
    padding: 20px 36px 16px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--surface);
}
.chat-header-icon {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: var(--gold-dim);
    border: 1px solid var(--gold);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.chat-header-title {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    font-weight: 600;
    color: var(--text);
}
.chat-header-status {
    font-size: 11px;
    color: var(--success);
    display: flex; align-items: center; gap: 5px;
}
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--success); display: inline-block; }

.messages-container {
    flex: 1; overflow-y: auto; padding: 28px 36px;
    display: flex; flex-direction: column; gap: 22px;
}

.msg-row { display: flex; gap: 12px; align-items: flex-start; }
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 34px; height: 34px; border-radius: 50%;
    flex-shrink: 0; display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 600;
}
.avatar.ai { background: var(--gold-dim); border: 1px solid var(--gold); color: var(--gold); font-family: 'Playfair Display', serif; }
.avatar.user { background: var(--user-bg); border: 1px solid var(--border); color: var(--text-muted); }

.bubble {
    max-width: 68%; padding: 13px 17px; border-radius: var(--radius);
    font-size: 14px; line-height: 1.65;
}
.bubble.ai { background: var(--ai-bg); border: 1px solid var(--border); border-top-left-radius: 4px; color: var(--text); }
.bubble.user { background: var(--user-bg); border: 1px solid #2A3050; border-top-right-radius: 4px; color: var(--text); }

/* PII warning badge */
.pii-badge {
    display: inline-block;
    background: rgba(224,92,92,0.15);
    border: 1px solid var(--danger);
    color: var(--danger);
    border-radius: 6px;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 2px 8px;
    margin-bottom: 6px;
}

.sources-card {
    margin-top: 12px;
    background: #0F1219;
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 10px;
    padding: 12px 16px;
}
.sources-title {
    font-size: 10px;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 10px;
    font-weight: 600;
}
.source-item {
    display: flex; gap: 10px; align-items: flex-start;
    padding: 8px 0; border-bottom: 1px solid var(--border);
}
.source-item:last-child { border-bottom: none; }
.source-num {
    width: 20px; height: 20px; border-radius: 50%;
    background: var(--gold-dim); border: 1px solid var(--gold);
    color: var(--gold); font-size: 10px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
}
.source-meta { flex: 1; }
.source-file { font-size: 11px; color: var(--gold-light); font-weight: 500; margin-bottom: 2px; }
.source-page { font-size: 10px; color: var(--text-muted); margin-bottom: 5px; }
.source-snippet { font-size: 12px; color: #9A9DAA; line-height: 1.5; font-style: italic; }

.thinking { display: flex; gap: 5px; align-items: center; padding: 14px 18px; }
.dot { width: 7px; height: 7px; border-radius: 50%; background: var(--gold); opacity: 0.3; }
.dot:nth-child(1) { animation: pulse 1.2s ease-in-out 0s infinite; }
.dot:nth-child(2) { animation: pulse 1.2s ease-in-out 0.2s infinite; }
.dot:nth-child(3) { animation: pulse 1.2s ease-in-out 0.4s infinite; }
@keyframes pulse { 0%,80%,100%{opacity:0.3;transform:scale(1)} 40%{opacity:1;transform:scale(1.3)} }

.welcome { text-align: center; padding: 60px 40px; max-width: 520px; margin: 0 auto; }
.welcome-icon { font-size: 48px; margin-bottom: 20px; }
.welcome-title { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; color: var(--text); margin-bottom: 10px; }
.welcome-sub { font-size: 14px; color: var(--text-muted); line-height: 1.7; margin-bottom: 28px; }

.input-bar { padding: 16px 36px 20px; border-top: 1px solid var(--border); background: var(--surface); }
[data-testid="stChatInput"] { background: var(--surface-2) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }
[data-testid="stChatInput"] textarea { background: transparent !important; color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; font-size: 14px !important; }
[data-testid="stChatInput"]:focus-within { border-color: var(--gold) !important; box-shadow: 0 0 0 3px var(--gold-dim) !important; }

hr { border-color: var(--border) !important; margin: 12px 0 !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ─── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "user_id" not in st.session_state:
    st.session_state.user_id = "U001"
if "income" not in st.session_state:
    st.session_state.income = 50000.0


# ─── Agent Loader ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_agent():
    """Load and cache the LoanAgent (initialises once, embeds all PDFs)."""
    try:
        from LoanAgent import agent
        return agent
    except Exception as e:
        st.error(f"Agent load error: {e}")
        return None


# ─── Helper: extract RAG sources from tool messages ───────────────────────────
def extract_sources(response_messages: list) -> list:
    sources = []
    for message in response_messages:
        if message.__class__.__name__ == "ToolMessage" and getattr(message, "name", "") == "invoke_rag":
            content = message.content
            if isinstance(content, str):
                try:
                    content = ast.literal_eval(content)
                except Exception:
                    continue
            if isinstance(content, dict):
                sources = content.get("sources", [])
    return sources


# ─── Helper: invoke agent with PII masking ────────────────────────────────────
def run_agent(query: str, user_id: str, income: float):
    agent = st.session_state.agent
    if agent is None:
        return "⚠️ Agent not loaded. Check your setup.", [], False

    # Mask PII in user input before it reaches the LLM
    pii_detected = has_pii(query)
    safe_query   = mask_pii(query)

    enriched = f"{safe_query}\n\n[Context] User ID: {user_id}, Monthly Income: ₹{income:,.0f}"

    try:
        response = agent.invoke({
            "messages": [{"role": "user", "content": enriched}]
        })
        answer  = response["messages"][-1].content
        # Mask PII in LLM output before rendering
        answer  = mask_pii(answer)
        sources = extract_sources(response["messages"])
        return answer, sources, pii_detected
    except Exception as e:
        return f"❌ Error: {str(e)}", [], False


# ─── Render a single message bubble ───────────────────────────────────────────
def render_message(role: str, content: str, sources: list = None, pii_warned: bool = False):
    if role == "user":
        st.markdown(f"""
            <div class="msg-row user">
                <div class="avatar user">U</div>
                <div class="bubble user">{content}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        pii_badge = '<div class="pii-badge">🛡 PII detected &amp; masked</div>' if pii_warned else ""

        sources_html = ""
        if sources:
            items_html = ""
            for i, src in enumerate(sources, 1):
                items_html += f"""
                    <div class="source-item">
                        <div class="source-num">{i}</div>
                        <div class="source-meta">
                            <div class="source-file">📄 {src.get('source', 'N/A')}</div>
                            <div class="source-page">Page {src.get('page', 'N/A')}</div>
                            <div class="source-snippet">"{src.get('snippet', '')[:180]}..."</div>
                        </div>
                    </div>
                """
            sources_html = f"""
                <div class="sources-card">
                    <div class="sources-title">📚 Sources Referenced</div>
                    {items_html}
                </div>
            """

        st.markdown(f"""
            <div class="msg-row">
                <div class="avatar ai">L</div>
                <div style="max-width:72%">
                    {pii_badge}
                    <div class="bubble ai">{content}</div>
                    {sources_html}
                </div>
            </div>
        """, unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="brand">
            <div class="brand-title">🏦 LoanIQ</div>
            <div class="brand-sub">AI Loan Assistant</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">User Profile</div>', unsafe_allow_html=True)
    user_id = st.text_input("User ID", value=st.session_state.user_id,
                            label_visibility="collapsed", placeholder="User ID e.g. U001")
    income  = st.number_input("Monthly Income (₹)", value=st.session_state.income,
                              step=5000.0, label_visibility="collapsed", min_value=0.0)

    if st.button("Apply Profile"):
        st.session_state.user_id = user_id
        st.session_state.income  = income
        st.success("Profile updated!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Load agent once
    if st.session_state.agent is None:
        with st.spinner("Loading agent & embedding PDFs..."):
            st.session_state.agent = load_agent()
        if st.session_state.agent:
            st.success("Agent ready ✓")
        else:
            st.error("Failed to load agent")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Upload PDF at runtime ──────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label" style="padding:0 20px;margin-bottom:8px;">Upload Document</div>',
                unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_file is not None:
        from EmbedService import PDFEmbedService
        embed_svc = PDFEmbedService()
        with st.spinner(f"Indexing {uploaded_file.name}..."):
            embed_svc.save_and_embed(uploaded_file.name, uploaded_file.read())
        st.success(f"'{uploaded_file.name}' indexed!")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label" style="padding:0 20px;margin-bottom:10px;">Quick Queries</div>',
                unsafe_allow_html=True)

    quick_queries = [
        "What is my credit score?",
        "Am I eligible for a home loan?",
        "What is my risk profile?",
        "What interest rate applies to me?",
        "Give me a complete loan summary.",
        "Explain the KYC and AML requirements.",
        "What are the NPA classification rules?",
        "What is the loan origination process?",
        "Explain prepayment and foreclosure charges.",
        "What happens if I default on my EMI?",
    ]

    st.markdown('<div class="chip-grid">', unsafe_allow_html=True)
    for q in quick_queries:
        if st.button(q, key=f"chip_{q}"):
            st.session_state["pending_query"] = q
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ─── Main Chat Area ────────────────────────────────────────────────────────────
st.markdown("""
    <div class="chat-header">
        <div class="chat-header-icon">🏦</div>
        <div>
            <div class="chat-header-title">LoanIQ Assistant</div>
            <div class="chat-header-status">
                <span class="status-dot"></span> Online · Retail &amp; NBFC Loan Specialist
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# ── Welcome screen ─────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome">
            <div class="welcome-icon">🏦</div>
            <div class="welcome-title">How can I assist you today?</div>
            <div class="welcome-sub">
                I can help with loan eligibility, credit scores, risk assessments,
                interest rates, RBI/NBFC compliance, KYC &amp; AML rules, NPA classification,
                and your complete loan agreement — all in one place.
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        render_message(
            msg["role"],
            msg["content"],
            msg.get("sources"),
            msg.get("pii_warned", False),
        )


# ── Handle quick query chip ────────────────────────────────────────────────────
if "pending_query" in st.session_state:
    query = st.session_state.pop("pending_query")
    st.session_state.messages.append({"role": "user", "content": query})
    render_message("user", query)

    with st.spinner(""):
        st.markdown("""
            <div class="msg-row">
                <div class="avatar ai">L</div>
                <div class="bubble ai">
                    <div class="thinking">
                        <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        answer, sources, pii_warned = run_agent(query, st.session_state.user_id, st.session_state.income)

    st.session_state.messages.append({
        "role": "assistant", "content": answer,
        "sources": sources, "pii_warned": pii_warned,
    })
    st.rerun()


# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about your loan, eligibility, RBI compliance, or policy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    with st.spinner("Thinking..."):
        answer, sources, pii_warned = run_agent(prompt, st.session_state.user_id, st.session_state.income)

    st.session_state.messages.append({
        "role": "assistant", "content": answer,
        "sources": sources, "pii_warned": pii_warned,
    })
    render_message("assistant", answer, sources, pii_warned)