"""
app.py
------
A simple Streamlit GUI on top of the same generate_copy() function
used by the CLI. Run with: streamlit run app.py
"""

import streamlit as st
from generator import generate_copy

st.set_page_config(page_title="AI Copywriter", page_icon="✍️")

st.title("✍️ Automated Copywriting & Tone Transformer")
st.caption("Runs entirely locally via Ollama — no API key, no cost.")

with st.form("copy_form"):
    product_name = st.text_input("Product name / description", placeholder="e.g. Wireless Noise-Cancelling Headphones")

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", ["instagram", "linkedin", "twitter", "email"])
    with col2:
        tone = st.text_input("Tone", placeholder="e.g. witty, professional, urgent")

    col3, col4 = st.columns(2)
    with col3:
        temperature = st.slider("Temperature (creativity)", 0.0, 1.5, 0.7, 0.1)
    with col4:
        top_p = st.slider("Top P (word diversity)", 0.0, 1.0, 0.9, 0.05)

    submitted = st.form_submit_button("Generate Copy")

if submitted:
    if not product_name or not tone:
        st.error("Please fill in both the product name and tone.")
    else:
        with st.spinner("Generating with your local model..."):
            result = generate_copy(
                product_name=product_name,
                platform=platform,
                tone=tone,
                temperature=temperature,
                top_p=top_p,
            )

        st.subheader("Generated Copy")
        st.write(result.generated_copy)

        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Character count", result.char_count)
        c2.metric("Within platform limit", "✅ Yes" if result.within_limit else "❌ No")
