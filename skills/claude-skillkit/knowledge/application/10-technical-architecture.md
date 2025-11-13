---
title: "Technical Architecture Deep Dive: How Skills Actually Work"
purpose: "Detailed mechanics of progressive disclosure, runtime, and platform differences"
token_estimate: "2500"
read_priority: "medium"
read_when:
  - "User asking 'How does progressive disclosure work technically?'"
  - "User needs implementation details"
  - "Debugging loading issues"
  - "Understanding platform differences"
  - "Advanced implementation planning"
related_files:
  must_read_first:
    - "01-why-skills-exist.md"
    - "02-skills-vs-subagents-comparison.md"
  read_together:
    - "05-token-economics.md"
    - "06-platform-constraints.md"
  read_next:
    - "12-testing-and-validation.md"
avoid_reading_when:
  - "User just learning concepts (too technical)"
  - "User not implementing yet"
  - "Simple use case (unnecessary detail)"
last_updated: "2025-11-03"
---

# Technical Architecture Deep Dive: How Skills Actually Work

## I. PENDAHULUAN

**Scope:** Technical mechanics dari progressive disclosure, runtime environment, dan platform-specific implementation details.

**Prerequisites:** Basic understanding dari Skills concepts (`01-why-skills-exist.md`), Skills vs Subagents distinctions (`02-skills-vs-subagents-comparison.md`).

**What This Covers:** Step-by-step loading process, context window management, execution environment, platform differences (Claude.ai vs API vs Code).

**What This Does NOT Cover:** Platform limitations dan deployment challenges (see `06-platform-constraints.md`), security risks (see `07-security-concerns.md`).

---

## II. PROGRESSIVE DISCLOSURE MECHANICS

### A. Three-Level Loading Architecture

Progressive disclosure adalah prinsip design inti yang membuat Skills flexible dan scalable. Sistem bekerja melalui tiga level hierarkis:

| Level | Component | Size | When Loaded | Token Cost |
|-------|-----------|------|-------------|------------|
| **1** | Metadata (name, description) | ~100 tokens | Startup | Always |
| **2** | SKILL.md body | 800-3,000 tokens | When triggered | On-demand |
| **3** | Resources (docs, scripts) | Variable | When needed | Zero until used |

**Key Efficiency:** 50 skills = 5,000 tokens at startup. Scripts execute WITHOUT loading codeÃ¢â‚¬â€only output consumes tokens.

### B. Loading Process Flow

**Example:** User requests "Extract text from this PDF"

```
STARTUP: System prompt includes all skill descriptions (~5,000 tokens)
QUERY: Claude evaluates PDF Processing skill as relevant
LOAD: bash: read /mnt/skills/pdf-skill/SKILL.md (800 tokens)
DECISION: Form filling not needed Ã¢â€ â€™ FORMS.md NOT loaded (0 tokens)
EXECUTE: Uses SKILL.md guidance for task
```

**Total tokens:** 5,800 (startup + active skill) vs 150,000+ all-in-context approach.

### C. Context Window Management

**Context Allocation:**

| Component | Token Budget | Priority |
|-----------|--------------|----------|
| User conversation | 40,000-60,000 | Highest |
| Active skill instructions | 800-5,000 | High |
| Skill metadata (all) | ~5,000 | Medium |
| System prompt | 10,000-15,000 | Critical |

**Multi-Skill Coordination:** Each skill loads independently. When multiple skills active: Conversation + Skill A + Skill B + Skill C instructions share context window. Example: PDF (800) + Excel (1,200) + Word (1,000) = 3,000 tokens total.

### D. Optimization Techniques

**1. Metadata Engineering:**
```yaml
# BAD: Vague (triggers unnecessarily)
description: "Helps with files"

# GOOD: Specific (reduces false activation)
description: "Extract text/tables from PDFs, fill forms, merge documents"
```

**2. Reference File Splitting:**
```
skill/
  SKILL.md           # Core (800 tokens)
  ADVANCED.md        # Complex scenarios (load when needed)
  scripts/validate.py  # Execute, not load
```

**3. Script Output Minimization:**
```python
# BAD: Verbose (4 lines)
print(f"Processing: {filename}")
print(f"Extracting...")
print(f"Found {len(text)} chars")
print(f"Done!")

# GOOD: Essential only (1 line)
print(f"Extracted {len(text)} chars from {filename}")
```

---

## III. RUNTIME ENVIRONMENT

### A. Execution Container

**VM Specifications:**

| Specification | Value | Implication |
|---------------|-------|-------------|
| Container Type | Sandboxed VM | Isolated execution |
| Filesystem Access | Full `/home/claude` | Read/write capable |
| Code Execution | Python, Bash, Node.js | Multi-language |
| Network | Limited | See platform docs |
| Resource Limits | Platform-dependent | Varies |

**Filesystem Scope:**
- `/home/claude/` - Working directory (full access)
- `/mnt/skills/` - Skill files (read-only)
- `/mnt/user-data/uploads/` - User files (read-only)
- `/mnt/user-data/outputs/` - Output delivery (write access)

**Security Boundaries:** Skills CANNOT access other skills' files, modify system files, or access other conversations. **For security details, see:** `07-security-concerns.md`

### B. Tool Access & Permissions

**Permission Models:**

| Context | Permission Model | Inheritance |
|---------|------------------|-------------|
| **Skills** | Inherit from user | Yes - full tools available |
| **Subagents** | Explicitly granted | No - must specify each |

