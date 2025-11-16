# Section 2: Full Creation Workflow

**Prerequisites:** Skill description provided, workspace available
**Quality Target:** >=7.5/10 (Good), >=8.0/10 (Excellent)
**Time:** <10 min with automation

### STEP 0: Decide Approach

**Tool:** `python scripts/decision_helper.py --analyze "description"`

**Gates:**
- IF "Skills" recommended -> PROCEED Step 1
- IF "Subagents" -> STOP, suggest alternative
- IF confidence <75% -> DISCUSS tradeoffs

**Knowledge:** `knowledge/foundation/02-skills-vs-subagents.md`

### STEP 1: Understand & Research

**Purpose:** Requirements + research + validated proposal + execution plan

**Workflow:** 1a -> 1b -> 1c -> 1d -> 1e -> 1f

#### 1a. Requirements
Ask: Tasks? Domain? Standards? Output formats?
Document requirements.

#### 1b. Knowledge Gaps
```
IF domain unfamiliar OR vague -> PROCEED 1c
ELSE -> OFFER research, user decides
```

#### 1c. Research [OFFER ALWAYS]
**Offer:** "Research [domain] best practices (~2-3 min)? Ensures research-driven vs assumptions."

**IF accepted:**
- Load: `references/research-methodology.md`
- Execute: 5-aspect VS strategy (technical, user, competitive, edge, innovation)
- Run: 3-5 web_search queries
- Synthesize: Findings summary
- Load knowledge if needed: foundation/02, 05, 07

#### 1d. Proposals
**Load:** `references/proposal-generation.md`

Generate 3-5 options via VS:
- Multi-criteria scoring
- Present: Options table + tradeoffs + token estimates
- Recommend: Highest probability option

**User patterns:** Direct select / Modify / Hybrid / Questions

#### 1e. Validate
```
User reviews -> Selects/modifies -> Claude confirms -> Documents blueprint
IF approved -> PROCEED Step 1f
IF modifications -> Adjust, re-present
IF uncertain -> Clarify, offer more research
```

**Checkpoint:** Blueprint approved before execution planning.

#### 1f. EXECUTION PLANNING

**Purpose:** Prevent over-planning by enforcing token budget and priorities

**Process:**
```
AFTER user approves proposal (Step 1e):

1. ANALYZE approved proposal structure
   - Count: How many reference files planned?
   - Calculate: Estimated tokens per file
   
2. ASSIGN PRIORITIES (P0/P1/P2)
   Priority Rules:
   - P0 (Critical): Must exist with substantial content (>=80 lines)
     * Core workflows, essential references
     * Cannot proceed without these
   - P1 (Important): Should exist with minimum content (>=40 lines)
     * Supporting documentation, helpful guides
     * Warn if missing but allow proceed
   - P2 (Optional): Placeholder acceptable
     * Nice-to-have references, future enhancements
     * Explicitly allowed to be "# TBD" stubs
   
3. ENFORCE TOKEN BUDGET RULES
   Rule 1: Each reference file MAX 300 tokens (~37 lines of content)
   Rule 2: Total reference files <= 70% of SKILL.md target tokens
   Rule 3: If >8 reference files -> MUST reduce OR reassign priorities
   
   Calculation Example:
   - SKILL.md target: 2000 tokens (250 lines)
   - Reference budget: 1400 tokens (70% limit)
   - Max files at 300 tokens each: 4-5 files
   - If proposal has 14 files -> Reduce to 4 P0 + 3 P1 + 7 P2
   
4. CREATE EXECUTION PLAN TABLE
   Output format:
   | File | Priority | Est. Lines | Est. Tokens | Creation Order |
   |------|----------|------------|-------------|----------------|
   | workflow.md | P0 | 80-120 | 240-360 | 1 |
   | api-ref.md | P0 | 90-110 | 270-330 | 2 |
   | examples.md | P1 | 40-60 | 120-180 | 3 |
   | advanced.md | P2 | placeholder | 0 | - |
   
5. USER VALIDATION CHECKPOINT
   Present to user:
   "Execution plan created:
   - 3 P0 files (must complete, ~900 tokens)
   - 2 P1 files (important, ~300 tokens)
   - 4 P2 files (placeholder OK, 0 tokens)
   Total estimated: 1200 tokens (within 1400 budget)
   
   This ensures focused effort on critical content.
   Approved? (y/n/adjust)"
   
   IF user says "too many P0" -> ADJUST priorities, recalculate
   IF user says "need more detail" -> EXPLAIN rationale for assignments
   IF approved -> DOCUMENT plan in comment, PROCEED Step 2
```

**Gate:** Cannot proceed to Step 2 without approved execution plan

**Output:** Execution plan documented in workspace (for Step 2.5 reference)

### STEP 2: Initialize & Create Content

