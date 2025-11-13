---
name: split-skill-guide
description: "Usage guide for split_skill.py - Auto-split large SKILL.md for progressive disclosure"
---

# Split Skill Usage Guide

**Script:** split_skill.py  
**Purpose:** Auto-split large SKILL.md into main file + references  
**Impact:** Enforces progressive disclosure (200-350 line target)  
**References:** Files 05, 10 (token optimization, architecture)

---

## Quick Start

### Preview Split (Recommended First)

```bash
# See what would be split without making changes
python split_skill.py path/to/skill/ --preview
```

### Execute Split

```bash
# Interactive mode (asks for confirmation)
python split_skill.py path/to/skill/

# Auto mode (no confirmation)
python split_skill.py path/to/skill/ --auto

# Custom threshold
python split_skill.py path/to/skill/ --threshold 400
```

---

## What Gets Split

### Core Sections (Stay in SKILL.md)
- Overview
- Installation / Setup
- Quick Start
- Basic Usage
- Core Workflow

### Reference Sections (Move to references/)
- Advanced usage
- Troubleshooting
- Extended examples
- API reference
- Edge cases
- Sections >100 lines

---

## Example Output

**Before:** 721 lines SKILL.md

**After Split:**
```
skill/
â”œâ”€â”€ SKILL.md (212 lines)          # Core content + links
â”œâ”€â”€ split_report.md                # Split summary
â””â”€â”€ references/
    â”œâ”€â”€ advanced-topic-1.md
    â”œâ”€â”€ troubleshooting.md         # 82 lines
    â”œâ”€â”€ additional-examples.md     # 314 lines
    â””â”€â”€ ... (16 files total)
```

**Reduction:** 69.1% (721 â†’ 212 lines in main file)

---

## Classification Logic

**Core Criteria (keywords):**
- overview, setup, installation, quick start
- basic usage, core, workflow, getting started

**Reference Criteria (keywords):**
- advanced, troubleshooting, examples, reference
- edge case, detailed, appendix, additional

**Heuristic:**
- Sections >100 lines â†’ move to references

---

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--threshold N` | Line count trigger | 500 |
| `--preview` | Show plan without executing | False |
| `--auto` | Skip confirmation | False |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success or already optimal |
| 1 | SKILL.md not found |
| 2 | Unexpected error |

---

## Best Practices

**Before Splitting:**
1. Run with `--preview` first
2. Review which sections move to references
3. Ensure section titles are clear

**After Splitting:**
1. Review updated SKILL.md
2. Check reference files are complete
3. Test cross-reference links
4. Read split_report.md

---

## Integration with Workflow

```bash
# Step 1: Develop skill (grows >500 lines)
# Step 2: Preview split
python split_skill.py my-skill/ --preview

# Step 3: Execute if satisfied
python split_skill.py my-skill/ --auto

# Step 4: Validate result
cat my-skill/SKILL.md
ls my-skill/references/
```

---

## References

- File 05: Token Economics (why progressive disclosure matters)
- File 10: Architecture (optimal file structure)
- phase3b-remaining-scripts-planning.md: Implementation plan
