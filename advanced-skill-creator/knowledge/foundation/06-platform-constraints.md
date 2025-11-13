---
title: "Platform Constraints & Technical Limitations"
purpose: "Understanding technical limitations dan workarounds"
token_estimate: "2000"
read_priority: "medium"
read_when:
  - "User asking 'Can Skills do X?'"
  - "Troubleshooting deployment issues"
  - "Enterprise planning"
  - "Team coordination questions"
  - "Platform compatibility questions"
related_files:
  must_read_first:
    - "01-why-skills-exist.md"
  read_together:
    - "07-security-concerns.md"
  read_next:
    - "08-when-not-to-use-skills.md"
avoid_reading_when:
  - "User just learning concepts"
  - "Not yet implementing"
  - "Personal use only (not team)"
last_updated: "2025-11-01"
---

# Platform Constraints & Technical Limitations

## I. PENDAHULUAN

Skills provide powerful extensibility but come with platform-specific constraints dan technical limitations yang must be understood untuk successful deployment, especially dalam enterprise contexts.

**Critical Dependencies:** Filesystem access (absolute requirement), Code execution environment (cannot function without), Platform-specific deployment methods (varies by Claude.ai/API/Code).

**Why This Matters:** Understanding limitations prevents unrealistic expectations, enables informed architecture decisions, dan helps plan workarounds untuk deployment challenges.

**This file addresses practical constraints. For security risks, see:** `07-security-concerns.md`

---

## II. DEPLOYMENT LIMITATIONS

### A. User Skills Only (No Organization-Wide Deployment)

**Current State (as of October 2025):** Custom skills are private to individual user accounts. No organization-wide deployment mechanism exists yet.

**Platform-Specific Methods:**

| Platform | Upload Method | Limit | Sharing |
|----------|---------------|-------|---------|
| Claude.ai/Desktop | Settings â†’ Capabilities â†’ Skills â†’ Upload ZIP | 20 per user | Manual each user |
| Claude Code | Copy to `~/.claude/skills/` (personal) or `.claude/skills/` (project) | Unlimited | Git repository |
| API | `client.skills.create()` programmatic upload | Unlimited | Skill ID references |

**Enterprise Impact:** Teams of 10+ people require significant manual coordination. Version drift common without strict processes. Each team member must upload skills separately.

### B. Manual Distribution (No Centralized Marketplace)

**Distribution Methods Table:**

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| Git Repository | Team collaboration | Version control, auditability | Manual install still required |
| ZIP Files | Simple sharing | Easy distribution | No version tracking, no dependencies |
| Internal Portal | Large organizations | Centralized access | Still requires manual user action |

**Official Anthropic Skills:** Only 4 pre-built skills available (PowerPoint, Excel, Word, PDF), automatically enabled. Community skills: None officially curated yet.

**Marketplace Status:** No official Skills marketplace exists (as of October 2025). Enterprise-wide deployment capabilities listed as "coming soon" but not ready. Timeline unknown.

### C. Enterprise Deployment Challenges

**Key Problems:**

**Version Control:** No automated update mechanism. Teams must coordinate versions manually. Testing updates across team required. Rollback: Manual only.

**Governance:** No approval workflows, no audit trails for skill usage, no centralized management console. Compliance tracking: Custom solutions needed.

**Support:** No official debugging tools, limited error reporting. Troubleshooting requires technical expertise.

**For context on official skills, see:** `01-why-skills-exist.md`

---

## III. TECHNICAL CONSTRAINTS

### A. Absolute Filesystem Dependency

**Core Requirement:** Skills REQUIRE filesystem access and code execution capabilities. Won't work without these features enabled.

**Platform Availability:**

| Platform | Filesystem | Code Execution | Skills Support |
|----------|------------|----------------|----------------|
| Claude.ai (Paid) | Yes | Yes | Full |
| Claude Desktop | Yes | Yes | Full |
| Claude Code CLI | Yes | Yes | Full |
| API (with betas) | Sandboxed | Sandboxed | Full |
| Claude.ai (Free) | No | No | NONE |
| Mobile Apps | Limited | No | NONE |

**Critical Distinction:** Biggest difference from previous approaches like MCP or ChatGPT Plugins which don't require code execution infrastructure.

### B. Platform-Specific Differences

**Comprehensive Comparison: Claude.ai vs API vs Code**

| Feature | Claude.ai/Desktop | Claude Code CLI | Anthropic API |
|---------|-------------------|-----------------|---------------|
| **Format** | ZIP file | Folder structure | ZIP file |
| **Skill Limit** | 20 per user | Unlimited | Unlimited |
| **Distribution** | Manual upload | Git/filesystem | Programmatic |
| **Network (Scripts)** | Yes (npm/PyPI install) | Yes | NO (sandboxed) |
| **External APIs** | Accessible | Accessible | NOT accessible |
| **Runtime Packages** | Install dynamically | Install dynamically | Pre-installed only |
| **Sharing** | Manual per user | Git repository | Skill ID refs |

