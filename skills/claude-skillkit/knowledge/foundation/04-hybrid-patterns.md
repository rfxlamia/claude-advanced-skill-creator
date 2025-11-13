---
title: "Hybrid Patterns: Combining Skills + Subagents"
purpose: "Best practices untuk menggunakan Skills dan Subagents bersama"
token_estimate: "2000"
read_priority: "high"
read_when:
  - "User wants to combine Skills + Subagents"
  - "Decision tree suggests hybrid"
  - "User has complex workflow"
  - "Optimizing existing multi-agent setup"
  - "After understanding basics of both"
related_files:
  must_read_first:
    - "02-skills-vs-subagents-comparison.md"
  read_together:
    - "05-token-economics.md"
  read_next:
    - "case-studies.md"
avoid_reading_when:
  - "User using pure Skills approach"
  - "User using pure Subagents approach"
  - "User just starting (too advanced)"
  - "Simple use case doesn't need hybrid"
last_updated: "2025-10-31"
---

# Hybrid Patterns: Combining Skills + Subagents

## I. PENDAHULUAN

Skills dan Subagents designed to work together. Highly complementary.

**Core Principle:**
- Subagents: Orchestration, complex reasoning
- Skills: Utilities, knowledge, templates
- Together: Optimize capability AND efficiency

**Research Validation:**
- 65% subagent complexity reduction (803â†’281 lines)
- 90.2% performance improvement (Opus 4 + Sonnet 4 subagents)
- Zero functionality lost

**When Hybrid Appropriate:**
Decision tree score -1 to +1 indicates hybrid. Task has both orchestration AND utility components.

**Prerequisites:** Understand Skills vs Subagents differences first.

**For conceptual foundation, see:** `02-skills-vs-subagents-comparison.md`

---

## II. PATTERN 1: SUBAGENT ORCHESTRATION + UTILITIES

### Pattern Description

**Core Concept:** Subagent orchestrates workflow, invokes Skills for utility functions.

**Architecture:**
```
Main Conversation
    |
Spawns Subagent (orchestrates complex workflow)
    |
    +-- Invokes Skill 1 (utility function)
    +-- Invokes Skill 2 (utility function)
    +-- Invokes Skill 3 (utility function)
    |
Subagent synthesizes results
    |
Returns to Main Conversation
```

**Key Characteristics:**
- Clear separation: orchestration vs utilities
- Skills reusable across multiple subagents
- Efficient token usage (Skills loaded on-demand)
- Clean workflow coordination

### Implementation Example: Document Processing Pipeline

**Scenario:** Process multiple PDFs with validation.

**Setup:**
- Subagent: document-processor (orchestrates)
- Skill 1: pdf-converter (extracts text)
- Skill 2: data-validator (checks format)
- Skill 3: reporting-template (generates output)

**Workflow:**
```
User: "Process these 10 PDFs and validate data"

document-processor subagent:
  FOR EACH pdf IN documents:
    text = invoke pdf-converter skill
    validation = invoke data-validator skill
    IF valid:
      aggregated_results.add(text, validation)
  
  report = invoke reporting-template skill
  RETURN summary to main
```

**Benefits:**
- Subagent handles iteration logic
- Skills provide deterministic operations
- Skills reusable by other workflows
- Token efficient (Skills shared, not duplicated)

### Implementation Checklist

- [ ] Define subagent orchestration role
- [ ] Identify reusable utilities â†’ create Skills
- [ ] Subagent system prompt references Skills
- [ ] Test workflow end-to-end
- [ ] Verify Skills invoked correctly

---

## III. PATTERN 2: MULTI-SUBAGENT + SHARED SKILLS

### Pattern Description

**Core Concept:** Multiple subagents share common Skills library. Extract duplicated knowledge to Skills.

**Architecture:**
```
Before:
Subagent A (800 lines: logic + templates + knowledge)
Subagent B (750 lines: logic + DUPLICATE templates)
Subagent C (700 lines: logic + DUPLICATE knowledge)

After:
Subagent A (250 lines: logic only)
Subagent B (230 lines: logic only)
Subagent C (220 lines: logic only)
    |
All invoke shared Skills:
    +-- templates-skill (300 lines)
    +-- standards-skill (200 lines)
    +-- utilities-skill (150 lines)
```

**Real Validation:** Subagent reduced 803â†’281 lines (65%) by extracting templates to Skills. Zero functionality lost.

**Key Benefit:** Update template once, all subagents benefit. DRY principle.

### Implementation Example: Multi-Domain Content Pipeline

**Scenario:** Blog, social media, email writers share brand guidelines.

**Before Optimization:**
- blog-writer: 700 lines (logic + brand + templates)
- social-writer: 650 lines (logic + brand DUPLICATE + templates)
- email-writer: 680 lines (logic + brand DUPLICATE + templates)
- Total: 2,030 lines with extensive duplication

