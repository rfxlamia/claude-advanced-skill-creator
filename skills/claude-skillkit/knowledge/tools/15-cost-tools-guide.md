---
title: "Cost Tools: Token Estimation Guide"
purpose: "Quick start for token_estimator.py automation"
token_estimate: "800"
read_priority: "high"
read_when: ["Cost analysis needed", "Progressive disclosure planning", "Budget optimization"]
related_files:
  concepts: ["05-token-economics", "10-progressive-architecture", "15-cost-optimization"]
  tools: ["token_estimator.py", "validate_skill.py"]
last_updated: "2025-11-05"
---

# Cost Tools: Quick Start

## Overview

`token_estimator.py` predicts token consumption and monthly costs using 3-level progressive disclosure analysis.

**Zero deployment cost** - pure estimation. Prevents token bloat before production.

**Theory:** File 05, 10, 15. **This guide:** Usage only.

---

## Installation

```bash
python3 /mnt/user-data/outputs/scripts/token_estimator.py --help
```

No dependencies required (uses built-in libraries).

---

## Basic Usage

```bash
python3 token_estimator.py <skill_path> [--volume N] [--model MODEL] [--format FORMAT]
```

**Example:**
```bash
# Human-readable output (default)
python3 token_estimator.py ./my-skill/

# JSON output for automation (v1.0.1+)
python3 token_estimator.py ./my-skill/ --format json

# Output shows:
# - Progressive disclosure (3 levels)
# - Usage scenarios (idle/typical/worst)
# - Cost projections
# - Optimization recommendations
```

---

## Options

**Volume:** `--volume N` (default: 1000)
```bash
python3 token_estimator.py ./my-skill/ --volume 10000
# Projects costs for 10K monthly uses
```

**Model:** `--model MODEL` (default: claude-sonnet-4.5)
```bash
python3 token_estimator.py ./my-skill/ --model claude-opus-4
# Uses Opus pricing ($15/$75 per M tokens)
```

**Format:** `--format {text|json}` (default: text) *[New in v1.0.1]*
```bash
# JSON output - parseable by automation tools
python3 token_estimator.py ./my-skill/ --format json | python -m json.tool

# Text output - human-readable
python3 token_estimator.py ./my-skill/ --format text
```

---

## Workflows

**Baseline Measurement:** `python3 token_estimator.py ./my-skill/` (note typical tokens)

**Post-Optimization:** Re-run after applying File 10, 15 techniques (compare reduction)

**Budget Planning:** `--volume 50000 --model claude-sonnet-4.5` (enterprise projections)

---

## Understanding Output

| Component | Description | Target |
|-----------|-------------|--------|
| Level 1 (Metadata) | YAML, always loaded | <100 tokens |
| Level 2 (Body) | SKILL.md body, when triggered | <5,000 tokens |
| Level 3 (Refs) | References, on-demand | <2,000 each |

**Scenarios:** Idle (metadata) | Typical (+ body) | With-Ref (+ smallest ref) | Worst (all)

**Cost:** (Input Ã— $3/M) + (Output Ã— $15/M) Ã— Volume | Reference: Files 05, 10

---

## Optimization Loop

1. Baseline: `token_estimator.py ./my-skill/` (e.g., 4,800 typical)
2. Optimize: Apply File 10, 15 (move to references/, shorten description)
3. Re-measure: Run again (target: <3,000 typical)
4. Calculate: Compare costs (e.g., 50% reduction = $230/year savings)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Path not found | `ls ./my-skill/SKILL.md` |
| High tokens | File 10 (progressive disclosure) |
| Large metadata | Shorten description |

---

## Best Practices

- âœ… Estimate before building (set token budget)
- âœ… Check frequently during development
- âœ… Target: Metadata <100, Body <5,000, Refs <2,000
- âœ… Final check pre-deployment

**Toolchain:** validate_skill.py â†’ token_estimator.py â†’ optimize â†’ re-check

---

## Quick Reference

```bash
# Basic estimate (human-readable)
python3 token_estimator.py ./my-skill/

# JSON output for automation
python3 token_estimator.py ./my-skill/ --format json

# Custom volume
python3 token_estimator.py ./my-skill/ --volume 5000

# Opus pricing with JSON output
python3 token_estimator.py ./my-skill/ --model claude-opus-4 --format json
```

**Targets:** Metadata <100 | Body <5,000 | Refs <2,000 each

**Next:** Optimize with File 10, 15 techniques if over targets.

**v1.0.1 Changes:** Added `--format` parameter for JSON/text output standardization.
