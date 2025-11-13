---
name: migration-helper-guide
description: "Usage guide for migration_helper.py - Convert docs to skill format"
tool_name: "migration_helper.py"
tool_type: "agent-layer"
read_priority: "medium"
read_when:
  - "User wants to convert existing docs to skill"
  - "Has markdown or text documentation"
  - "Needs rapid skill creation"
  - "Bulk conversion required"
related_files:
  - "File 10: Technical architecture"
  - "File 05: Token economics"
  - "Files 01-13: Best practices"
token_estimate: "800"
last_updated: "2025-11-08"
---

# Migration Helper Guide

## PURPOSE

Agent-layer tool untuk convert existing documentation (MD, TXT) to proper skill format. Automates structure generation, section classification, and frontmatter creation.

**Flow:** User provides doc â†’ Claude calls tool â†’ JSON output â†’ Skill created

---

## SUPPORTED FORMATS

| Format | Extension | Status |
|--------|-----------|--------|
| Markdown | .md, .markdown | âœ… Full support |
| Plain text | .txt | âœ… Full support |
| PDF | .pdf | âŒ Future |
| DOCX | .docx | âŒ Future |

---

## USAGE (AGENT-LAYER)

### Standard Conversion

```bash
python migration_helper.py source.md --format json
```

**Output:**
```json
{
  "status": "success",
  "source": "company-guide.md",
  "format": "markdown",
  "skill_name": "company-guide",
  "preview": false,
  "conversion": {
    "source_lines": 543,
    "skill_md_lines": 187,
    "core_sections": 4,
    "reference_sections": 8,
    "reduction_percent": 65.6
  },
  "output": {
    "skill_path": "./company-guide",
    "skill_md": "./company-guide/SKILL.md",
    "references": ["advanced-features.md", "troubleshooting.md", ...],
    "report": "./company-guide/conversion_report.md"
  }
}
```

---

### Preview Mode (Before Converting)

```bash
python migration_helper.py source.md --preview --format json
```

**Output:** Same structure with `"preview": true` and no files created.

---

### Custom Options

```bash
# Custom skill name
python migration_helper.py doc.md --skill-name my-skill --format json

# Custom output directory
python migration_helper.py doc.md --output-dir ./skills/ --format json

# Combined
python migration_helper.py doc.md --skill-name my-skill --output-dir ./skills/ --preview --format json
```

---

## CLASSIFICATION LOGIC

### Core Sections (â†’ SKILL.md)
Keywords: overview, introduction, setup, installation, quick start, getting started, basic, usage, workflow, how to use

**Characteristics:**
- Essential understanding
- Getting started content
- Basic workflows
- â‰¤100 lines

### Reference Sections (â†’ references/)
Keywords: advanced, troubleshooting, examples, reference, API, edge cases, detailed, appendix, additional, extended

**Characteristics:**
- Advanced topics
- Detailed examples
- Technical specs
- >100 lines

---

## ERROR RESPONSES

### File Not Found
```json
{
  "status": "error",
  "error_type": "FileNotFound",
  "message": "Source not found: missing.md",
  "help": "Ensure source file exists and path is correct"
}
```

### Unsupported Format
```json
{
  "status": "error",
  "error_type": "UnsupportedFormat",
  "message": "Unsupported format: .pdf",
  "help": "Only .md, .markdown, and .txt files are supported"
}
```

### Unexpected Error
```json
{
  "status": "error",
  "error_type": "UnexpectedError",
  "message": "...",
  "help": "Check file permissions and content format"
}
```

---

## CLAUDE'S USAGE PATTERN

**Step 1:** User requests conversion
```
User: "Convert this markdown file to a Claude skill"
```

**Step 2:** Claude calls tool with preview first
```python
# Preview to show user what will happen
result = bash_tool("python migration_helper.py /path/to/doc.md --preview --format json")
data = json.loads(result.stdout)

if data['status'] == 'success':
    # Show preview to user
    print(f"This will create skill '{data['skill_name']}' with:")
    print(f"- {data['conversion']['core_sections']} core sections")
    print(f"- {data['conversion']['reference_sections']} reference files")
    print(f"- {data['conversion']['reduction_percent']}% size reduction")
```

**Step 3:** If user approves, execute conversion
```python
# Actual conversion (without --preview)
result = bash_tool("python migration_helper.py /path/to/doc.md --format json")
data = json.loads(result.stdout)

if data['status'] == 'success':
    # Inform user of success
    print(f"âœ… Skill created at: {data['output']['skill_path']}")
    print(f"Next: Review SKILL.md and validate structure")
```

