import streamlit as st
import json

# Load structured constitution
@st.cache_data
def load_constitution():
    with open("constitution.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_constitution()

# Sidebar options
st.sidebar.title("📚 Malawi Constitution")
view_option = st.sidebar.radio("Choose View Mode:", ["Browse by Chapter", "Search by Keyword"])

st.title("Mzika Malawi Constitution Reader")

# Browse Mode
if view_option == "Browse by Chapter":
    chapter_titles = [ch["chapter"] for ch in data]
    selected = st.selectbox("Select a Chapter", chapter_titles)

    chapter = next((c for c in data if c["chapter"] == selected), None)
    if chapter:
        st.subheader(chapter["chapter"])
        for section in chapter["sections"]:
            with st.expander(f"{section['section']}"):
                st.write(section["content"])

# Search Mode
elif view_option == "Search by Keyword":
    query = st.text_input("Enter a keyword (e.g. land, rights, life):")
    if query:
        query = query.lower()
        found = False
        for chapter in data:
            for section in chapter["sections"]:
                if query in section["content"].lower() or query in section["section"].lower():
                    if not found:
                        st.subheader("🔍 Search Results")
                        found = True
                    st.markdown(f"**{chapter['chapter']} – {section['section']}**")
                    st.write(section["content"])
                    st.markdown("---")
        if not found:
            st.warning("No matching content found.")
