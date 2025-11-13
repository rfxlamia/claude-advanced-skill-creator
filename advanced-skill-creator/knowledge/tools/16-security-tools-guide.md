---
title: "Security Tools: Vulnerability Scanning Guide"
purpose: "Quick start for security_scanner.py automation"
token_estimate: "800"
read_priority: "critical"
read_when: ["Before deployment", "Security audit", "Third-party skill review"]
related_files:
  concepts: ["07-security-concerns", "14-validation-theory"]
  tools: ["security_scanner.py", "validate_skill.py"]
last_updated: "2025-11-05"
---

# Security Tools: Quick Start

## Overview

`security_scanner.py` detects 7 types of security vulnerabilities automatically. **Zero false sense of security** - finds real risks.

**Critical for:** Pre-deployment, third-party skill audits, compliance checks.

**Theory:** File 07. **This guide:** Usage only.

---

## Installation

```bash
python3 /mnt/user-data/outputs/scripts/security_scanner.py --help
```

No dependencies (uses built-in libraries).

---

## Basic Usage

```bash
python3 security_scanner.py <skill_path> [--severity LEVEL] [--format FORMAT]
```

**Example:**
```bash
python3 security_scanner.py ./my-skill/

# Output shows:
# - Critical issues (must fix)
# - High severity (should fix)
# - Medium issues (review)
# - Exit code: 0=ok, 1=high, 2=critical
```

---

## Vulnerability Types

7 types detected automatically:
- **CRITICAL:** Hardcoded secrets, shell=True, eval/exec
- **HIGH:** SQL injection, pickle, unsafe yaml.load()
- **MEDIUM:** Path traversal, network calls, prompt injection

Reference: File 07 for prevention.

---

## Options

`--severity LEVEL`: Filter by CRITICAL/HIGH/MEDIUM/LOW

`--format json`: Machine-readable for CI/CD

---

## Workflows

**Pre-Deploy:** `security_scanner.py ./skill/` (exit 0=ok, 1=high, 2=critical)

**CI/CD:** `--severity CRITICAL --format json` in pipeline

**Third-Party:** Scan untrusted skills before use

---

## Remediation Guide

| Severity | Action | Common Fixes |
|----------|--------|--------------|
| CRITICAL | Do NOT deploy | Env vars for secrets, remove shell=True/eval/exec |
| HIGH | Fix before prod | Parameterized queries, json instead of pickle |
| MEDIUM | Review & mitigate | Validate paths, verify network calls (File 07) |

**False Positives:** URLs in docs (expected), review all in context

---

## Best Practices

- âœ… Scan before EVERY deployment (MUST pass)
- âœ… Address all CRITICAL findings
- âœ… Never commit secrets (use env vars)
- âœ… Scan third-party skills before use
- âœ… Test in isolated environment

**Toolchain:** validate_skill.py â†’ security_scanner.py â†’ token_estimator.py

---

## Quick Reference

```bash
# Standard scan
python3 security_scanner.py ./my-skill/

# Critical only
python3 security_scanner.py ./my-skill/ --severity CRITICAL

# JSON for CI/CD
python3 security_scanner.py ./my-skill/ --format json
```

**Exit Codes:** 0=safe | 1=high severity | 2=critical issues

**Next:** File 07 for remediation techniques, validate_skill.py for structure.
