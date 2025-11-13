---
name: test-generator-guide
description: "Usage guide for test_generator.py - Auto-generate comprehensive test scenarios for skills"
---

# Test Generator Usage Guide

**Script:** test_generator.py  
**Purpose:** Auto-generate comprehensive test scenarios from skill descriptions  
**Impact:** Saves 1-2 hours per skill testing  
**References:** File 12 (testing best practices)

---

## Quick Start

### Basic Usage

```bash
# Standard coverage with pytest
python test_generator.py path/to/skill/

# Comprehensive coverage
python test_generator.py path/to/skill/ --coverage comprehensive

# Unittest format
python test_generator.py path/to/skill/ --format unittest
```

### What Gets Generated

```
skill-directory/
â””â”€â”€ tests/
    â”œâ”€â”€ test_scenarios.md    # Human-readable test scenarios
    â””â”€â”€ test_skill.py        # Test implementation skeleton
```

---

## Coverage Levels

| Level | Description | Scenarios per Capability |
|-------|-------------|-------------------------|
| **basic** | Happy path only | 1 scenario |
| **standard** | Happy + error cases | 3 scenarios |
| **comprehensive** | Happy + error + edge cases | 5+ scenarios |

**Recommendation:** Use `standard` for most skills, `comprehensive` for critical skills.

---

## Test Formats

### pytest (Default)

```bash
python test_generator.py my-skill/ --format pytest
```

Generates pytest-compatible test functions:
```python
def test_01_capability_description():
    """Test description."""
    # TODO: Implement test logic
    pass
```

**Run tests:** `pytest my-skill/tests/`

### unittest

```bash
python test_generator.py my-skill/ --format unittest
```

Generates unittest.TestCase class:
```python
class TestSkill(unittest.TestCase):
    def test_01_capability_description(self):
        """Test description."""
        pass
```

**Run tests:** `python -m unittest discover my-skill/tests`

### plain

```bash
python test_generator.py my-skill/ --format plain
```

Generates plain text test plan (no code).

---

## How It Works

### 1. Parse SKILL.md

Extracts testable capabilities from:
- Frontmatter description
- "can X" patterns
- WHEN clauses
- Bullet points

### 2. Generate Scenarios

For each capability:
- **P0 (Critical):** Happy path
- **P1 (High):** Error handling + invalid input
- **P2 (Medium):** Edge cases (empty, large, etc.)

### 3. Write Files

- **test_scenarios.md:** Human-readable documentation
- **test_skill.py:** Implementation skeleton with TODOs

---

## Examples

### Example 1: JSON Converter Skill

```bash
$ python test_generator.py json-converter/ --coverage standard

Generating tests for json-converter/...
Skill: json-converter
Capabilities found: 2
Test scenarios generated: 6
  - P0 (Critical): 2
  - P1 (High): 4
  - P2 (Medium): 0

âœ… Test documentation: json-converter/tests/test_scenarios.md
âœ… Pytest implementation: json-converter/tests/test_skill.py
```

### Example 2: Comprehensive Testing

```bash
$ python test_generator.py api-wrapper/ --coverage comprehensive

Test scenarios generated: 15
  - P0 (Critical): 3
  - P1 (High): 6
  - P2 (Medium): 6
```

---

## Integration with Workflow

### Step 1: Develop Skill

Create your SKILL.md with clear capability descriptions.

### Step 2: Generate Tests

```bash
python test_generator.py my-skill/ --coverage standard
```

### Step 3: Review Scenarios

```bash
cat my-skill/tests/test_scenarios.md
```

Check if all important capabilities are covered.

### Step 4: Implement Tests

Edit `my-skill/tests/test_skill.py` and replace `pass` with actual test logic.

### Step 5: Run Tests

```bash
pytest my-skill/tests/
```

---

## Error Handling

### Missing SKILL.md

```bash
Ã¢Å’ Error: SKILL.md not found in path/to/skill
```

**Solution:** Ensure skill directory contains SKILL.md file.

### No Capabilities Found

If frontmatter description is too generic, the script may not extract capabilities. 

**Solution:** Add clear capability statements:
- Use bullet points
- Include "can X" patterns
- Add WHEN clauses

---

## Best Practices

**For Better Test Generation:**
1. Write clear, specific capability descriptions in frontmatter
2. Use action verbs (convert, parse, analyze, validate)
3. Include WHEN clauses in SKILL.md content
4. List features as bullet points

**After Generation:**
1. Review test_scenarios.md for completeness
2. Add custom scenarios if needed
3. Implement test logic incrementally
4. Start with P0 tests first

---

## Limitations

**What Script CANNOT Do:**
- Implement actual test logic (provides skeleton only)
- Infer complex test data without examples
- Test runtime behavior automatically

**What You Must Do:**
- Implement test logic in TODO sections
- Provide skill-specific test inputs
- Add assertions for expected outputs

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Tests generated successfully |
| 1 | Invalid skill path or missing SKILL.md |
| 2 | Unexpected error during generation |

---

## Success Metrics

**Time Savings:**
- Manual test creation: 1-2 hours
- Script execution: <5 seconds
- **Savings:** 99% time reduction

**Coverage:**
- Standard: 3 scenarios per capability
- Comprehensive: 5+ scenarios per capability
- Identifies edge cases automatically

---

**References:**
- File 12: Testing & Validation (best practices)
- script-opportunities-analysis.md: Original requirements
- phase3b-remaining-scripts-planning.md: Implementation plan