**Critical API Limitation:** NO network access from code execution container. Cannot install packages at runtime. Only pre-installed packages available. Cannot access external APIs directly.

**Impact:** API deployments require pre-packaging ALL dependencies. Cannot dynamically fetch data during execution.

**For tool security boundaries with Subagents, see:** `02-skills-vs-subagents-comparison.md`

### C. Sandboxed Execution Environment

**Security Container:** All Skills run in sandboxed environment with restricted permissions.

**Default Restrictions:** No access to user's local filesystem (outside container), no system resources, no privileged operations, no persistent storage between conversations.

**Tool Permissions:** Use `allowed-tools` in YAML to restrict:

```yaml
allowed-tools: "Read,Write,Bash(git:*)"
# Allows: Read, Write, git commands only
# Blocks: other Bash commands
```

**Resource Limits:** Memory limited (exact limits undocumented), CPU shared, execution timeouts exist (not publicly specified), large files may cause issues.

---

## IV. EXECUTION LIMITATIONS

### A. Discovery and Triggering Issues

**LLM-Based Routing:** Skills use pure LLM-based discovery (no algorithmic selection). Claude evaluates skill descriptions against conversation context.

**Common Problems:**

**Vague Descriptions Prevent Activation:**
```yaml
# BAD (won't trigger reliably)
description: "Helps with documents"

# GOOD (clear triggers)
description: "Convert PDF files to Excel spreadsheets. Use when user mentions PDF conversion or Excel export"
```

**Phrasing Mismatch:** User says "Transform PDF to spreadsheet" but skill description says "Convert documents to XLSX" â†’ May not trigger.

**Solution:** Use multiple synonyms in description: "Convert, transform, export, change PDF files to Excel, XLSX, spreadsheet format"

**Balancing Act:** Descriptions must be specific enough to prevent false positives, broad enough to catch valid use cases.

### B. Script Best Practices

**Execution Model:** Scripts execute via bash. Output only (not code contents) consumes tokens.

**Key Practices:**

**1. Error Handling:**
```python
try:
    result = process_data(input_file)
    print(json.dumps({"status": "success", "result": result}))
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}))
```

**2. Structured Output:**
```python
# GOOD: JSON (easy parsing)
print(json.dumps({"findings": [...], "summary": "..."}))

# BAD: Unstructured text
print("Found some issues... maybe check line 45...")
```

**API Constraint:** Remember sandboxed environment - no external network calls from scripts.

### C. Resource and Performance Considerations

**Observed Limits:** Single script execution ~5-10 minutes timeout. Memory sufficient for typical tasks, issues with large datasets (>1GB). Large files (>100MB) may be slow.

**Optimization:** Use progressive disclosure effectively. Keep SKILL.md lean, move heavy content to references.

**For token optimization strategies, see:** `05-token-economics.md`

---

## V. WORKAROUNDS SUMMARY

**Key Solutions for Major Limitations:**

| Problem | Workaround |
|---------|------------|
| No org-wide deployment | Git repository + installation docs. Create setup scripts. |
| No marketplace | Internal skills library (Git). Curated collection with README. |
| Version synchronization | Semantic versioning in metadata. Team communication channel. Testing protocols. |
| API no network | Pre-package all data. Use main conversation to fetch external data (Claude web tools), pass to skill. |
| Discovery unreliable | Engineer descriptions with multiple synonyms. Test various phrasings. Include explicit triggers. |
| Platform differences | Document platform-specific behavior. Test on target platform. Provide platform instructions. |
| No governance | Internal approval process. Code review for all skills. Security audit checklist. |
| Resource limits | Split operations into chunks. Process incrementally. Use streaming where possible. |

**For enterprise adoption strategies, see:** `adoption-strategy.md` (when available)

---

## WHEN TO READ NEXT

**For Security Concerns:**
- Security risks and mitigations â†’ `07-security-concerns.md`

**For Decision Making:**
- When NOT to use Skills â†’ `08-when-not-to-use-skills.md`
- Should I use Skills or Subagents? â†’ `03-skills-vs-subagents-decision-tree.md`

**For Implementation:**
- Token optimization â†’ `05-token-economics.md`
- Hybrid patterns â†’ `04-hybrid-patterns.md`

**For Strategic Context:**
- Why Skills exist â†’ `01-why-skills-exist.md`

---

**FILE END - Estimated Token Count: ~2,000 tokens (~236 lines)**