**Options:**
A. `python scripts/migration_helper.py doc.md --format json` (if doc exists)
B. `python scripts/init_skill.py skill-name --path /home/claude` (Anthropic standard)
C. Manual folder creation

**Guide:** `knowledge/tools/22-migration-helper.md`

#### 2.5: CONTENT CREATION CHECKPOINT [NEW - CRITICAL]

**Purpose:** Enforce sequential creation with priority order

**Process:**
```
AFTER structure initialized (Step 2):

1. LOAD execution plan from Step 1f
   - Retrieve: P0/P1/P2 file assignments
   - Verify: reference files directory created
   
2. ENFORCE SEQUENTIAL CREATION RULE
   
   RULE: Create files in strict priority order
   - Phase 1: ALL P0 files (one by one, complete before next)
   - Phase 2: ALL P1 files (one by one, minimum 40 lines)
   - Phase 3: P2 files (placeholder OK with "# TBD" header)
   
   Example Sequence:
   1. Create P0 file 1 -> Verify >=80 lines -> Complete
   2. Create P0 file 2 -> Verify >=80 lines -> Complete
   3. Create P0 file 3 -> Verify >=80 lines -> Complete
   4. Create P1 file 1 -> Verify >=40 lines -> Complete
   5. Create P1 file 2 -> Verify >=40 lines -> Complete
   6. Create P2 files -> Placeholder acceptable
   
3. TOKEN BUDGET MONITORING
   Before creating each file:
   - Calculate: Current total tokens used
   - Check: Will this file exceed 70% budget?
   - IF yes -> STOP, reassess, inform user
   
   Running Example:
   - After P0 file 1 (300 tokens): 300/1400 (21%) - OK proceed
   - After P0 file 2 (280 tokens): 580/1400 (41%) - OK proceed
   - After P0 file 3 (350 tokens): 930/1400 (66%) - OK proceed
   - Before P1 file 1: Check if adding 180 tokens stays under 70%
   
4. COMPLETION VERIFICATION per file
   After creating P0/P1 file:
   - Count lines: `wc -l references/filename.md`
   - Check: P0 >=80 lines, P1 >=40 lines
   - IF fail -> MUST complete before next file
   
   Verification commands:
   ```bash
   # After creating P0 file
   lines=$(wc -l < references/p0-file.md)
   if [ $lines -lt 80 ]; then
     echo "ERROR: P0 file needs $((80 - lines)) more lines"
     # CANNOT proceed to next file
   fi
   ```
```

**Gate:** ALL P0 files must be complete before proceeding

**Output:** All P0 files created with >=80 lines each

#### 2.8: CONTENT COMPLETION VERIFICATION [NEW - CRITICAL]

**Purpose:** Final safety net before validation

