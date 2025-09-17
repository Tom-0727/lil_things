

def gen_search_plan_for_browser_use_claude(question: str):
    return f"""Generate a realistic browser navigation plan to answer the given question. Follow these principles:

## CRITICAL RULES:
1. **NEVER assume specific URLs** beyond main domain names (e.g., cornell.edu is ok, but not /specific/path)
2. **ALWAYS start with a Google search** unless the main website is explicitly mentioned
3. **Break complex queries into multiple searches** - don't expect all information in one place
4. **Use exploratory navigation** - click through menus and links rather than guessing paths
5. **Include verification steps** when dealing with dates, versions, or specific claims

## Plan Structure:
- Start broad, then narrow down
- When counting or ordering (e.g., "fifth section"), explicitly navigate and count
- For comparative queries (e.g., "most titles"), systematically check all options
- For date-specific information, consider:
  - The information might be in archives
  - Dates might be holidays affecting schedules
  - Multiple documents might need cross-referencing

## Output Format:
List concrete, observable actions like:
- "Search for [specific terms] on Google"
- "Click on the result from [domain]"
- "Navigate to [menu item] section"
- "Look for [specific text/pattern] on the page"
- "Count the items to find the [nth] one"
- "Open each link to check for [criteria]"
- "Verify by searching for [confirmation info]"

## Avoid:
- Assuming you know the exact location of information
- Providing specific URLs beyond the main domain
- Expecting comprehensive information in a single source
- Skipping intermediate navigation steps
- Making assumptions about ordering, dates, or classifications

Remember: Act like a real user who doesn't know the website structure and needs to explore systematically.

Here is the question: `{question}`, please generate the search plan."""



def gen_search_plan_for_browser_use_openai(question: str):
    return f"""You create robust, executable web Search Plans for a browser agent that has no memory and must succeed in a single run. Your plan must avoid hallucinated deep links and rely on authoritative entry points, time/version disambiguation, multi-hop retrieval, in-page anchors, and fallbacks.

# Constraints & Guardrails
- Do not hardcode deep URLs unless the plan first lands on an official index page that visibly links to them.
- Always resolve time/version context from the question (e.g., specific month/year, “as of” year, weekday vs weekend/holiday).
- Prefer official sources (homepages, release indices, rule indices, official PDFs) before third-party pages.
- Use multi-hop: first identify the needed ID/version/section, then open the document that contains the exact field.
- Add a fallback for each critical step (site search, site:domain Google query, alternate index/archived page).
- Define page verification signals (e.g., page title or section header contains specific text) before extracting info.
- Include at least one cross-check if time/edition/schedule might vary.
- Extraction must be minimal and format-correct (e.g., 12-hour time with AM/PM, no leading zero).
- The agent has to complete everything in a single instruction block; keep steps concise and deterministic.

# Output Format (JSON)
Produce only a compact JSON object with these fields:
```json
{{
  "objective": "<one sentence restatement>",
  "start_queries": ["<2-4 google queries, prefer site: filters>"],
  "primary_domains": ["<likely official domains>"],
  "steps": [
    {{
      "action": "open|search|click|find|scroll",
      "target": "<url or query or anchor text>",
      "expect": "<visible signals to confirm correctness>",
      "fallback": "<what to do if not found>"
    }}
    ...
  ],
  "cross_checks": ["<brief description of 1-2 checks tied to date/version/schedule>"],
  "extraction": {{
    "where": "<exact page/section to read>",
    "how": "<the field/pattern to extract>",
    "format": "<exact output formatting rules>"
  }}
}}
```

# Planning Heuristics (apply silently)
- If the task mentions a date/version → add a step to filter to that version or open “Other versions/archives”.
- If the answer depends on day type (weekday/weekend/holiday) → add a step to verify the calendar/holiday and select the correct schedule.
- For legal/rule repositories → enter from the rules index, then the article, then the rule, then the amendment notes.
- For changelogs → enter via Release/What's New index, then open the matching dated release, then Bug fixes subsection.
- No more than 10 steps.

# Now generate the plan for this question:
`{question}`
"""