import os
import streamlit as st
from src.crew import run_crew

st.set_page_config(
    page_title="B2B Market Intelligence",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 B2B Competitive Intelligence & Market Scouting")
st.markdown(
    "Select an industry and let the AI agent crew research, synthesise, "
    "and generate a strategic intelligence report."
)

INDUSTRIES = [
    "E-Commerce",
    "FinTech",
    "EdTech",
    "SaaS",
    "HealthTech",
    "Electric Vehicles",
    "Cybersecurity",
    "Renewable Energy",
    "Retail",
    "Logistics",
]

st.divider()

industry = st.selectbox("Select an Industry", INDUSTRIES)

run_clicked = st.button("🚀 Run Market Research", type="primary")

if run_clicked:
    with st.spinner(
        f"Agents are researching the **{industry}** industry — this may take a few minutes..."
    ):
        try:
            paths = run_crew(industry)
        except Exception as e:
            st.error(f"An error occurred while running the crew: {e}")
            st.stop()

    st.success(f"Research complete for **{industry}**!")
    st.divider()

    swot_path = paths["swot"]
    brief_path = paths["brief"]

    if os.path.exists(swot_path) and os.path.exists(brief_path):
        tab1, tab2 = st.tabs(["📊 SWOT Analysis", "📋 Actionable Brief"])

        with tab1:
            with open(swot_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
            with open(swot_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download SWOT (Markdown)",
                    data=f,
                    file_name=f"swot_{industry.lower().replace(' ', '_')}.md",
                    mime="text/markdown",
                )

        with tab2:
            with open(brief_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
            with open(brief_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Brief (Markdown)",
                    data=f,
                    file_name=f"brief_{industry.lower().replace(' ', '_')}.md",
                    mime="text/markdown",
                )
    else:
        st.warning("Output files were not found. Check the terminal logs for errors.")
