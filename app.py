import streamlit as st
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image as GeminiImage
from utils import (
    read_pdfs,
    read_csv_excel,
    read_url,
    read_images,
    clean_text
)

# =========================
# VERTEX INIT (LOCKED)
# =========================
PROJECT_ID = "gemmaagent-462506"
LOCATION = "global"

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-3-pro-preview")

# =========================
# UI
# =========================
st.set_page_config("Auto Domain AI", layout="wide")
st.title("🤖 Auto-Domain Self-Configuring AI Assistant")

# =========================
# STATE
# =========================
for k in ["persona", "domain", "ready", "messages"]:
    if k not in st.session_state:
        st.session_state[k] = None if k != "messages" else []

# =========================
# SIDEBAR – SETTINGS
# =========================
with st.sidebar:
    st.header("⚙️ Settings – Data Sources")

    pdfs = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    data_file = st.file_uploader(
        "Upload CSV / Excel",
        type=["csv", "xlsx"]
    )

    images = st.file_uploader(
        "Upload Images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    url = st.text_input("Website URL")

    if st.button(" Build Domain Assistant"):
        with st.spinner("Understanding business context..."):
            context = ""

            if pdfs:
                context += read_pdfs(pdfs)

            if data_file:
                context += read_csv_excel(data_file)

            if url:
                context += read_url(url)

            if images:
                img_descriptions = []
                for img in images:
                    gem_img = GeminiImage.load_from_file(img)
                    resp = model.generate_content(
                        ["Describe this image in business context", gem_img]
                    )
                    img_descriptions.append(resp.text)
                context += "\n".join(img_descriptions)

            prompt = f"""
            From the following mixed business data:
            - documents
            - tables
            - images
            - website text

            Do the following:
            1. Identify the primary domain
            2. Identify tone and communication style
            3. Create a strict system persona for a domain-specific AI assistant

            Respond ONLY in JSON:
            {{
              "domain": "...",
              "persona": "..."
            }}

            DATA:
            {context[:12000]}
            """

            meta = model.generate_content(prompt).text

            st.session_state.domain = meta.split('"domain":')[1].split('"')[1]
            st.session_state.persona = meta.split('"persona":')[1].rsplit('"', 1)[0]
            st.session_state.ready = True

        st.success("Domain-specific assistant is ready!")

    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

# =========================
# CHAT
# =========================
# =========================
# CHAT
# =========================
st.subheader("💬 Domain-Specific Chat")

# Show chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat input ALWAYS visible
q = st.chat_input(
    "Say hi, or upload data from Settings to build a domain assistant"
)

if q:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.markdown(q)

    with st.chat_message("assistant"):
        # 🔹 BEFORE configuration → guidance mode
        if not st.session_state.ready:
            basic_reply = (
                "Hi 👋\n\n"
                "I’m an **Auto-Domain AI Assistant**.\n\n"
                "To become domain-specific, please upload PDFs / CSV / Images "
                "or a Website URL from **Settings** and click "
                "**Build Domain Assistant**.\n\n"
                "Once configured, I’ll answer as a domain expert."
            )
            st.markdown(basic_reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": basic_reply}
            )

        # 🔹 AFTER configuration → domain persona
        else:
            prompt = f"""
            SYSTEM PERSONA:
            {st.session_state.persona}

            USER QUESTION:
            {q}
            """
            ans = model.generate_content(prompt).text
            st.markdown(ans)

            st.session_state.messages.append(
                {"role": "assistant", "content": ans}
            )
