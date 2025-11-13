---
title: "Decision Helper Tool: Skills vs Subagents"
purpose: "Guide for using decision_helper.py to get instant recommendations"
tool_name: "decision_helper.py"
tool_type: "agent-layer"
read_priority: "high"
read_when:
  - "User asks 'Should I use Skill or Subagent for X?'"
  - "Decision guidance needed"
  - "Token efficiency comparison required"
  - "Before implementing new capability"
related_files:
  - "File 02: Skills vs Subagents comparison"
  - "File 03: Decision tree logic"
  - "File 05: Token economics"
token_estimate: "800"
last_updated: "2025-11-06"
---

# Decision Helper Tool: Skills vs Subagents

## PURPOSE

Agent-layer tool untuk instant Skills vs Subagents recommendations menggunakan File 03 decision tree. Called BY Claude via bash_tool, NOT for direct human use.

**Flow:** User asks â†’ Claude calls tool â†’ JSON output â†’ Claude explains

---

## THREE MODES

### Mode 1: Pre-Answered (Preferred)

**When:** Claude has extracted clear answers from conversation.

**Input (answers.json):**
```json
{
  "utility_task": false, "multi_step": true, "reusable": false,
  "specialized_personality": true, "missing_knowledge": false,
  "coordination": true, "isolated_context": true, "clutter_chat": true
}
```

**Call:** `python decision_helper.py --answers /tmp/answers.json`

**Accuracy:** Highest (90-95% confidence).

---

### Mode 2: Keyword Inference (Fallback)

**When:** User query ambiguous, inference needed.

**Call (JSON output - default):**
```bash
python decision_helper.py --analyze "code review with validation"
```

**Call (Text output - for debugging):** *[New in v1.0.1]*
```bash
python decision_helper.py --analyze "code review with validation" --format text
```

**Accuracy:** Lower (confidence reduced 15%).

**Note:** Prefer Mode 1 when possible. JSON is default for agent-layer use.

---

### Mode 3: Show Criteria (Reference)

**When:** User asks "How do you decide?"

**Call (JSON output - default):**
```bash
python decision_helper.py --show-criteria
```

**Call (Text output):** *[New in v1.0.1]*
```bash
python decision_helper.py --show-criteria --format text
```

**Output:** All 8 questions + score interpretation table.

---

## OUTPUT STRUCTURE

**Success:**
```json
{
  "status": "success",
  "recommendation": "Strong Subagent",
  "score": -6,
  "confidence": 0.92,
  "reasoning": ["Multi-step process...", "Specialized personality..."],
  "token_analysis": {
    "skill_approach_tokens": 500,
    "subagent_approach_tokens": 7500,
    "cost_multiplier": 15.0
  },
  "pattern_suggestions": ["Implement as Subagent", ...],
  "references": {"conceptual": "File 02", ...}
}
```

**Error:**
```json
{
  "status": "error",
  "error_type": "InvalidInput|FileNotFound|InvalidJSON",
  "message": "...",
  "help": "..."
}
```

**Exit Codes:** 0 = success, 1 = error.

---

## CLAUDE'S USAGE PATTERN

**Step 1:** User asks â†’ Claude analyzes question

**Step 2:** Claude prepares answers.json with 8 boolean values

**Step 3:** Call tool via bash_tool

**Step 4:** Parse JSON output (`json.loads(result.stdout)`)

**Step 5:** Check `status` field:
- `"success"` â†’ Use recommendation, explain reasoning to user
- `"error"` â†’ Handle error (retry or ask clarification)

**Example Explanation:**
```
Based on analysis, I recommend **Subagent** (92% confidence).

Reasons:
â€¢ Multi-step process needed
â€¢ Specialized personality beneficial
â€¢ Isolated context prevents clutter

Token cost: ~7,500 tokens (15Ã— multiplier, justified for complexity)

See File 03 for decision tree details.
```

---

## ERROR HANDLING

| Error Type | Fix |
|------------|-----|
| `InvalidInput` | Provide all 8 answers |
| `FileNotFound` | Check path or use --analyze |
| `InvalidJSON` | Validate JSON syntax |
| `InvalidType` | Use boolean values (true/false) |

**Recovery:** If error, Claude asks clarification OR retries with Mode 2.

---

## REFERENCES

- **File 02:** Skills vs Subagents comparison
- **File 03:** 8-question decision tree
- **File 05:** Token economics

**Tool:** `/mnt/user-data/outputs/decision_helper.py` (607 lines, stdlib only)

---

**Status:** Ã¢Å“â€¦ Production-ready | **Version:** 1.0 | **Integration:** Ready for advanced-skill-creator
