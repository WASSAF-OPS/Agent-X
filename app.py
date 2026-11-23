
import streamlit as st
import ollama

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AgentX AI",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------
# AGENTX SYSTEM SETTINGS
# --------------------------------

SYSTEM_PROMPT = """
You are AgentX, a helpful and intelligent AI assistant.

Your rules:
1. Always communicate in English.
2. Give clear, accurate and relevant answers.
3. Use simple and understandable language.
4. Explain difficult concepts step by step.
5. Be polite, professional and helpful.
6. Never randomly change languages.
7. If you do not know something, be honest.
8. Do not invent facts.
"""

MODEL_NAME = "qwen2.5:3b"

# --------------------------------
# SESSION INITIALIZATION
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------
# HEADER
# --------------------------------

st.title("🤖 AgentX")
st.caption("Your Personal Local AI Assistant")

st.divider()

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:
    st.title("⚙️ Settings")

    st.write("**Model:** Qwen 2.5 3B")
    st.write("**Mode:** Local AI")
    st.write("**Language:** English")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by Python, Streamlit and Ollama.")

# --------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------
# USER INPUT
# --------------------------------

user_input = st.chat_input("Ask AgentX anything...")

if user_input:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("AgentX is thinking..."):

            try:

                response = ollama.chat(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        *st.session_state.messages
                    ]
                )

                answer = response["message"]["content"]

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(
                    "AgentX encountered an error. "
                    "Please check whether Ollama is running "
                    "and the selected model is installed."
                )

                st.code(str(e))
