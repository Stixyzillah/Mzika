import streamlit as st
import json

# Load constitution data
with open('constitution.json') as f:
    constitution = json.load(f)

st.title("Malawi Constitution Reader 🇲🇼📖")
query = st.text_input("Search for a right, law, or topic:")

if query:
    for chapter in constitution:
        for section in chapter['sections']:
            if query.lower() in section['title'].lower() or query.lower() in section['text'].lower():
                st.subheader(f"{chapter['chapter']} - {section['number']} {section['title']}")
                st.write(section['text'])
else:
    st.write("Browse by Chapter:")
    for chapter in constitution:
        with st.expander(chapter['chapter'] + " - " + chapter['title']):
            for section in chapter['sections']:
                st.markdown(f"**{section['number']} {section['title']}**")
                st.write(section['text'][:200] + "...")  # short preview
                if st.button("Read more", key=section['number']):
                    st.write(section['text'])   