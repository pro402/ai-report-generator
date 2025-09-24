import streamlit as st
import re
from models import Report
from workflow import graph

def main():
    st.title("AI Report Generator")
    st.write("Generate a detailed report based on your input parameters below.")
    topic = st.text_input("Topic", "Latest advancements and News on AI 2025")
    report_type = st.selectbox("Report Type", ["Report", "News Letter", "Blog"])
    outline = st.text_area("Outline", "include sections that contain a table when needed and ensure that the links are valid for references.")

    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            state: Report = {
                "topic": topic,
                "report_type": report_type,
                "outline": outline,
                "report_structure": None,
                "final_report": None,
                "queries": [],
                "deep_research": [],
                "messages": []
            }
            try:
                response = graph.invoke(state, debug=True)
            except Exception as e:
                st.error(f"Workflow error: {e}")
                return

            with st.expander("Show workflow/graph output state"):
                st.write(response)
            report_content_raw = response.get("final_report")
            if not report_content_raw or not isinstance(report_content_raw, str) or len(report_content_raw.strip()) == 0:
                st.warning("No report was generated. Please check your workflow or try again.")
                return

            pattern = re.compile(r'<report>(.*?)</report>', re.DOTALL)
            matches = pattern.findall(report_content_raw)
            report_md = ''.join(matches) if matches else report_content_raw
            if not report_md.strip().endswith("</report>"):
                report_md = report_md.rstrip() + "\n</report>"
            st.markdown("# Report")
            st.markdown(report_md)
            st.download_button(
                label="Download Report as Markdown",
                data=report_md,
                file_name="report.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()
