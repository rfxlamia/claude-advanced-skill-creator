# Knowledge Base Index

Quick reference for on-demand file loading during skill creation workflows.

**Total Files:** 22 knowledge files organized in 3 categories
- **Foundation** (Files 01-08): Core concepts and decision frameworks
- **Application** (Files 09-13): Real-world implementation guidance
- **Tools** (Files 14-22): Automation script documentation

---

## Quick Navigation

### By Topic

#### Platform & Architecture
- **[01] Why Skills Exist** → `foundation/01-why-skills-exist.md`
  - Problem skills solve, platform capabilities vs limitations
- **[06] Platform Constraints** → `foundation/06-platform-constraints.md`
  - Size limits, markdown requirements, invocation mechanics
- **[10] Technical Architecture** → `application/10-technical-architecture.md`
  - System design, progressive disclosure, 3-level model

#### Decision Making & Planning
- **[02] Skills vs Subagents Comparison** → `foundation/02-skills-vs-subagents-comparison.md`
  - Conceptual differences, when to use each approach
- **[03] Skills vs Subagents Decision Tree** → `foundation/03-skills-vs-subagents-decision-tree.md`
  - 8-question decision framework with scoring
- **[04] Hybrid Patterns** → `foundation/04-hybrid-patterns.md`
  - Combining skills + subagents for optimal results
- **[08] When NOT to Use Skills** → `foundation/08-when-not-to-use-skills.md`
  - Anti-patterns and misuse scenarios
- **[18] Decision Helper Guide** → `tools/18-decision-helper-guide.md`
  - Using decision_helper.py for automated recommendations

#### Token Economics & Optimization
- **[05] Token Economics** → `foundation/05-token-economics.md`
  - Cost analysis, progressive disclosure benefits
- **[15] Cost Tools Guide** → `tools/15-cost-tools-guide.md`
  - Using token_estimator.py and split_skill.py
- **[20] Split Skill Guide** → `tools/20-split-skill-guide.md`
  - Auto-splitting large SKILL.md for efficiency

#### Security & Best Practices
- **[07] Security Concerns** → `foundation/07-security-concerns.md`
  - Command injection, XSS, validation requirements
- **[16] Security Tools Guide** → `tools/16-security-tools-guide.md`
  - Using security_scanner.py for vulnerability detection

#### Quality Assurance
- **[12] Testing and Validation** → `application/12-testing-and-validation.md`
  - Quality standards, validation criteria
- **[14] Validation Tools Guide** → `tools/14-validation-tools-guide.md`
  - Using validate_skill.py for structure checking
- **[19] Test Generator Guide** → `tools/19-test-generator-guide.md`
  - Using test_generator.py for automated test creation
- **[21] Quality Scorer Guide** → `tools/21-quality-scorer-guide.md`
  - Using quality_scorer.py for comprehensive scoring

#### Workflow Patterns & Implementation
- **[17] Pattern Tools Guide** → `tools/17-pattern-tools-guide.md`
  - Using pattern_detector.py for workflow recommendations
- **[22] Migration Helper Guide** → `tools/22-migration-helper-guide.md`
  - Converting existing docs to skills

#### Case Studies & Strategy
- **[09] Case Studies** → `application/09-case-studies.md`
  - Real-world examples and success stories
- **[11] Adoption Strategy** → `application/11-adoption-strategy.md`
  - Team rollout, change management
- **[13] Competitive Landscape** → `application/13-competitive-landscape.md`
  - Comparison with alternatives

---

## By Workflow Step

### Step 0: Decision (Skills vs Subagents)
**Load these files:**
- [02] Skills vs Subagents Comparison
- [03] Skills vs Subagents Decision Tree
- [18] Decision Helper Guide

**Purpose:** Determine if skills is the right approach for your use case.

---

### Step 1: Research & Proposal Generation
**Load these files:**
- [09] Case Studies (for inspiration and patterns)
- [05] Token Economics (for cost-aware design)
- [17] Pattern Tools Guide (for workflow recommendations)

