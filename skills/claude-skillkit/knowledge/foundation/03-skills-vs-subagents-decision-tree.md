---
title: "Decision Tree: Memilih Skills atau Subagents"
purpose: "Practical framework untuk decision-making Skills vs Subagents"
token_estimate: "2400"
read_priority: "critical"
read_when:
  - "User asking 'Should I use Skill or Subagent for X?'"
  - "User needs decision guidance"
  - "User describing a use case"
  - "User wants recommendation"
  - "Before starting implementation"
related_files:
  must_read_first:
    - "02-skills-vs-subagents-comparison.md"
  read_together:
    - "04-hybrid-patterns.md"
  read_next:
    - "05-token-economics.md"
avoid_reading_when:
  - "User already decided (skip to implementation)"
  - "User only needs conceptual understanding (read 02 only)"
  - "User asking about costs (skip to 05)"
last_updated: "2025-10-31"
---

# Decision Tree: Memilih Skills atau Subagents

## I. PENDAHULUAN

This file provides practical decision framework untuk memilih antara Skills dan Subagents menggunakan 8-question scoring system.

**Prerequisites:** Understand conceptual differences first (see `02-skills-vs-subagents-comparison.md`)

**How This Works:** Answer 8 questions about your use case. Each answer scores +1 (favors Skill), -1 (favors Subagent), or 0 (neutral). Calculate confidence score untuk recommendation dengan reasoning.

**Important:** This is guidance framework, not rigid rules. Consider context dan specific requirements.

---

## II. DECISION FLOWCHART

Quick visual guide untuk decision process:

```
Is it a utility/conversion/template?
â”œâ”€ YES â†’ SKILL (+1)
â””â”€ NO â†’ Continue

Does it need multiple steps of reasoning?
â”œâ”€ YES â†’ SUBAGENT (-1)
â””â”€ NO â†’ Continue

Will it be reused as building block?
â”œâ”€ YES â†’ SKILL (+1)
â””â”€ NO â†’ Continue

Does it need specialized personality?
â”œâ”€ YES â†’ SUBAGENT (-1)
â””â”€ NO â†’ Continue

Is it knowledge Claude doesn't have?
â”œâ”€ YES â†’ SKILL (+1)
â””â”€ NO â†’ Continue

Does it coordinate operations?
â”œâ”€ YES â†’ SUBAGENT (-1)
â””â”€ NO â†’ Continue

Does it need isolated context?
â”œâ”€ YES â†’ SUBAGENT (-1)
â””â”€ NO â†’ Continue

Would it clutter main chat?
â”œâ”€ YES â†’ SUBAGENT (-1)
â””â”€ NO â†’ SKILL (+1)

SCORE INTERPRETATION:
+6 to +8: Strong Skill
+3 to +5: Moderate Skill
-1 to +2: Consider Hybrid
-3 to -5: Moderate Subagent
-6 to -8: Strong Subagent
```

---

## III. 8 PERTANYAAN KUNCI

### Q1: Is It a Utility/Conversion/Template Task?

**Question:** Does the task primarily involve applying standard procedures, converting formats, atau using templates?

**Examples:**
- YES: PDF to Excel conversion, brand guidelines application
- NO: Code review dengan multiple validation stages

**Scoring:** YES â†’ +1 | NO â†’ -1 | MAYBE â†’ 0

**Why:** Skills excel untuk well-defined procedural tasks (file conversions, template applications, utility functions).

---

### Q2: Does It Need Multiple Steps of Reasoning?

**Question:** Does the task require multiple decision points, hypothesis testing, atau iterative refinement?

**Examples:**
- YES: Code review (scan â†’ analyze â†’ prioritize â†’ recommend)
- NO: Apply coding style guide, extract text from PDF

**Scoring:** YES â†’ -1 | NO â†’ +1 | MAYBE â†’ 0

**Why:** Subagents designed untuk complex workflows dengan multiple stages dan synthesis requirements.

---

### Q3: Will It Be Reused as Building Block?

**Question:** Will this capability be invoked by other workflows atau agents as a utility?

**Examples:**
- YES: Document converter used by multiple subagents
- NO: One-time analysis untuk specific project

**Scoring:** YES â†’ +1 | NO â†’ -1 | MAYBE â†’ 0

**Why:** Skills are composable building blocks. Research validates 65% subagent reduction by extracting templates to skills.

**For reusability patterns, see:** `04-hybrid-patterns.md`

---

### Q4: Does It Need Specialized Personality?

**Question:** Does the task benefit dari specialized role, tone, atau domain-specific persona?

**Examples:**
- YES: Security auditor (paranoid perspective), code reviewer (strict standards)
- NO: Format converter, template applier

**Scoring:** YES â†’ -1 | NO â†’ +1 | MAYBE â†’ 0

**Why:** Subagents can embody specialized expertise dengan pre-configured AI personalities.

---

### Q5: Is It Knowledge Claude Doesn't Have?

**Question:** Does the task require organizational procedures, proprietary methods, atau domain-specific knowledge beyond Claude's training?

**Examples:**
- YES: Company WACC methodology, organizational workflows
- NO: General code review principles, standard data analysis

**Scoring:** YES â†’ +1 | NO â†’ 0 | MAYBE â†’ +1

**Why:** Skills extend Claude's knowledge dengan organizational procedures. Rakuten validates: "Skills streamline our workflows using our procedures."

---

### Q6: Does It Coordinate Operations with Decision Points?

**Question:** Does the task involve orchestrating multiple operations dengan conditional logic dan branching paths?

**Examples:**
- YES: Multi-stage validation (if fail â†’ retry, if pass â†’ continue)
- NO: Linear transformation pipeline

**Scoring:** YES â†’ -1 | NO â†’ +1 | MAYBE â†’ 0

