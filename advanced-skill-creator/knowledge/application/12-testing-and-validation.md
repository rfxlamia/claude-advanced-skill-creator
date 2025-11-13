---
title: "Testing & Validation: Quality Assurance for Skills"
purpose: "Pre-deployment validation, testing frameworks, debugging workflows"
token_estimate: "2000"
read_priority: "high"
read_when:
  - "Before deploying any skill"
  - "User asking 'How do I test this?'"
  - "Debugging skill issues"
  - "Quality assurance planning"
  - "Creating testing checklist"
related_files:
  must_read_first:
    - "01-why-skills-exist.md"
  read_together:
    - "11-adoption-strategy.md"
  read_next:
    - "14-validation-best-practices.md"
    - "15-cost-optimization-guide.md"
    - "16-security-scanning-guide.md"
avoid_reading_when:
  - "Still learning concepts (not implementing yet)"
  - "Using only official Anthropic skills"
last_updated: "2025-11-03"
---

# Testing & Validation: Quality Assurance for Skills

## I. PENDAHULUAN

**Why Testing Critical:** Validation failures waste 2-4 hours debugging post-deployment. Pre-deployment testing catches issues early, ensures quality, prevents user frustration.

**Testing Philosophy:** Test BEFORE deployment, test WHAT matters (not everything), automate where possible, iterate based on failures.

**Scope:** Pre-deployment validation, functional testing, debugging workflows. **For automated scripts:** `14-validation-best-practices.md`. **For security:** `07-security-concerns.md`.

---

## II. PRE-DEPLOYMENT VALIDATION

### A. Structure Validation

| Check | Requirement | Status |
|-------|-------------|--------|
| **YAML** | Valid frontmatter, required fields | Ã¢ËœÂ |
| **Name** | Max 64 chars, descriptive | Ã¢ËœÂ |
| **Description** | Max 1,024 chars, has triggers | Ã¢ËœÂ |
| **Files** | SKILL.md present, proper structure | Ã¢ËœÂ |
| **Organization** | Progressive disclosure (main + refs) | Ã¢ËœÂ |

**File Organization:**
```
skill-name/
  SKILL.md           # Required, <500 lines
  reference/         # Optional, Level 3 content
  scripts/           # Optional, executables
```

**For automated validation:** `validate_skill.py` (see `14-validation-best-practices.md`).

### B. Content Quality

| Aspect | Good Example | Bad Example |
|--------|--------------|-------------|
| **Description** | "Extract PDFs. Use when..." | "PDF tool" |
| **Triggers** | "convert PDF", "extract text" | Vague wording |
| **Instructions** | "1. Run X, 2. Verify Y" | "Handle appropriately" |
| **Examples** | 2-3 inline, realistic | Too many, unrealistic |
| **Cross-Refs** | Valid file paths | Broken links |

**Description Tips:** Include task verbs ("extract", "convert"), add trigger phrases ("Use when"), be specific ("PDF to Word" NOT "documents").

### C. Token Efficiency

| Component | Target | Max | Action if Over |
|-----------|--------|-----|----------------|
| SKILL.md | 200-350 lines | 500 | Split to refs |
| Description | 50-150 chars | 1,024 | Condense |
| Token estimate | Ã‚Â±10% actual | N/A | Recalculate |

**Token Formula:** Tokens Ã¢â€°Ë† Words Ãƒâ€” 1.3 to 1.5

