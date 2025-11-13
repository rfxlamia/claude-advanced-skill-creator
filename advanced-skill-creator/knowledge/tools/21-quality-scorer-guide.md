---
name: quality-scorer-guide
description: "Usage guide for quality_scorer.py - Score skill quality against best practices"
tool_name: "quality_scorer.py"
tool_type: "agent-layer"
read_priority: "high"
read_when:
  - "User asks 'How good is my skill?'"
  - "Quality assessment needed"
  - "Before deployment"
  - "Quality tracking required"
related_files:
  - "Files 01-13: All best practices"
  - "File 05: Token economics"
  - "File 07: Security concerns"
  - "File 10: Architecture standards"
token_estimate: "900"
last_updated: "2025-11-07"
---

# Quality Scorer Guide

## PURPOSE

Agent-layer tool untuk score skill quality menggunakan 100-point system across 5 categories. Called BY Claude via bash_tool, NOT for direct human use.

**Flow:** User asks â†’ Claude calls tool â†’ JSON output â†’ Claude explains

---

## SCORING SYSTEM (100 Points)

| Category | Points | Criteria |
|----------|--------|----------|
| **Structure** | 20 | YAML, organization, progressive disclosure, references |
| **Content** | 30 | Description (WHAT+WHEN), triggers, writing style, examples |
| **Efficiency** | 20 | Line count, token estimate, bloat detection |
| **Security** | 15 | No secrets, safe patterns, input validation |
| **Style** | 15 | Imperative voice, conciseness, clear headers |

**Grade Scale:**
- A (90-100%): Excellent - Production ready
- B (80-89%): Good - Minor improvements
- C (70-79%): Fair - Several improvements needed
- D (60-69%): Needs Improvement
- F (<60%): Poor

---

## USAGE (AGENT-LAYER)

### Standard Call

```bash
python quality_scorer.py /path/to/skill --format json
```

**Output:**
```json
{
  "status": "success",
  "skill_path": "/mnt/skills/public/docx",
  "skill_name": "docx",
  "overall": {
    "score": 86,
    "max": 100,
    "percentage": 86.0,
    "grade": "B (Good)"
  },
  "categories": {
    "structure": {"score": 20, "max": 20, "percentage": 100.0, "issues": []},
    "content": {"score": 28, "max": 30, "percentage": 93.33, "issues": [...]},
    "efficiency": {"score": 15, "max": 20, "percentage": 75.0, "issues": [...]},
    "security": {"score": 15, "max": 15, "percentage": 100.0, "issues": []},
    "style": {"score": 5, "max": 15, "percentage": 33.33, "issues": [...]}
  },
  "recommendations": [
    "Content: Writing style not agent-optimized",
    "Efficiency: Content bloat detected",
    "Style: Not using imperative voice"
  ]
}
```

---

### Error Response

```json
{
  "status": "error",
  "error_type": "FileNotFound",
  "message": "Skill directory not found: /path/to/skill",
  "help": "Ensure skill directory exists and contains SKILL.md"
}
```

**Error Types:**
- `FileNotFound`: Invalid path or missing SKILL.md
- `UnexpectedError`: Script error (permissions, malformed files)

---

## CLAUDE'S USAGE PATTERN

**Step 1:** User asks "How good is my skill?"

**Step 2:** Claude calls tool with JSON format:
```python
result = bash_tool("python quality_scorer.py /path/to/skill --format json")
```

**Step 3:** Parse JSON output:
```python
data = json.loads(result.stdout)
if data['status'] == 'success':
    # Use score and recommendations
else:
    # Handle error
```

**Step 4:** Explain to user naturally:
```
Your skill scores **86/100 (Grade B)** - Good quality with minor improvements needed.

**Strengths:**
âœ“ Perfect structure (20/20)
âœ“ Excellent security (15/15)

**Areas to Improve:**
âš  Content: Writing style could be more agent-optimized (28/30)
âš  Efficiency: Some content bloat detected (15/20)
âš  Style: Use more imperative voice (5/15)

**Recommendations:**
1. Use more action verbs (Use, Run, Execute)
2. Reduce section length (move to references/)
3. Keep sentences concise (<20 words)

See Files 05, 07, 10 for optimization guidance.
```

---

## CATEGORY DETAILS

### Structure (20 pts)
- YAML frontmatter valid (5): Has `name:` and `description:`
- File organization (5): SKILL.md exists, proper directory
- Progressive disclosure (5): <500 lines OR uses references/
- Reference files (5): Lowercase names, no spaces

### Content (30 pts)
- Description quality (10): Includes WHAT task does + WHEN to use
- Clear triggers (5): Has "use when", "trigger", "invoke" keywords
- Writing style (10): Uses code blocks, lists, tables, action verbs
- Inline examples (5): Examples in context, not separate section

### Efficiency (20 pts)
- Line count (10): <500 lines full, <800 partial
- Token estimate (5): <5,000 tokens (estimated: chars Ã· 4)
- No bloat (5): No sections >150 lines, >70% unique content

### Security (15 pts)
- No secrets (5): No hardcoded API keys, passwords, tokens
- Safe patterns (5): No `eval()`, `exec()`, `shell=True`
- Input validation (5): Has validation keywords/code

### Style (15 pts)
- Imperative voice (5): >70% sentences start with action verbs
- Concise (5): Average sentence length <20 words
- Clear headers (5): >70% headers descriptive (>2 words)

---

## EXIT CODES

| Code | Meaning | Quality |
|------|---------|---------|
| 0 | Success, score â‰¥70% | Acceptable quality |
| 1 | Success but <70%, OR error | Below threshold or invalid |
| 2 | Unexpected error | Script failure |

**CI/CD Integration:**
```yaml
- run: python quality_scorer.py ./skill --format json
  # Fails if score <70%
```

---

## HUMAN-READABLE MODE

**For developers debugging:**
```bash
# Text output with breakdown
python quality_scorer.py /path/to/skill --detailed

# Export report files
python quality_scorer.py /path/to/skill --export report.json
python quality_scorer.py /path/to/skill --export report.md
```

**Note:** Human mode is for development only. Claude always uses `--format json`.

---

## REFERENCES

**Best Practices:**
- Files 01-13: Comprehensive checklist
- File 05: Token optimization
- File 07: Security guidelines
- File 10: Architecture standards

**Related Tools:**
- `validate_skill.py`: Technical validation
- `security_scanner.py`: Detailed security audit
- `split_skill.py`: Fix efficiency via progressive disclosure
- `token_estimator.py`: Detailed token analysis

**Script:** `/mnt/project/quality_scorer.py` (831 lines)

---

**Status:** âœ… Production-ready | **Version:** 1.0 | **Integration:** Agent-layer JSON output
