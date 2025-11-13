# Section 4: Decision Workflow (Skills vs Subagents)

**Use when:** User uncertain if Skills is right approach

**Entry Point:** User asks "should I use Skills or Subagents?" or "decide approach"

### Decision Process

**Tool:** `scripts/decision_helper.py`

```bash
python scripts/decision_helper.py --format json
```

**Interactive Questions:**
1. "Describe the use case and requirements"
2. "How often will this be used?"
3. "What's the complexity level?"
4. "Do you need persistent knowledge?"
5. "What's the typical context size?"

**JSON Output Example:**
```json
{
  "recommendation": "Skills",
  "confidence": 0.85,
  "rationale": "Use case fits Skills pattern: reusable knowledge, moderate complexity, clear scope",
  "tradeoffs": {
    "skills_advantages": ["Reusable", "Token efficient", "Clear scope"],
    "skills_disadvantages": ["Limited context awareness"],
    "subagents_advantages": ["Context-aware", "Flexible"],
    "subagents_disadvantages": ["Higher token cost", "Complex orchestration"]
  },
  "next_steps": "Proceed with Skills creation"
}
```

**Decision Gates:**
```
IF recommendation = "Skills" AND confidence >=0.75:
    -> PROCEED to Section 2 (Full Creation)
    
IF recommendation = "Subagents":
    -> EXPLAIN why Subagents better
    -> STOP (out of scope for this skill)
    
IF confidence <0.75:
    -> DISCUSS tradeoffs with user
    -> CLARIFY requirements
    -> RE-RUN decision helper
```

**Knowledge Loading:**
- Load `knowledge/foundation/02-skills-vs-subagents.md`
- Load `knowledge/foundation/03-decision-tree.md`
- Present decision framework to user

---