**Progressive Disclosure:** Core in SKILL.md (<500 lines), advanced in reference files, scripts output-only (don't load), examples inline.

**For optimization:** `15-cost-optimization-guide.md`

### D. Security Audit

| Risk | Check | Vulnerable | Fixed |
|------|-------|-----------|--------|
| **Secrets** | No hardcoded keys | `API_KEY="abc"` | `os.getenv()` |
| **Injection** | No unchecked input | `os.system(input)` | `subprocess.run()` |
| **Permissions** | Minimal tools | `allowed-tools: [*]` | Specific list |
| **Network** | Justified access | Unchecked calls | Validate URLs |

**Quick Scan:**
```bash
grep -r "API_KEY\s*=" skill-name/        # Hardcoded secrets
grep -r "os\.system" skill-name/         # Injection risk
grep -r "eval\|exec" skill-name/         # Code execution
```

**For comprehensive security:** `07-security-concerns.md` + `16-security-scanning-guide.md`

---

## III. FUNCTIONAL TESTING

### A. Positive Tests (Should Succeed)

| Type | Test Case | Expected |
|------|-----------|----------|
| **Direct** | "Use PDF skill to extract" | Activates immediately |
| **Implicit** | "Extract text from PDF" | Detects relevance, activates |
| **Multi-Skill** | "Extract PDF, analyze Excel" | Both coordinate |

**Examples:**
1. Direct: "Use data-analysis skill" Ã¢â€ â€™ Triggers, processes
2. Implicit: "Analyze sales data" Ã¢â€ â€™ Detects keywords, triggers
3. Multi-step: "Convert PDF, create charts" Ã¢â€ â€™ Both skills activate

### B. Negative Tests (Should NOT Trigger)

| Type | Test Case | Expected |
|------|-----------|----------|
| **Unrelated** | "What's the weather?" | No activation |
| **Similar Keywords** | "I like to analyze movies" | No false positive |
| **Wrong Context** | "Email analysis" (Excel skill) | Correct skill triggers |

**Examples:**
1. Unrelated: "Tell joke about data" Ã¢â€ â€™ No trigger
2. False positive: "Document this process" Ã¢â€ â€™ No doc-gen trigger (instruction, not task)
3. Edge: "Summarize PDF" Ã¢â€ â€™ Only PDF triggers, not redundant summarization

### C. Integration Tests

| Type | Focus | Validation |
|------|-------|------------|
| **Skill + Subagent** | Coordination | Both execute, no conflicts |
| **Multi-Skill** | Sequential | Correct order, data passing |
| **Tool Access** | Permissions | Allowed work, blocked fail |
| **Error Handling** | Graceful failures | Valid error messages |

**Example:** "Extract PDF, analyze Excel" Ã¢â€ â€™ Verify PDF first, Excel receives data, both complete.

### D. Performance Tests

| Metric | Target | Alert |
|--------|--------|-------|
| **Token Usage** | Ã‚Â±10% estimate | >20% variance |
| **Response Time** | <30 sec | >60 sec |
| **File Handling** | Works to limit | Crashes |
| **Error Rate** | <5% | >10% |

---

## IV. DEBUGGING WORKFLOWS

### A. Common Issues

| Issue | Solution |
|-------|----------|
| **Not Triggering** | Improve description (add trigger keywords) |
| **Wrong Skill** | Make description more specific |
| **Script Fails** | Check permissions, validate inputs |
| **Permission Error** | Add required tool to allowed-tools |
| **Slow** | Check SKILL.md size, split files |

**Decision Tree:**
```
Not working?
Ã¢â€Å“Ã¢â€â‚¬ Not activating? Ã¢â€ â€™ Fix description, test explicit mention
Ã¢â€Å“Ã¢â€â‚¬ Fails execution? Ã¢â€ â€™ Check permissions, validate code
Ã¢â€Å“Ã¢â€â‚¬ Wrong output? Ã¢â€ â€™ Review instructions, add examples
Ã¢â€â€Ã¢â€â‚¬ Slow? Ã¢â€ â€™ Optimize token usage, split files
```

### B. Diagnostic Techniques

**1. Description Analysis:**
```
Bad: "Helps with documents"
Good: "Convert Word/PDF/Excel. Use when processing documents."
```

**2. Trigger Testing:**
```
Test: "Convert PDF", "Extract text", "Process document", "Use converter"
Ã¢â€ â€™ Track which phrases trigger consistently
```

**3. Permission Check:**
```yaml
allowed-tools:
  - bash_tool        # Script execution
  - view             # Read files
  - create_file      # Output
```

### C. Iterative Improvement

**5-Step Loop:**
1. **Observe:** Document failure (screenshot, error)
2. **Hypothesize:** "Description lacks 'convert' keyword"
3. **Fix:** Add one keyword (minimal change)
4. **Re-Test:** Same case again
5. **Validate:** Test 3-5 times (confirm reliability)

**Example:**
```
Iteration 1: Not triggering Ã¢â€ â€™ Add "process" keyword Ã¢â€ â€™ Works
Iteration 2: Workflow unclear Ã¢â€ â€™ Add steps Ã¢â€ â€™ Completes
Iteration 3: Fails Word docs Ã¢â€ â€™ Add example Ã¢â€ â€™ Both formats work
```

### D. Documentation

**Test Log:**

| Date | Test | Result | Issue | Resolution |
|------|------|--------|-------|------------|
| 11-01 | PDF extract | Ã¢Å“â€¦ | None | - |
| 11-01 | Excel convert | Ã¢ÂÅ’ | Permission | Added `create_file` |
| 11-02 | Excel convert | Ã¢Å“â€¦ | None | Fixed |

**Known Issues:**
```
Issue #1: Slow with large PDFs (>50MB)
Status: Open | Workaround: Split files | Target: v1.2.0

Issue #2: False trigger "analyze"
Status: Fixed v1.1.0 | Solution: Specific description
```

---

## V. QUALITY ASSURANCE FRAMEWORK

**Testing Stages:**

| Stage | Focus | Pass Criteria |
|-------|-------|---------------|
| **Dev** | Basic functionality | All positive tests pass |
| **Staging** | Integration + edges | 90% pass, no critical issues |
| **Production** | Real usage | <5% error, satisfaction Ã¢â€°Â¥7/10 |

**Sign-Off Checklist:**

| Criteria | Required |
|----------|----------|
| Validation checks passed | Yes Ã¢ËœÂ |
| Positive tests Ã¢â€°Â¥95% | Yes Ã¢ËœÂ |
| Negative tests Ã¢â€°Â¥95% | Yes Ã¢ËœÂ |
| Security audit done | Yes Ã¢ËœÂ |
| Documentation current | Yes Ã¢ËœÂ |
| Peer review complete | Yes Ã¢ËœÂ |

**Regression Testing:** Re-run ALL tests after ANY change to SKILL.md, scripts, or references.

**Monitoring:** Usage frequency (daily), error rate (<5%), complaints (<3/week). **For setup:** `11-adoption-strategy.md` IV.D.

---

## VI. KEY TAKEAWAYS

**Testing Priorities:** Pre-deployment validation prevents disasters (structure + security). Functional testing ensures core works (positive tests) and avoids false positives (negative tests). Performance optimization follows (token usage + speed).

**Quality Gates:** Pilot requires validation + positive tests. Team expansion needs integration + negative tests. Production demands performance metrics + security audit completion.

**Debugging Strategy:** Quick fixesâ€”check description keywords, verify tool permissions, test explicit mentions. Deep fixesâ€”review SKILL.md clarity, test edge cases systematically, document failure patterns.

**Next Steps:** Automation â†’ `14-validation-best-practices.md`. Optimization â†’ `15-cost-optimization-guide.md`. Security â†’ `16-security-scanning-guide.md`. Adoption â†’ `11-adoption-strategy.md`.

---

**End of File 12**