**Purpose:** Research best practices and generate implementation proposals.

---

### Step 1f: Execution Planning (P0/P1/P2)
**Load these files:**
- [05] Token Economics (for budget allocation)
- [06] Platform Constraints (for size limits)
- [10] Technical Architecture (for progressive disclosure)

**Purpose:** Plan file structure and token budgets.

---

### Step 2: Content Creation
**Load these files:**
- [06] Platform Constraints (YAML requirements, markdown format)
- [07] Security Concerns (avoid vulnerabilities)
- [04] Hybrid Patterns (if combining approaches)

**Purpose:** Write SKILL.md and knowledge files safely.

---

### Steps 3-8: Validation & Optimization
**Load these files:**
- [14] Validation Tools Guide (structure validation)
- [15] Cost Tools Guide (token estimation)
- [16] Security Tools Guide (vulnerability scanning)
- [19] Test Generator Guide (automated testing)
- [20] Split Skill Guide (if > 500 lines)
- [21] Quality Scorer Guide (comprehensive quality check)

**Purpose:** Ensure quality, security, and efficiency before deployment.

---

### Step 9: Package & Deploy
**Load these files:**
- [12] Testing and Validation (deployment checklist)
- [11] Adoption Strategy (rollout planning)

**Purpose:** Prepare skill for production use.

---

## By Use Case

### "I'm deciding if Skills is right for my task"
**Load:**
- [02] Skills vs Subagents Comparison
- [03] Skills vs Subagents Decision Tree
- [08] When NOT to Use Skills
- [18] Decision Helper Guide

**Tool:** Run `python scripts/decision_helper.py --analyze "your use case"`

---

### "I'm designing a new skill"
**Load:**
- [09] Case Studies (see examples)
- [17] Pattern Tools Guide (find workflow pattern)
- [04] Hybrid Patterns (if complex)
- [10] Technical Architecture (understand 3-level model)

**Tool:** Run `python scripts/pattern_detector.py "your use case"`

---

### "I'm optimizing token usage"
**Load:**
- [05] Token Economics
- [10] Technical Architecture (progressive disclosure)
- [15] Cost Tools Guide
- [20] Split Skill Guide

**Tools:**
- `python scripts/token_estimator.py skill-name/`
- `python scripts/split_skill.py skill-name/ --preview`

---

### "I'm validating a skill before deployment"
**Load:**
- [14] Validation Tools Guide
- [16] Security Tools Guide
- [21] Quality Scorer Guide
- [12] Testing and Validation

**Tools (run in sequence):**
```bash
python scripts/validate_skill.py skill-name/
python scripts/security_scanner.py skill-name/
python scripts/token_estimator.py skill-name/
python scripts/quality_scorer.py skill-name/
```

---

### "I'm converting a document to a skill"
**Load:**
- [22] Migration Helper Guide
- [05] Token Economics (for size planning)
- [06] Platform Constraints (requirements)

**Tool:** Run `python scripts/migration_helper.py document.md`

---

### "I'm troubleshooting a skill issue"
**Load based on issue type:**

**Structure Issues:**
- [06] Platform Constraints (YAML requirements)
- [14] Validation Tools Guide

**Performance Issues:**
- [05] Token Economics
- [15] Cost Tools Guide
- [20] Split Skill Guide

**Security Issues:**
- [07] Security Concerns
- [16] Security Tools Guide

**Quality Issues:**
- [12] Testing and Validation
- [21] Quality Scorer Guide

---

### "I'm planning team adoption"
**Load:**
- [11] Adoption Strategy
- [09] Case Studies (show value)
- [13] Competitive Landscape (justify choice)

---

## File Categories Reference

### Foundation (Conceptual Knowledge)
Files 01-08 provide core concepts and decision frameworks. Load when you need to understand "why" or make strategic decisions.

