---
title: "Pattern Tools: Workflow Selection Guide"
purpose: "Quick start for pattern_detector.py automation"
token_estimate: "800"
read_priority: "medium"
read_when: ["Designing new skill", "Pattern selection needed", "Architecture planning"]
related_files:
  concepts: ["04-hybrid-patterns", "09-case-studies", "Panduan-Komprehensif"]
  tools: ["pattern_detector.py"]
last_updated: "2025-11-05"
---

# Pattern Tools: Quick Start

## Overview

`pattern_detector.py` recommends workflow patterns from 8 proven patterns. **Accelerates design** by matching use cases to best practices.

**Use when:** Starting new skill, unsure which pattern fits, learning proven architectures.

**Theory:** Panduan Komprehensif, Files 04, 09. **This guide:** Usage only.

---

## Installation

```bash
python3 /mnt/user-data/outputs/scripts/pattern_detector.py --help
```

No dependencies (built-in libraries only).

---

## Basic Usage

```bash
python3 pattern_detector.py "your use case description" [--format {text|json}]
python3 pattern_detector.py --interactive
python3 pattern_detector.py --list [--format {text|json}]
```

**Example:**
```bash
# Human-readable output (default)
python3 pattern_detector.py "convert PDF to Word"

# JSON output for automation (v1.0.1+)
python3 pattern_detector.py "convert PDF to Word" --format json

# Output:
# - Recommended pattern: Read-Process-Write
# - Match confidence: 33%
# - Use cases, examples, references
# - (JSON mode: includes alternatives and structured data)
```

---

## Three Modes

**1. Analysis Mode:** Describe use case, get recommendation
```bash
# Text output (default)
python3 pattern_detector.py "scan code for security issues"

# JSON output (v1.0.1+)
python3 pattern_detector.py "scan code for security issues" --format json
# â†' Search-Analyze-Report pattern with alternatives in JSON
```

**2. Interactive Mode:** Guided questionnaire
```bash
python3 pattern_detector.py --interactive
# Answer questions â†' Get recommendation
# Note: Interactive mode does not support JSON output
```

**3. List Mode:** See all patterns
```bash
# Text output - formatted list
python3 pattern_detector.py --list

# JSON output - parseable structure (v1.0.1+)
python3 pattern_detector.py --list --format json
# Shows all 8 patterns with keywords and examples
```

---

## The 8 Patterns

| Pattern | Use For |
|---------|---------|
| Read-Process-Write | File transformations, cleanup |
| Search-Analyze-Report | Code analysis, security scans |
| Script Automation | CI/CD, test automation |
| Wizard Multi-Step | Project setup, configuration |
| Template Generation | Reports, emails, documents |
| Iterative Refinement | Code review, optimization |
| Context Aggregation | Dashboards, status reports |
| Validation Pipeline | Data validation, compliance |

Reference: Panduan Komprehensif for details.

---

## Workflows

**Selection:** Describe use case â†’ Review recommendation + alternatives â†’ Study pattern (Panduan)

**Learning:** List patterns â†’ Study Panduan â†’ Try interactive mode

---

## Output Interpretation

**Confidence:** >50% (strong) | 30-50% (good, check alternatives) | <30% (weak, try interactive)

**Alternatives:** Shown when confidence < 50%

---

## Best Practices & Tips

- âœ… Use at design phase (before coding)
- âœ… Review alternatives if confidence < 50%
- âœ… Include pattern keywords for better matches
- âœ… Use interactive mode for guidance
- âœ… Study Panduan + File 04 (hybrid) + File 09 (examples)

---

## Troubleshooting

**Low confidence (<30%):**
- Use --interactive mode
- Add more keywords to description
- Review --list to see all options

**Wrong pattern recommended:**
- Check alternatives shown
- Try interactive mode for guided selection
- Keywords might be misleading (e.g., "report" â†’ template vs analysis)

---

## Quick Reference

```bash
# Analysis
python3 pattern_detector.py "convert PDF"

# Interactive
python3 pattern_detector.py -i

# List all
python3 pattern_detector.py -l
```

**Next:** Panduan Komprehensif for pattern details â†’ File 04 for hybrids â†’ File 09 for examples.
