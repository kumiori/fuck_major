# app.py
import streamlit as st
from fuck_major.scraper import scrape_journal

def main():
    st.title("Journal Data Scraper")
    
    # Input field for journal URL
    journal_url = st.text_input("Enter Journal URL", "")
    
    if st.button("Fetch Journal Data"):
        if journal_url:
            try:
                # Fetching journal data
                st.write("Fetching data...")
                journal_data = scrape_journal(journal_url)
                
                # Display journal data
                if journal_data:
                    st.subheader("Journal Details:")
                    st.write(f"**Title**: {journal_data.get('title', 'N/A')}")
                    st.write(f"**Editor**: {journal_data.get('editor', 'N/A')}")
                    st.write(f"**APC (Article Processing Charge)**: {journal_data.get('apc', 'N/A')}")
                    st.write(f"**Time to First Decision**: {journal_data.get('time_to_first_decision', 'N/A')}")
                    st.write(f"**Review Time**: {journal_data.get('review_time', 'N/A')}")
                    st.write(f"**Submission to Acceptance**: {journal_data.get('submission_to_acceptance', 'N/A')}")
                    st.write(f"**Impact Factor**: {journal_data.get('impact_factor', 'N/A')}")
                    st.write(f"**CiteScore**: {journal_data.get('citescore', 'N/A')}")
                    st.write(f"**About the Journal**: {journal_data.get('about_the_journal', 'N/A')}")
                else:
                    st.error("Failed to fetch journal data.")
            except Exception as e:
                st.error(f"​⬤