**Example:**
```yaml
# Skills automatically inherit ALL user tools
allowed-tools: [bash_tool, view, create_file]

# Subagents must list explicitly
subagent.tools = ["bash_tool", "web_search"]
```

### C. Code Execution

**Supported Languages:**

| Language | Execution | Package Mgmt | Use Cases |
|----------|-----------|--------------|-----------|
| Python | Native | pip, conda | Data, ML, APIs |
| Bash | Native | apt, brew | File ops, system |
| Node.js | Native | npm | Web scraping |

**Execution Pattern:**
```python
# Skills execute code WITHOUT loading to context
result = subprocess.run(['python', 'process.py'], capture_output=True)
print(result.stdout)  # Only output consumes tokens
```

### D. Network & External Access

| Platform | Web Access | API Calls | Rate Limits |
|----------|------------|-----------|-------------|
| Claude.ai | Via `web_search` | Yes | Platform limits |
| API | Via `web_search` | Yes | User/org limits |
| Claude Code | Direct network | Yes | None |

**For detailed constraints, see:** `06-platform-constraints.md` Section III

---

## IV. PLATFORM DIFFERENCES

### A. Claude.ai Web/Desktop

**Deployment:**
```
Settings Ã¢â€ â€™ Capabilities Ã¢â€ â€™ Skills Ã¢â€ â€™ Upload ZIP
Limit: 20 skills per user
```

| Feature | Specification |
|---------|---------------|
| Container | Sandboxed VM |
| Filesystem | `/home/claude` read/write |
| Code | Python, Bash, Node pre-installed |
| Network | `web_search` only |
| Updates | Manual re-upload required |

**Best Practices:** Keep Ã¢â€°Â¤20 skills, use progressive disclosure, version control via Git (manual sync).

### B. Claude API

**Deployment:**
```python
client = Anthropic(api_key="...")
skill = client.skills.create(
    name="my-skill",
    files=[("SKILL.md", content)]
)
```

| Feature | Specification |
|---------|---------------|
| Container | Sandboxed VM |
| Filesystem | `/mnt/skills/` read-only |
| Code | Full capabilities |
| Network | Full access |
| Updates | Programmatic `skills.update()` |

**API-Specific Features:**

**Programmatic Management:**
```python
skill = client.skills.create(...)       # Create
client.skills.update(skill_id, ...)     # Update
client.skills.delete(skill_id)          # Delete
skills = client.skills.list()           # List
```

**Dynamic Loading:**
```python
response = client.messages.create(
    skills=[skill.id],  # Reference by ID
    messages=[...]
)
```

**No 20-skill limit.** Metadata loaded per-conversation (not globally).

### C. Claude Code CLI

**Deployment:**
```bash
# Personal skills
~/.claude/skills/my-skill/SKILL.md

# Project skills
.claude/skills/my-skill/SKILL.md
```

| Feature | Specification |
|---------|---------------|
| Container | Direct filesystem (no sandbox) |
| Filesystem | Full system access |
| Code | Native execution all languages |
| Network | Full access unrestricted |
| Updates | Instant file editing |

**Unique Advantages:**

**1. Direct Editing:**
```bash
vim ~/.claude/skills/my-skill/SKILL.md  # Changes instant
```

**2. Git Integration:**
```bash
cd ~/.claude/skills/my-skill
git init && git commit -m "Initial"
```

**3. Project-Specific Skills:**
```
project/.claude/skills/  # Only available in this project
```

**Development Workflow:**
```bash
mkdir -p ~/.claude/skills/my-skill
vim ~/.claude/skills/my-skill/SKILL.md
claude chat "test skill"  # Test immediately
```

### D. Platform Selection Guide

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Individual productivity | Claude.ai/Desktop | Easy setup |
| Rapid development | Claude Code | Instant testing |
| Production | API | Scalability, control |
| Team collaboration | API + Git | Version control |
| Enterprise | API | Automation, security |

**Migration Paths:**

```
Claude.ai Ã¢â€ â€™ Claude Code: Export ZIP, unzip to ~/.claude/skills/
Claude Code Ã¢â€ â€™ API: Read SKILL.md, upload via client.skills.create()
API Ã¢â€ â€™ Claude.ai: Download files, create ZIP, upload via UI
```

---

## V. KEY TAKEAWAYS

**Progressive Disclosure Benefits:**

Three-level loading architecture (metadata â†’ SKILL.md â†’ resources) enables massive scalability without context window pressure. Unused skills cost zero tokens at runtime. Scripts execute without loading codeâ€”only output consumes tokens. This design allows unlimited skill installations with minimal startup overhead.

**Platform-Aware Design:**

Core architecture remains consistent: progressive disclosure, SKILL.md structure, YAML frontmatter work identically across platforms. Platform differences affect deployment onlyâ€”not skill design. Choose based on needs: Claude.ai for individual productivity, API for programmatic control and scale, Claude Code for rapid development and Git workflows.

**Next Steps:**

Implementation guidance â†’ `12-testing-and-validation.md` for testing methodology. Token optimization â†’ `05-token-economics.md` for efficiency patterns. Platform constraints â†’ `06-platform-constraints.md` for deployment limits. Security boundaries â†’ `07-security-concerns.md` for risk assessment.

---

**End of File 10**