**Process:**
```
BEFORE running validate_skill.py (Step 3):

1. RUN BASH VERIFICATION
   ```bash
   # Check P0 files exist and have content
   echo "Verifying P0 files..."
   p0_count=0
   p0_pass=0
   for file in references/*-p0-*.md references/p0-*.md; do
     if [ -f "$file" ]; then
       p0_count=$((p0_count + 1))
       lines=$(wc -l < "$file")
       if [ $lines -lt 80 ]; then
         echo "ERROR: P0 file $file only has $lines lines (need >=80)"
       else
         echo "OK: $file has $lines lines"
         p0_pass=$((p0_pass + 1))
       fi
     fi
   done
   
   if [ $p0_count -eq 0 ]; then
     echo "WARNING: No P0 files found (may use different naming)"
   elif [ $p0_pass -ne $p0_count ]; then
     echo "FAIL: Not all P0 files meet requirements"
     exit 1
   fi
   
   # Check P1 files
   echo "Verifying P1 files..."
   for file in references/*-p1-*.md references/p1-*.md; do
     if [ -f "$file" ]; then
       lines=$(wc -l < "$file")
       if [ $lines -lt 40 ]; then
         echo "WARN: P1 file $file only has $lines lines (need >=40)"
       else
         echo "OK: $file has $lines lines"
       fi
     fi
   done
   ```

2. REPORT TO USER
   Example output:
   "Content Verification Results:
   [OK] 3 P0 files complete (avg 95 lines)
   [OK] 2 P1 files complete (avg 52 lines)
   [INFO] 4 P2 files placeholder (as planned)
   
   All critical content verified.
   Ready for validation? (y/n)"
   
3. GATE ENFORCEMENT
   IF any P0 file <80 lines -> CANNOT proceed to Step 3
   IF P1 file <40 lines -> WARN user, allow proceed with confirmation
   IF user confirms -> PROCEED Step 3
   IF user wants to add content -> RETURN to content creation
```

**Gate:** Cannot proceed without verification pass

**Output:** Verification report confirming P0 completion

### STEP 3: Validate

**Tool:** `python scripts/validate_skill.py skill-name/ --format json`

**Gates:**
- IF success -> PROCEED Step 4
- IF critical -> FIX, re-run
- IF warnings -> REVIEW with user

**Guide:** `knowledge/tools/14-validation-tools.md`

### STEP 4: Security

**Tool:** `python scripts/security_scanner.py skill-name/ --format json`

**Gates:**
- IF no critical -> PROCEED Step 5
- IF critical -> FIX immediately
- IF medium -> DOCUMENT/fix

**Knowledge:** `knowledge/foundation/07-security-concerns.md`

### STEP 5: Tokens

**Tool:** `python scripts/token_estimator.py skill-name/ --format json`

**Gates:**
- <3000 tokens -> PROCEED Step 6
- 3000-5000 -> CONSIDER optimize
- >5000 -> MUST optimize via split_skill.py

**Knowledge:** `knowledge/foundation/05-token-economics.md`
**Guide:** `knowledge/tools/15-cost-tools-guide.md`

### STEP 6: Progressive Disclosure

**Tool:** `python scripts/split_skill.py skill-name/ --format json`

```
IF >350 lines -> SPLIT to references/
IF 200-350 -> OPTIMAL
IF <200 -> CHECK if minimal
```

**Guide:** `knowledge/tools/20-split-skill-guide.md`

### STEP 7: Tests

**Tool:** `python scripts/test_generator.py skill-name/ --format json`

Generates automated tests for validation.

**Guide:** `knowledge/tools/19-test-generator-guide.md`

### STEP 8: Quality (v1.2.1 Enhanced)

**Tool:** `python scripts/quality_scorer.py skill-name/ --format json`

**v1.2.1 Improvements:**
- Imperative voice detection improved 11x (3.33% → 37.50%)
- YAML frontmatter stripped before processing
- Markdown formatting properly removed (bold, italic, code, links)
- First 3 words checked instead of only first word
- Threshold lowered: 70% → 50% for full points

**Quality Gates:**
- **>=8.0 (Grade B+)** -> PROCEED Step 9 (Excellent quality)
- **7.5-7.9 (Grade C+)** -> ACCEPTABLE, consider improvements
- **7.0-7.4 (Grade C)** -> REVIEW improvements recommended
- **<7.0 (Grade D/F)** -> MUST improve before packaging

**Realistic Targets:**
- Most skills: 7.5-8.5/10 is good quality
- High-polish skills: 8.5-9.0/10 with manual refinement
- 9.0+/10: Exceptional, requires significant polish

**Score Interpretation:**
```
90-100 (Grade A): Exceptional - Production ready, comprehensive
80-89  (Grade B): Good - Minor improvements may help
70-79  (Grade C): Acceptable - Consider targeted improvements
60-69  (Grade D): Needs work - Address major issues
<60    (Grade F): Critical - Significant revision required
```

**Example Impact (v1.2.1):**
- readme-expert.skill: 78/100 (C) → 81/100 (B)
- Average improvement: 73% in scoring accuracy

**Guide:** `knowledge/tools/21-quality-scorer-guide.md`

### STEP 9: Package (v1.2.1 Enhanced)

**Tool:** `python scripts/package_skill.py skill-name/` (Anthropic)

**Usage Options:**
```bash
# Basic packaging
python scripts/package_skill.py skill-name/

# Custom output directory
python scripts/package_skill.py skill-name/ ./dist

# Strict mode (fail on any reference issues)
python scripts/package_skill.py skill-name/ ./dist --strict
```

**v1.2.1 Improvements:**
- Fixed output directory handling (respects user-specified paths)
- Fixed archive structure organization
- Enhanced pre-packaging validation
- Strict mode for production deployments

**Pre-Packaging Checklist:**
- ✅ Structure validation (validate_skill.py)
- ✅ Security audit (security_scanner.py)
- ✅ Token optimization (<5000 tokens ideal)
- ✅ Progressive disclosure (if >350 lines)
- ✅ Quality score >=7.5/10
- ✅ Reference validation (no broken links)
- ✅ No orphaned files (warnings shown)

**Output:** skill-name.skill (deploy-ready ZIP file)

**Validation Modes:**
- **Default**: Warns about reference issues, continues packaging
- **--strict**: Fails on any broken references or orphaned files

---

## Changelog Integration (v1.2.1)

**Recent Fixes Applied to Workflow:**

1. **quality_scorer.py** - Imperative Detection (Step 8)
   - 11x improvement in accuracy (3.33% → 37.50%)
   - Better handling of YAML and markdown formatting
   - More realistic scoring thresholds

2. **decision_helper.py** - Confidence Calculation (Step 0)
   - Fixed backwards confidence logic
   - Proper score-to-confidence mapping
   - More reliable recommendations

3. **package_skill.py** - Output & Structure (Step 9)
   - Fixed output directory handling
   - Corrected archive structure
   - Enhanced validation workflow

**For complete changelog:** [See CHANGELOG.md v1.2.1](../CHANGELOG.md#121---2025-11-14)

---
