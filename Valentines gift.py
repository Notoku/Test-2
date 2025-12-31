import streamlit as st
from groq import Groq
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="For Tepy 💖",
    page_icon="💖",
    layout="centered"
)

# ---------------- API CLIENT ----------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- PERSONAL PROFILE ----------------
GIRL_PROFILE = """
Name: Tepy
Relationship: Girlfriend
Personality: sweet, caring, playful, thoughtful
Tone: warm, affectionate, gentle, slightly playful
Purpose: Make her feel loved, safe, and appreciated

Rules:
- Speak directly to Tepy
- Never break character
- Be emotionally supportive
- Keep replies short, warm, and natural
"""

SYSTEM_PROMPT = f"""
You are a personalized AI created as a Valentine's gift.
You are talking directly to Tepy.

{GIRL_PROFILE}

Stay loving and genuine.
"""

# ---------------- CACHE UI (VERY IMPORTANT) ----------------


@st.cache_data
def load_valentine_ui():
    return """
    <style>
    body {
        background: linear-gradient(135deg, #ffafbd, #ffc3a0);
        overflow: hidden;
    }

    .heart {
        position: fixed;
        width: 16px;
        height: 16px;
        background: pink;
        transform: rotate(45deg);
        animation: float 12s infinite;
        opacity: 0.6;
    }

    .heart:before,
    .heart:after {
        content: "";
        width: 16px;
        height: 16px;
        background: pink;
        border-radius: 50%;
        position: absolute;
    }

    .heart:before { top: -8px; left: 0; }
    .heart:after { left: -8px; top: 0; }

    @keyframes float {
        0% { bottom: -10%; opacity: 0; }
        50% { opacity: 0.7; }
        100% { bottom: 110%; opacity: 0; }
    }
    </style>

    <div class="heart" style="left:10%; animation-delay:0s;"></div>
    <div class="heart" style="left:30%; animation-delay:3s;"></div>
    <div class="heart" style="left:50%; animation-delay:6s;"></div>
    <div class="heart" style="left:70%; animation-delay:2s;"></div>
    <div class="heart" style="left:90%; animation-delay:4s;"></div>
    """


st.markdown(load_valentine_ui(), unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;'>💖 For You, Tepy 💖</h1>",
    unsafe_allow_html=True
)
st.caption("A little AI made just for you")

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Type something 💕")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # ⚠️ LIMIT HISTORY (THIS IS THE BIG PERFORMANCE FIX)
    context = st.session_state.messages[-6:]  # last 6 messages only

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # MUCH faster
            messages=context,
            temperature=0.7,
        )

        ai_reply = response.choices[0].message.content
        st.markdown(ai_reply)

    # Save reply
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )
