import streamlit as st
import re
from models import Report
from workflow import graph

def main():
    st.title("AI Report Generator")

    # User input fields
    st.write("Generate a detailed report based on your input parameters below.")
    topic = st.text_input("Topic", "Latest advancements and News on AI 2025")
    report_type = st.selectbox("Report Type", ["Report", "News Letter", "Blog"])
    outline = st.text_area("Outline", "include sections that contain a table when needed and ensure that the links are valid for references.")

    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            # Create the initial state for the workflow
            state: Report = {
                "topic": topic,
                "report_type": report_type,
                "outline": outline,
                "report_structure": None,
                "final_report": None,
                "queries": [],
                "deep_research": []
            }
            # Run the workflow to generate the report
            response = graph.invoke(state, debug=True)
            report_content_raw = response["final_report"]
            # Extract the report enclosed within <report> and </report>
            pattern = re.compile(r'<report>(.*?)</report>', re.DOTALL)
            matches = pattern.findall(report_content_raw)
            report_md = ''.join(matches)
            # Display the generated report in Markdown format
            st.markdown("# Report")
            st.markdown(report_md)
            # Provide a download button for the Markdown file
            st.download_button(
                label="Download Report as Markdown",
                data=report_md,
                file_name="report.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()