```
01 - Why Skills Exist            (problem & solution)
02 - Skills vs Subagents         (comparison)
03 - Decision Tree               (8-question framework)
04 - Hybrid Patterns             (combining approaches)
05 - Token Economics             (cost analysis)
06 - Platform Constraints        (technical limits)
07 - Security Concerns           (safety requirements)
08 - When NOT to Use             (anti-patterns)
```

### Application (Implementation Guidance)
Files 09-13 provide real-world implementation guidance. Load when planning or executing projects.

```
09 - Case Studies                (examples & patterns)
10 - Technical Architecture      (system design)
11 - Adoption Strategy           (rollout planning)
12 - Testing and Validation      (quality standards)
13 - Competitive Landscape       (market context)
```

### Tools (Script Documentation)
Files 14-22 document automation scripts in scripts/ directory. Load when using specific tools.

```
14 - Validation Tools            (validate_skill.py)
15 - Cost Tools                  (token_estimator.py, split_skill.py)
16 - Security Tools              (security_scanner.py)
17 - Pattern Tools               (pattern_detector.py)
18 - Decision Helper             (decision_helper.py)
19 - Test Generator              (test_generator.py)
20 - Split Skill                 (split_skill.py - detailed guide)
21 - Quality Scorer              (quality_scorer.py)
22 - Migration Helper            (migration_helper.py)
```

---

## Loading Strategy

### For Quick Tasks (Simple Skills)
**Load minimum:** 02, 03, 06, 14
- Decide if skill is right approach
- Understand constraints
- Validate structure

### For Standard Workflows (Medium Skills)
**Load core set:** 02-06, 09, 14-16, 21
- Full decision framework
- Examples and patterns
- Core validation tools

### For Complex Projects (Advanced Skills)
**Load comprehensive:** All 22 files
- Deep understanding of all concepts
- All optimization strategies
- Complete toolset

---

## Quick Search Index

**Keywords → Files:**

- **API, REST, GraphQL** → [09] Case Studies, [17] Pattern Tools
- **Architecture** → [10] Technical Architecture, [04] Hybrid Patterns
- **Automation** → [17] Pattern Tools, [14-22] All tool guides
- **Budget, Cost, Pricing** → [05] Token Economics, [15] Cost Tools
- **CI/CD, Pipeline** → [09] Case Studies, [12] Testing
- **Code Review** → [09] Case Studies, [17] Pattern Tools
- **Conversion, Migration** → [22] Migration Helper
- **Decision, Choice** → [02-03] Skills vs Subagents, [18] Decision Helper
- **Efficiency, Optimization** → [05] Token Economics, [15, 20] Cost Tools
- **Examples, Templates** → [09] Case Studies
- **Formats, YAML, Markdown** → [06] Platform Constraints
- **Hybrid, Combined** → [04] Hybrid Patterns
- **Progressive Disclosure** → [05] Token Economics, [10] Architecture
- **Quality, Score, Grade** → [12] Testing, [21] Quality Scorer
- **Security, Safety, XSS** → [07] Security Concerns, [16] Security Tools
- **Size, Large, Split** → [20] Split Skill Guide
- **Strategy, Adoption, Rollout** → [11] Adoption Strategy
- **Testing, Validation** → [12] Testing, [14, 19] Validation/Test Tools
- **Token, Context, Memory** → [05] Token Economics
- **Troubleshooting, Debug** → [12] Testing, [14, 16, 21] Validation tools
- **Workflow, Pattern, Process** → [17] Pattern Tools

---

## Version History

**v1.0** (2025-11-11)
- Initial index creation
- 22 files indexed across 3 categories
- Organized by topic, workflow step, and use case
- Keyword search index added

---

## Maintenance Notes

When adding new files to knowledge/:
1. Add entry to appropriate section (Foundation/Application/Tools)
2. Update "By Topic" section with cross-references
3. Update "By Workflow Step" if file relates to specific steps
4. Add relevant "By Use Case" entries
5. Update keyword search index
6. Increment version number

**Current file count:** 22
**Last updated:** 2025-11-11
