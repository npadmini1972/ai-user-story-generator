import streamlit as st
from anthropic import Anthropic

st.set_page_config(
    page_title="AI User Story Generator",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

try:
    client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except Exception:
    st.error("API key not found. Add ANTHROPIC_API_KEY to .streamlit/secrets.toml")
    st.stop()

def generate_user_stories(problem, persona, num_stories, edge_cases):
    edge_clause = (
        "- EDGE CASE: Given [edge condition], When [action], Then [safe/graceful outcome]"
        if edge_cases else ""
    )
    prompt = f"""You are an expert Product Owner generating sprint-ready user stories.

Business Problem:
{problem}

Primary Persona: {persona}

Generate exactly {num_stories} user stories. Use this EXACT format for each:

---
USER STORY [N]
As a {persona}, I want [specific, measurable goal], so that [clear business value].

Acceptance Criteria:
- GIVEN [precondition], WHEN [user action], THEN [expected system response]
- GIVEN [precondition], WHEN [user action], THEN [expected system response]
- GIVEN [precondition], WHEN [user action], THEN [expected system response]
{edge_clause}
---

After all stories, add:

DEFINITION OF DONE (applies to all stories):
[ ] Code reviewed and approved
[ ] All acceptance criteria verified by PO in staging
[ ] Unit tests written and passing (> 80% coverage)
[ ] No critical accessibility violations (WCAG 2.1 AA)
[ ] Documentation updated
[ ] Deployed to staging, smoke tested, and signed off

PO NOTES:
- Key assumption: [one assumption baked into these stories]
- Dependency to flag: [one dependency or blocker]
- Suggested priority order: [rank the stories 1 = highest]

Rules: Be specific and testable. Avoid vague words like fast, easy, or user-friendly."""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

st.title("📋 AI User Story Generator")
st.markdown("*Generate sprint-ready user stories and acceptance criteria from a plain-English problem description.*")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    problem = st.text_area(
        "📝 Describe the business problem or feature request",
        placeholder=(
            "Example: Our data analysts spend 3 hours daily manually exporting reports "
            "from Snowflake into Excel and emailing them to stakeholders. We need an "
            "automated reporting workflow that delivers the right report to the right "
            "person at the right time."
        ),
        height=160
    )

with col2:
    persona = st.selectbox(
        "👤 Primary Persona",
        options=[
            "End User", "Data Analyst", "System Administrator",
            "Compliance Officer", "Operations Manager", "Business Stakeholder"
        ]
    )
    num_stories = st.slider("Number of User Stories", min_value=2, max_value=6, value=3)
    edge_cases = st.checkbox("Include edge case acceptance criteria", value=True)

st.divider()

if st.button("✨ Generate User Stories", type="primary", use_container_width=True):
    if not problem.strip():
        st.warning("⚠️ Please describe the business problem first.")
    else:
        with st.spinner("Generating user stories with Claude AI..."):
            try:
                result = generate_user_stories(problem, persona, num_stories, edge_cases)
                st.success("✅ User stories generated!")
                st.markdown("### Generated Output")
                st.markdown(result)
                st.download_button(
                    label="⬇️ Download as .txt",
                    data=result,
                    file_name="user_stories.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
                st.info("Check your API key in .streamlit/secrets.toml")

st.divider()
st.caption(
    "Built by Padmini Nagarajan | AI Product Owner Portfolio | "
    "github.com/npadmini1972/ai-user-story-generator"
)