---
name: advanced-skill-creator
description: >
  Professional skill creation with research-driven workflow and automated validation.
  
  USE WHEN: Creating new skills, validating existing skills, deciding between Skills 
  vs Subagents, migrating documents to skills, or running individual validation tools.
  
  PRIMARY TRIGGERS:
  "create skill" -> Full creation (12 steps with research + execution planning)
  "validate skill" -> Validation workflow (steps 3-8)
  "Skills vs Subagents" -> Decision workflow (step 0)
  "convert doc to skill" -> Migration workflow
  "estimate tokens" -> Token optimization
  "security scan" -> Security audit
  
  WORKFLOW COMPLIANCE: Structured workflows with validation checkpoints.
  Research phase (Step 1c-1d) ensures skills based on proven approaches.
  
  DIFFERENTIATOR: Research-driven creation. Web search (3-5 queries) before
  building. Multi-proposal generation. 9 automation scripts. Quality 9.0+/10.
  
  REUSED: Anthropic's init_skill.py and package_skill.py (production-tested).
---

## Section 1: Intent Detection & Routing
**Detect user intent, route to appropriate workflow.**

| Intent | Keywords | Route To |
|--------|----------|----------|
| Full creation | "create", "build", "new skill" | Section 2 |
| Validation | "validate", "check quality" | Section 3 |
| Decision | "Skills vs Subagents", "decide" | Section 4 |
| Migration | "convert", "migrate doc" | Section 5 |
| Single tool | "validate only", "estimate tokens", "scan" | Section 6 |

**PROCEED to corresponding section after intent detection.**

**Workflow Value:** Research-driven approach validates design before building.
Sequential steps with checkpoints produce 9.0/10+ quality vs ad-hoc creation.

---

## Section 2: Full Creation Workflow (Overview)

**Prerequisites:** Skill description provided, workspace available  
**Quality Target:** >=9.0/10  
**Time:** <10 min with automation

### 12-Step Process with Validation Gates:

**STEP 0: Decide Approach**
- Tool: `decision_helper.py`
- Decides: Skills vs Subagents
- Gate: Proceed only if "Skills" recommended

**STEP 1: Understand & Research** [ENHANCED]
- 1a. Gather requirements
- 1b. Identify knowledge gaps
- 1c. **Research domain** (web_search 3-5 queries)
- 1d. **Generate proposals** (3-5 options)
- 1e. **User validates** (checkpoint before build)
- 1f. **EXECUTION PLANNING** [NEW]
  - Assign priorities (P0: critical, P1: important, P2: optional)
  - Token budget allocation per file (max 300 tokens each)
  - Sequential creation plan (P0 -> P1 -> P2)
  - Gate: Approved execution plan required before init

**STEP 2: Initialize & Create Content** [ENHANCED]
- Tool: `python scripts/init_skill.py skill-name --path /path` (Anthropic)
- Alternative: `migration_helper.py` (if doc exists)
- Creates: skill folder structure
- **2.5: CONTENT CREATION CHECKPOINT** [NEW]
  - Sequential creation enforcement (P0 -> P1 -> P2 order)
  - Token budget monitoring per file
  - Line count verification (P0 >=80 lines, P1 >=40 lines)
  - Gate: ALL P0 files must complete before proceeding
- **2.8: CONTENT COMPLETION VERIFICATION** [NEW]
  - Bash verification script runs automatically
  - Reports: P0/P1/P2 completion status
  - Gate: Cannot proceed to validation with incomplete P0 files

**STEP 3: Validate Structure**
- Tool: `validate_skill.py`
- Gate: Fix critical issues before proceeding

**STEP 4: Security Audit**
- Tool: `security_scanner.py`
- Gate: Fix critical vulnerabilities immediately

**STEP 5: Token Optimization**
- Tool: `token_estimator.py`
- Gate: Optimize if >5000 tokens

**STEP 6: Progressive Disclosure**
- Tool: `split_skill.py`
- Gate: Split if SKILL.md >350 lines

**STEP 7: Generate Tests**
- Tool: `test_generator.py`
- Creates: Automated validation tests

**STEP 8: Quality Assessment**
- Tool: `quality_scorer.py`
- Gate: Must achieve >=9.0/10 before packaging

**STEP 9: Package for Deployment**
- Tool: `python scripts/package_skill.py skill-name/` (Anthropic)
- Creates: .skill file ready to deploy

**For detailed implementation:** [See references/section-2-full-creation-workflow.md](references/section-2-full-creation-workflow.md)

---

## Section 3: Validation Workflow (Overview)

**Use when:** Validating existing skill

**Steps:** Execute validation subset (Steps 3-8)
1. Structure validation (validate_skill.py)
2. Security audit (security_scanner.py)
3. Token analysis (token_estimator.py)
4. Progressive disclosure check
5. Test generation (optional)
6. Quality assessment (quality_scorer.py)

**For detailed workflow:** [See references/section-3-validation-workflow-existing-skill.md](references/section-3-validation-workflow-existing-skill.md)

---

