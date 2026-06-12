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

# ── Persona-aware prompt instructions ──────────────────────────────────────
PERSONA_CONTEXT = {
    "Product Owner": (
        "The Product Owner defines acceptance criteria, prioritizes backlog items, "
        "and ensures stories deliver measurable business value. Stories should reflect "
        "backlog health, roadmap alignment, and PO sign-off requirements."
    ),
    "Scrum Master": (
        "The Scrum Master facilitates Agile ceremonies, removes blockers, and ensures "
        "the team follows Scrum/SAFe processes. Stories should focus on process "
        "improvements, ceremony effectiveness, and team delivery metrics."
    ),
    "End User": "The End User interacts directly with the product to accomplish day-to-day tasks.",
    "Data Analyst": "The Data Analyst works with data pipelines, reports, and dashboards to derive business insights.",
    "System Administrator": "The System Administrator manages configurations, access, and system health.",
    "Compliance Officer": "The Compliance Officer ensures regulatory and audit requirements are met.",
    "Operations Manager": "The Operations Manager oversees operational workflows and team performance.",
    "Business Stakeholder": "The Business Stakeholder sponsors the initiative and tracks ROI and business outcomes.",
    "Contract Specialist": "The Contract Specialist manages lease contracts, asset records, and billing workflows in InfoLease.",
    "Portfolio Manager": "The Portfolio Manager monitors the lease portfolio performance, residuals, and financial reporting.",
}

# ── InfoLease modules and phases ───────────────────────────────────────────
INFOLEASE_MODULES = [
    "Asset Management",
    "Billing & Invoicing",
    "Contract Management",
    "Financial Reporting / GL Integration",
    "Infotrieve / Query Reporting",
    "End-of-Lease / Residual Management",
    "Data Migration & Validation",
    "API Integration / System Connectivity",
    "User Access & Security",
]

UPGRADE_PHASES = [
    "Phase 1 — Discovery",
    "Phase 2 — Evaluate Options",
    "Phase 3 — Design",
    "Phase 4 — Deliver & Deploy",
    "Phase 5 — Post-Production Stabilization",
    "Phase 6 — Knowledge Transfer & Handover",
]

# ── Core generation function ───────────────────────────────────────────────
def generate_user_stories(problem, persona, num_stories, edge_cases, infolease_context=None):
    edge_clause = (
        "- EDGE CASE: Given [edge condition], When [action], Then [safe/graceful outcome]"
        if edge_cases else ""
    )

    persona_instruction = PERSONA_CONTEXT.get(persona, "")

    infolease_block = ""
    if infolease_context:
        infolease_block = f"""
InfoLease Engagement Context:
- Module in scope: {infolease_context['module']}
- Upgrade Phase: {infolease_context['phase']}
- Client: Synovus Bank | Vendor: Solifi (formerly IDS) | Delivery: Infosys

Tailor the user stories to reflect InfoLease platform terminology, lease lifecycle 
workflows, and the three-party engagement model (Infosys SME/PO bridging Synovus 
and Solifi). Use realistic InfoLease field names, module behaviors, and upgrade 
activities where applicable.
"""

    prompt = f"""You are an expert Product Owner generating sprint-ready user stories.

Business Problem:
{problem}

Primary Persona: {persona}
Persona Context: {persona_instruction}
{infolease_block}
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


# ── UI ─────────────────────────────────────────────────────────────────────
st.title("📋 AI User Story Generator")
st.markdown("*Generate sprint-ready user stories and acceptance criteria from a plain-English problem description.*")
st.divider()

# InfoLease context toggle
infolease_mode = st.toggle(
    "🏦 InfoLease Engagement Mode (Synovus / Solifi upgrade context)",
    value=False,
    help="Enable this to generate user stories tailored to an InfoLease platform upgrade engagement."
)

infolease_context = None
if infolease_mode:
    st.info(
        "**InfoLease Mode ON** — Stories will be tailored to the InfoLease upgrade "
        "engagement context (Synovus Bank ↔ Infosys SME/PO ↔ Solifi).",
        icon="🏦"
    )
    il_col1, il_col2 = st.columns(2)
    with il_col1:
        il_module = st.selectbox("InfoLease Module in Scope", options=INFOLEASE_MODULES)
    with il_col2:
        il_phase = st.selectbox("Upgrade Phase", options=UPGRADE_PHASES)
    infolease_context = {"module": il_module, "phase": il_phase}
    st.divider()

# Main inputs
col1, col2 = st.columns([2, 1])

with col1:
    # Dynamic placeholder based on mode
    if infolease_mode:
        placeholder = (
            "Example: During the InfoLease 9 to 10 upgrade, Contract Specialists at "
            "Synovus cannot view migrated asset records in the new Asset Management "
            "module. They need a validated asset register that confirms all active "
            "lease assets were accurately migrated with no data loss."
        )
    else:
        placeholder = (
            "Example: Our data analysts spend 3 hours daily manually exporting reports "
            "from Snowflake into Excel and emailing them to stakeholders. We need an "
            "automated reporting workflow that delivers the right report to the right "
            "person at the right time."
        )

    problem = st.text_area(
        "📝 Describe the business problem or feature request",
        placeholder=placeholder,
        height=160
    )

with col2:
    # Updated persona list with PO, SM, and InfoLease-specific roles
    persona_options = [
        "Product Owner",
        "Scrum Master",
        "End User",
        "Data Analyst",
        "System Administrator",
        "Compliance Officer",
        "Operations Manager",
        "Business Stakeholder",
    ]

    # Add InfoLease-specific personas when in InfoLease mode
    if infolease_mode:
        persona_options += ["Contract Specialist", "Portfolio Manager"]

    persona = st.selectbox("👤 Primary Persona", options=persona_options)

    # Show persona context hint
    if persona in PERSONA_CONTEXT:
        st.caption(f"*{PERSONA_CONTEXT[persona]}*")

    num_stories = st.slider("Number of User Stories", min_value=2, max_value=6, value=3)
    edge_cases = st.checkbox("Include edge case acceptance criteria", value=True)

st.divider()

if st.button("✨ Generate User Stories", type="primary", use_container_width=True):
    if not problem.strip():
        st.warning("⚠️ Please describe the business problem first.")
    else:
        spinner_msg = (
            "Generating InfoLease-context user stories with Claude AI..."
            if infolease_mode
            else "Generating user stories with Claude AI..."
        )
        with st.spinner(spinner_msg):
            try:
                result = generate_user_stories(
                    problem, persona, num_stories, edge_cases, infolease_context
                )
                st.success("✅ User stories generated!")

                # Show context badge if InfoLease mode
                if infolease_mode:
                    st.markdown(
                        f"**Context:** `{il_module}` · `{il_phase}` · Persona: `{persona}`"
                    )

                st.markdown("### Generated Output")
                st.markdown(result)

                # Download filename reflects context
                filename = (
                    f"user_stories_{il_module.replace(' ', '_').replace('/', '')}_{il_phase[:7].replace(' ', '')}.txt"
                    if infolease_mode
                    else "user_stories.txt"
                )
                st.download_button(
                    label="⬇️ Download as .txt",
                    data=result,
                    file_name=filename,
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
