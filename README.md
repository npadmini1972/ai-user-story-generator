# AI User Story Generator
**A Product Owner tool powered by Claude AI**

> Live demo: [https://ai-user-story-generator-t3jexxd7cuiftfc8vkah7i.streamlit.app/](https://ai-user-story-generator-t3jexxd7cuiftfc8vkah7i.streamlit.app/)

## Problem Statement
Product Owners and Business Analysts spend significant time manually translating 
vague business requests into structured, testable user stories. This tool uses 
Claude AI to generate a first-draft backlog item — user stories, Given/When/Then 
acceptance criteria, and a Definition of Done — in under 15 seconds.

## What It Does
- Accepts a plain-English business problem description
- Lets you select a persona (End User, Data Analyst, Admin, etc.)
- Generates 2–6 structured user stories with acceptance criteria
- Optionally includes edge case test scenarios
- Outputs a downloadable .txt file

## Product Decisions I Made (Why This Is a PO Project)
| Decision | What I chose | Why |
|----------|-------------|-----|
| Output format | Given/When/Then | Enforces testable criteria; aligns with BDD |
| Model | claude-opus-4-5 | Best instruction-following for structured output |
| No login/accounts | Stateless tool | Reduces friction; portfolio demo doesn't need state |
| No Jira export (v1) | Plain text download | 80% of value at 10% of the complexity |

## Acceptance Criteria (Written Before Coding)
- [ ] Given a problem is entered, When Generate is clicked, Then stories appear in < 15s
- [ ] Given a persona is selected, Then all stories reference that persona
- [ ] Given empty input, When Generate is clicked, Then a warning shows (no API call)
- [ ] Given output exists, Then user can download as .txt

## Tech Stack
- **UI:** Streamlit (Python)
- **AI:** Anthropic Claude API
- **Deployment:** Streamlit Community Cloud

## Run Locally
```bash
pip install streamlit anthropic
# Add ANTHROPIC_API_KEY to .streamlit/secrets.toml
streamlit run app.py
```

## About
Built by [Padmini Nagarajan](https://www.linkedin.com/in/padmini-nagarajan/), 
Product Owner with 10+ years in data analytics and digital workflow transformation. 
This project is part of my AI Product Owner portfolio.