## Section 4: Decision Workflow (Overview)

**Use when:** Uncertain if Skills is right approach

**Process:**
1. Run `decision_helper.py`
2. Answer interactive questions
3. Receive recommendation with confidence score
4. Proceed if Skills recommended (confidence >=75%)

**For detailed workflow:** [See references/section-4-decision-workflow-skills-vs-subagents.md](references/section-4-decision-workflow-skills-vs-subagents.md)

---

## Section 5: Migration Workflow (Overview)

**Use when:** Converting document to skill

**Process:**
1. Decision check (Step 0)
2. Migration analysis (migration_helper.py)
3. Structure creation
4. Execute validation steps (3-8)
5. Package (Step 9)

**For detailed workflow:** [See references/section-5-migration-workflow-doc-to-skill.md](references/section-5-migration-workflow-doc-to-skill.md)

---

## Section 6: Individual Tool Usage
**Use when:** User needs single tool, not full workflow

**Entry Point:** User asks for specific tool like "estimate tokens" or "security scan"

### Available Tools

**Validation Tool:**
```bash
python scripts/validate_skill.py skill-name/ --format json
```
Guide: `knowledge/tools/14-validation-tools-guide.md`

**Token Estimator:**
```bash
python scripts/token_estimator.py skill-name/ --format json
```
Guide: `knowledge/tools/15-cost-tools-guide.md`

**Security Scanner:**
```bash
python scripts/security_scanner.py skill-name/ --format json
```
Guide: `knowledge/tools/16-security-tools-guide.md`

**Pattern Detector:**
```bash
python scripts/pattern_detector.py skill-name/
```
Guide: `knowledge/tools/17-pattern-tools-guide.md`
Note: Output is human-readable (not JSON yet)

**Decision Helper:**
```bash
# Interactive mode (recommended)
python scripts/decision_helper.py --analyze "your skill description"

# Note: --format json not supported by this tool
# Output is always human-readable format
```
Guide: `knowledge/tools/18-decision-helper-guide.md`

**Test Generator:**
```bash
python scripts/test_generator.py skill-name/ --format json
```
Guide: `knowledge/tools/19-test-generator-guide.md`

**Split Skill:**
```bash
python scripts/split_skill.py skill-name/ --format json
```
Guide: `knowledge/tools/20-split-skill-guide.md`

**Quality Scorer:**
```bash
python scripts/quality_scorer.py skill-name/ --format json
```
Guide: `knowledge/tools/21-quality-scorer-guide.md`

**Migration Helper:**
```bash
python scripts/migration_helper.py doc.md --format json
```
Guide: `knowledge/tools/22-migration-helper-guide.md`

### Known Issues & Limitations

**Parameter Inconsistencies (Priority 2 - Being Fixed):**
- `decision_helper.py` does NOT support `--format json` parameter
- `pattern_detector.py` outputs human-readable format only (not JSON)
- Other tools consistently support `--format json`
- Workaround: Check tool guide before using

**Quality Scorer Context (Priority 3):**
- Scores are calibrated to specific heuristics
- Target: 7.5/10 is realistic (not 9.0/10 for all cases)
- High scores (8.5+) may require manual review beyond automated fixes
- Use quality_scorer.py as guidance, not absolute truth
- Supplement with manual checklist for final validation

---

## Section 7: Knowledge Reference Map (Overview)

**Strategic context loaded on-demand.**

### Foundation Concepts (Files 01-08):
- Why Skills exist vs alternatives
- Skills vs Subagents decision framework
- Token economics and efficiency
- Platform constraints and security
- When NOT to use Skills

### Application Knowledge (Files 09-13):
- Real-world case studies (Rakuten, Box, Notion)
- Technical architecture patterns
- Adoption and testing strategies
- Competitive landscape analysis

### Tool Guides (Files 14-22):
- One guide per automation script
- Usage patterns and parameters
- JSON output formats
- Integration examples

**For complete reference map:** [See references/section-7-knowledge-reference-map.md](references/section-7-knowledge-reference-map.md)

---

## Workflow Compliance Reinforcement
**This skill works best when workflows are followed sequentially.**

**Why compliance matters:**
1. Research validation reduces iteration (validate before build)
2. Security checks prevent vulnerabilities (catch issues early)
3. Token optimization ensures efficiency (avoid bloat)
4. Quality gates maintain standards (9.0/10+ target)

**Mechanisms encouraging compliance:**
- Frontmatter priming: "WORKFLOW COMPLIANCE" statement
- Section routing: Explicit "PROCEED to Section X"
- Validation gates: IF/THEN with checkpoints
- Quality target: ">=9.0/10 requires following workflow"

**Flexible when needed:**
- Single tool usage (Section 6) skips full workflow
- Validation-only (Section 3) runs subset of steps
- User can request deviations with justification

**Goal:** Strong encouragement through design, not strict enforcement.

---

## Additional Resources

**Detailed implementations available in references/ directory:**

All section overviews above link to detailed reference files for deep-dive information.
Load references on-demand when detailed implementation guidance needed.