**After Optimization:**
- blog-writer: 220 lines (logic + blog-specific templates)
- social-writer: 190 lines (logic + social-specific templates)
- email-writer: 200 lines (logic + email-specific templates)
- brand-guidelines skill: 250 lines (shared)
- content-utilities skill: 150 lines (shared)
- Total: 610 + 400 = 1,010 lines
- Reduction: 50% fewer lines, zero functionality lost

**Token Savings:**
- Brand guidelines loaded once (250 lines)
- Shared across 3 subagents
- Instead of 250 Ã— 3 = 750 lines loaded separately
- Savings: 500 lines per workflow = 67% reduction for shared content

**For detailed token analysis, see:** `05-token-economics.md`

### Implementation Checklist

- [ ] Audit subagent prompts for duplicated content
- [ ] Extract common templates â†’ Skills
- [ ] Extract shared knowledge â†’ Skills
- [ ] Update subagent prompts to reference Skills
- [ ] Test all subagents with new Skills
- [ ] Measure token reduction

---

## IV. PATTERN 3: CONDITIONAL INVOCATION

### Pattern Description

**Core Concept:** Runtime decision - invoke Skill OR spawn Subagent based on task complexity evaluation.

**Decision Logic:**
```
Task Received
    |
Evaluate Complexity
    |
    +-- Simple/Straightforward?
    |       |
    |       +-- Invoke Skill (fast, efficient)
    |       +-- Cost: 800-2,000 tokens
    |
    +-- Complex/Multi-Step?
            |
            +-- Spawn Subagent (capable, thorough)
            +-- Cost: 7,000-15,000 tokens (justified)
```

**Key Characteristics:**
- Dynamic evaluation at runtime
- Cost optimization through intelligent routing
- Maintains capability when complexity demands it
- Transparent decision logic

### Implementation Example: Data Analysis Router

**User Query:** "Analyze this dataset"

**Decision Logic Implementation:**
```
Evaluate Dataset:
  rows = dataset.row_count
  metrics = required_analysis
  
Decision:
  IF rows < 1,000 AND metrics == "basic":
    â†’ Invoke data-analysis Skill
    â†’ Quick summary statistics
    â†’ Time: 5 minutes
    â†’ Cost: 850 tokens
    
  ELIF rows > 1,000 OR metrics == "complex":
    â†’ Spawn data-scientist Subagent
    â†’ Comprehensive analysis with ML
    â†’ Time: 20 minutes
    â†’ Cost: 7,000 tokens (justified)
```

**Execution Path 1 (Simple - Skill):**
- Dataset: 500 rows, basic statistics requested
- Action: data-analysis Skill invoked
- Process: Mean, median, std dev, visualizations
- Output: Summary statistics report
- Cost: 850 tokens ($0.0026)

**Execution Path 2 (Complex - Subagent):**
- Dataset: 50,000 rows, ML predictions needed
- Action: data-scientist Subagent spawned
- Process: Feature analysis, correlation matrix, model training, predictions
- Output: Comprehensive analysis with ML insights
- Cost: 7,000 tokens ($0.021, justified for ML work)

**Decision Factors:**
- Data volume (rows, columns, size)
- Analysis complexity (descriptive vs predictive)
- Time constraints (urgent vs thorough)
- Output requirements (summary vs comprehensive)

**Benefits:**
- Simple tasks handled efficiently (Skill)
- Complex tasks get full capability (Subagent)
- Cost optimized automatically
- User gets appropriate level of analysis

### Implementation Checklist

- [ ] Define complexity thresholds clearly
- [ ] Implement decision logic (IF/THEN rules)
- [ ] Create Skill for simple cases
- [ ] Configure Subagent for complex cases
- [ ] Test both execution paths
- [ ] Monitor routing decisions for optimization

---

## V. BEST PRACTICES

**Start Simple:** Begin with Pattern 1 (orchestration + utilities), scale to Pattern 2/3 when needed.

**Separation of Concerns:** Subagents orchestrate workflows, Skills provide utilities. Clear boundaries.

**Token Efficiency:** Extract duplicates to Skills immediately. Research validates 40-65% reduction.

**Maintainability:** Update Skills once, all subagents benefit. Version control Skills separately.

**Cost Optimization:** Use Pattern 3 for intelligent routing. Simple tasksâ†’Skills (cheap), Complexâ†’Subagents (justified).

**Progressive Disclosure:** Design Skills with references. Main instructions + on-demand details.

---

## WHEN TO READ NEXT

**For Cost Details:**
Token economics analysis â†’ `05-token-economics.md`

**For Implementation:**
Real-world validation â†’ `case-studies.md`
Platform constraints â†’ `06-platform-constraints.md`
Security considerations â†’ `07-security-concerns.md`

**If Starting Fresh:**
Review conceptual differences â†’ `02-skills-vs-subagents-comparison.md`
Use decision framework â†’ `03-skills-vs-subagents-decision-tree.md`

---

**FILE END - Estimated Token Count: ~2,000 tokens (~270 lines)**