**Why:** Subagents excel untuk coordination requiring multiple queries dan synthesis.

---

### Q7: Does It Need Isolated Context?

**Question:** Would the task benefit dari separate context window untuk avoid pollution atau confusion?

**Examples:**
- YES: Long debugging session, extensive exploration
- NO: Quick utility function, template application

**Scoring:** YES â†’ -1 | NO â†’ +1 | MAYBE â†’ 0

**Why:** Context isolation adalah key Subagent feature preventing "context pollution" dalam main conversation.

**For token efficiency analysis, see:** `05-token-economics.md`

---

### Q8: Would It Clutter Main Chat with Intermediate Steps?

**Question:** Does the task generate substantial intermediate output yang would overwhelm main conversation?

**Examples:**
- YES: Security scan dengan 50+ findings, comprehensive code analysis
- NO: Single file conversion, template application

**Scoring:** YES â†’ -1 | NO â†’ +1 | MAYBE â†’ 0

**Why:** Subagents return clean summaries, keeping main conversation focused.

---

## IV. CONFIDENCE SCORING

### Calculation Method

Sum your scores dari 8 questions. Range: -8 (strong Subagent) to +8 (strong Skill).

### Score Interpretation Table

| Score Range | Recommendation | Characteristics | Token Cost | Complexity |
|-------------|----------------|-----------------|------------|------------|
| **+6 to +8** | STRONG SKILL | Utility functions, procedures | 30-50 tokens overhead | Low |
| **+3 to +5** | MODERATE SKILL | Mostly procedural dengan some logic | Low overhead | Low-Medium |
| **-1 to +2** | CONSIDER HYBRID | Mix of utility + orchestration | Optimized | Medium |
| **-3 to -5** | MODERATE SUBAGENT | Multi-step dengan some structure | 15x multiplier | Medium-High |
| **-6 to -8** | STRONG SUBAGENT | Complex workflows, expertise needed | High (justified) | High |

### Confidence Modifiers

**Increase Confidence in Skill IF:**
- Task repeats frequently (token efficiency matters)
- Multiple teams will use it (reusability critical)
- Procedural knowledge well-documented
- No iteration or exploration needed

**Increase Confidence in Subagent IF:**
- Task high-value and infrequent (cost justified)
- Requires domain expertise personality
- Involves exploration and discovery
- Benefits dari isolated context

**Consider Hybrid IF:**
- Score near neutral (-1 to +2)
- Task has both utility and orchestration components
- Want to optimize token efficiency while maintaining capability

---

## V. REAL-WORLD SCENARIOS

### Scenario 1: Brand Guidelines Enforcement

**Description:** Apply company logo, colors, fonts, tone to documents.

**Scoring Analysis:**
Q1-Q8: +1, +1, +1, +1, +1, +1, +1, +1 = **+8**

**Recommendation:** STRONG SKILL

**Reasoning:** Pure utility function dengan organizational knowledge. Research validates: "Skills menerapkan brand style guidelines secara otomatis."

---

### Scenario 2: Comprehensive Security Audit

**Description:** Scan codebase untuk vulnerabilities, analyze severity, prioritize fixes, generate report.

**Scoring Analysis:**
Q1-Q8: -1, -1, 0, -1, 0, -1, -1, -1 = **-6**

**Recommendation:** STRONG SUBAGENT

**Reasoning:** Multi-step workflow dengan specialized expertise. Research validates: "Subagents excel untuk security audits dengan comprehensive checks."

---

### Scenario 3: Code Review Process

**Description:** Review code untuk bugs, style violations, security issues, performance problems.

**Scoring Analysis:**
Q1-Q8: 0, -1, 0, -1, +1, -1, -1, -1 = **-4**

**Recommendation:** MODERATE SUBAGENT + Skills (HYBRID)

**Reasoning:** Complex workflow but uses company standards. HYBRID PATTERN: Subagent handles review process, invokes coding-standards Skill for rules.

**For implementation, see:** `04-hybrid-patterns.md`

---

## VI. QUICK REFERENCE

### Decision Cheat Sheet

**Use SKILL if:**
- Utility/conversion/template task
- Single or linear workflow
- Will be reused as building block
- Organizational knowledge needed
- Doesn't need personality
- Won't clutter conversation

**Use SUBAGENT if:**
- Multi-step reasoning required
- Needs specialized personality
- Coordinates multiple operations
- Benefits from isolated context
- Would generate substantial output

**Use HYBRID if:**
- Has orchestration components (Subagent)
- Uses reusable utilities (Skills)

### Simple Rules

**Start with Skill unless:**
- You need multiple reasoning steps
- You need specialized expertise personality
- You need isolated context window
- Intermediate steps would clutter main chat

Skills simpler, faster, easier to maintain. Upgrade ke Subagent when complexity demands it.

### Token Cost Quick Reference

**Skills:** 30-50 tokens overhead (very efficient)  
**Subagents:** 15x token multiplier (justified for complexity)  
**Hybrid:** Optimizes both (Subagent orchestrates, Skills reduce duplication)

**For detailed cost analysis, see:** `05-token-economics.md`

---

## WHEN TO READ NEXT

**For Implementation:**
- Decided Hybrid? â†’ `04-hybrid-patterns.md`
- Need cost details? â†’ `05-token-economics.md`
- Ready to build? â†’ Implementation guides

**For Context:**
- Need conceptual review? â†’ `02-skills-vs-subagents-comparison.md`
- Want strategic context? â†’ `01-why-skills-exist.md`
- See detailed validation? â†’ `case-studies.md`

**For Constraints:**
- Platform limitations? â†’ `06-platform-constraints.md`
- Security concerns? â†’ `07-security-concerns.md`

---

**FILE END - Estimated Token Count: ~2,400 tokens (~326 lines)**
