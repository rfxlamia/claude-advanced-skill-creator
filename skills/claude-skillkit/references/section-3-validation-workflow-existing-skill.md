# Section 3: Validation Workflow (Existing Skill)

**Use when:** User has existing skill, wants to validate quality/compliance

**Prerequisites:**
- Skill folder exists
- SKILL.md file present

**Entry Point:** User says "validate my skill" or "check skill quality"

### Validation Steps

Execute Steps 3-8 from Full Creation Workflow:

1. **Structure Validation** (Step 3)
   - Run `scripts/validate_skill.py skill-name/ --format json`
   - Check critical issues
   - Fix if needed

2. **Security Audit** (Step 4)
   - Run `scripts/security_scanner.py skill-name/ --format json`
   - Address critical/medium issues

3. **Token Analysis** (Step 5)
   - Run `scripts/token_estimator.py skill-name/ --format json`
   - Optimize if needed

4. **Progressive Disclosure Check** (Step 6)
   - Verify SKILL.md line count
   - Split if >350 lines

5. **Test Generation** (Step 7 - optional)
   - Run `scripts/test_generator.py skill-name/ --format json`
   - Execute tests

6. **Quality Assessment** (Step 8)
   - Run `scripts/quality_scorer.py skill-name/ --format json`
   - Review score and recommendations

### Validation Report

Present comprehensive report:
```
VALIDATION REPORT: [skill-name]

Structure: [PASS/FAIL]
Security: [PASS/FAIL] 
Tokens: [EFFICIENT/NEEDS_OPTIMIZATION]
Quality Score: [X.X/10]

Issues Found: [count]
- Critical: [list]
- Warnings: [list]

Recommendations:
1. [Priority action]
2. [Secondary action]
3. [Optional improvement]

Overall Status: [READY/NEEDS_WORK]
```

---