**Step 4:** Suggest next actions
```
Next steps:
1. Review SKILL.md frontmatter
2. Validate: python validate_skill.py {skill_path}/
3. Check quality: python quality_scorer.py {skill_path}/ --format json
```

---

## GENERATED STRUCTURE

```
{skill-name}/
â”œâ”€â”€ SKILL.md                  # Core content + frontmatter
â”œâ”€â”€ conversion_report.md      # Conversion summary
â””â”€â”€ references/               # Reference materials (if any)
    â”œâ”€â”€ advanced-features.md
    â”œâ”€â”€ troubleshooting.md
    â”œâ”€â”€ examples.md
    â””â”€â”€ ...
```

**SKILL.md includes:**
- YAML frontmatter (name, description, source)
- Core sections
- Additional Resources section (links to references/)

---

## EXIT CODES

| Code | Meaning | Scenario |
|------|---------|----------|
| 0 | Success | Conversion completed |
| 1 | Invalid input | File not found, unsupported format |
| 2 | Unexpected error | Permission denied, I/O error |

---

## CONVERSION WORKFLOW

**Typical Agent-Layer Flow:**

1. **Parse source** â†’ Detect format, extract sections
2. **Classify** â†’ Core vs reference sections
3. **Generate frontmatter** â†’ Auto-create YAML metadata
4. **Plan** â†’ Calculate reduction, estimate tokens
5. **Execute** â†’ Create skill structure, generate files
6. **Report** â†’ Conversion summary with next steps

---

## HUMAN-READABLE MODE

**For developer debugging:**

```bash
# Preview in console
python migration_helper.py doc.md --preview

# Convert with console output
python migration_helper.py doc.md

# Custom options
python migration_helper.py doc.md --skill-name my-skill --output-dir ./skills/
```

**Note:** Claude always uses `--format json` for machine-parseable output.

---

## INTEGRATION EXAMPLE

```python
# Complete skill creation workflow

# Step 1: Convert docs
convert_result = bash_tool(
    "python migration_helper.py company-docs.md --format json"
)
convert_data = json.loads(convert_result.stdout)

if convert_data['status'] != 'success':
    # Handle error
    return

skill_path = convert_data['output']['skill_path']

# Step 2: Validate structure
validate_result = bash_tool(
    f"python validate_skill.py {skill_path} --format json"
)

# Step 3: Check quality
quality_result = bash_tool(
    f"python quality_scorer.py {skill_path} --format json"
)
quality_data = json.loads(quality_result.stdout)

# Step 4: Optimize if needed
if quality_data['overall']['percentage'] < 70:
    # Suggest improvements or split
    split_result = bash_tool(
        f"python split_skill.py {skill_path} --preview"
    )

# Step 5: Report to user
print(f"âœ… Skill created and validated")
print(f"Quality: {quality_data['overall']['grade']}")
```

---

## BEST PRACTICES

**Before Converting:**
1. Use `--preview` first to see conversion plan
2. Check that source format is supported
3. Review section titles for better classification

**After Converting:**
1. âœ… Review SKILL.md frontmatter (update description)
2. âœ… Add trigger phrases (WHEN to use)
3. âœ… Validate: `python validate_skill.py {skill}/`
4. âœ… Test skill in Claude
5. âœ… Optimize if needed

**For Bulk Conversion:**
```bash
for doc in docs/*.md; do
  python migration_helper.py "$doc" --output-dir ./skills/ --format json
done
```

---

## LIMITATIONS

**Current:**
- MD and TXT only (no PDF, DOCX yet)
- Auto-generated descriptions may need manual refinement
- Section classification is heuristic-based (~85% accuracy)

**Workarounds:**
- Manually edit SKILL.md after conversion
- Use `--skill-name` for better naming
- Review classification in preview mode

---

## REFERENCES

**Best Practices:**
- File 10: Skill structure standards
- File 05: Progressive disclosure rationale
- Files 01-13: Complete skill design guide

**Related Tools:**
- `validate_skill.py`: Validate converted skill
- `quality_scorer.py`: Assess conversion quality
- `split_skill.py`: Further optimize if needed

**Script:** `/mnt/project/migration_helper.py` (~560 lines)

---

**Status:** âœ… Production-ready | **Version:** 1.0 | **Integration:** Agent-layer JSON output
