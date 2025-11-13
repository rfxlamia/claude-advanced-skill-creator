---
title: "Skills vs Subagents: Perbedaan Konseptual"
purpose: "Fundamental understanding of Skills vs Subagents differences"
token_estimate: "2400"
read_priority: "critical"
read_when:
  - "User confused about Skills vs Subagents"
  - "User asking 'What's the difference?'"
  - "Before reading decision tree"
  - "Comparing approaches"
  - "Understanding architecture"
related_files:
  must_read_first:
    - "01-why-skills-exist.md"
  read_together:
    - "03-skills-vs-subagents-decision-tree.md"
  read_next:
    - "04-hybrid-patterns.md"
    - "05-token-economics.md"
avoid_reading_when:
  - "User already understands distinction clearly"
  - "User only needs decision guidance (skip to 03-decision-tree)"
  - "User asking about costs only (skip to 05-token-economics)"
last_updated: "2025-10-31"
---

# Skills vs Subagents: Perbedaan Konseptual

## I. PENDAHULUAN

Skills dan Subagents adalah dua mekanisme ekstensibilitas yang fundamentally different, melayani purposes yang distinct. Understanding kapan use each adalah critical untuk building effective AI workflows.

**Core Distinction:**
- **Skills** = Modular capability packages (instructions + resources)
- **Subagents** = Pre-configured AI personalities (specialized workers)

**Key Insight:** Ini bukan either/or choice. Most powerful workflows use BOTH - Skills untuk utilities, Subagents untuk orchestration.

**This file addresses conceptual differences. For decision guidance, see:** `03-skills-vs-subagents-decision-tree.md`

---

## II. SKILLS: INSTRUKSI "HOW-TO"

### Definisi dan Structure

**Claude Skills** adalah modular, reusable capability packages containing instructions, scripts, dan resources.

**Structure:** Folder dengan SKILL.md file (YAML frontmatter + markdown body), plus optional scripts, references, assets.

**Primary Function:** Extend Claude's knowledge dengan procedural "how-to" information.

### Mental Model: Recipe Cards

Think of Skills seperti recipe cards dalam cookbook:
- Each card contains specific instructions
- Pull out card when needed
- Multiple cards can be used together
- Instructions stay same, execution adapts to context

### 6 Karakteristik Utama

**1. Automatic Discovery**
Claude evaluates all skill descriptions against conversation context dan loads relevant skills automatically. NO explicit user command needed.

**2. Shared Context Window**
Skills pull necessary information ke current chat. Act as quick add-ons untuk single tasks. NO separate context window.

**3. Progressive Disclosure**
- Level 1: Metadata always loaded (30-50 tokens)
- Level 2: SKILL.md loaded when triggered
- Level 3: References loaded on-demand
- Extreme token efficiency

**4. Procedural Knowledge Focus**
"How-to" instructions, domain-specific procedures, organizational standards, templates dan formats.

**5. Composability**
Multiple skills can be loaded simultaneously dan stack together seamlessly. Reusable across different contexts.

**6. Tool Access Inheritance**
Uses main Claude's tools. All tools available yang diberikan ke main conversation.

### Best Use Cases

**Single, Well-Defined Tasks:**
- File conversions (PDF to Excel)
- Template applications (brand guidelines)
- Domain knowledge reference (API docs)
- Utility functions (validation, transformation)

**Examples:** Brand guidelines enforcement, code style guides, financial modeling procedures, document processing.

**For detailed patterns, see:** `references/workflows.md`

---

## III. SUBAGENTS: AI WORKER

### Definisi dan Structure

**Claude Subagents** adalah pre-configured AI personalities dengan specialized system prompts.

**Structure:** Markdown file dengan YAML frontmatter defining role, tools, system prompt, optional skill invocations.

**Primary Function:** Handle complex, multi-step workflows requiring dedicated focus.

### Mental Model: Specialist Team Members

Think of Subagents seperti specialist team members:
- Each expert has specialized role
- Works independently dengan own workspace
- Can be called explicitly atau delegate automatically
- Returns results when done

### 6 Karakteristik Utama

**1. Dual Invocation Pattern**
Automatic delegation (Claude spawns specialized agents) OR explicit invocation ("@agent-name" atau "Use the X subagent"). User has direct control.

**2. Isolated Context Window**
Operates dalam separate, dedicated context window. Complete isolation prevents "context pollution". Can focus entirely pada specific task.

**3. Specialized Personality**
Pre-configured role dan expertise. Domain-specific system prompts. Consistent behavior patterns.

**4. Multi-Step Workflow Capability**
Handles complex sequences dengan decision points, multiple queries dan synthesis, iterative hypothesis testing.

**5. Restricted Tool Permissions**
Can have specific tool permissions. Example: code-reviewer gets Read/Grep/Glob only, NO Write/Edit. Security boundaries maintained.

**6. Higher Token Consumption**
Dedicated context per agent. Multi-agent systems use approximately 15x more tokens. Justified untuk high-value complex tasks.

### Best Use Cases

**Complex, Multi-Step Workflows:**
- Code review processes dengan multiple stages
- Data analysis requiring multiple queries dan synthesis
- Debugging dengan iterative hypothesis testing
- Security audits dengan comprehensive checks

**Examples:** zahtevki-researcher (downloads attachments, analyzes, compares), code reviewer (multiple validation passes), security auditor (comprehensive scanning).

**For orchestration patterns, see:** `04-hybrid-patterns.md`

---

## IV. COMPARISON MATRIX

### Core Differences Table

| Dimension | Skills | Subagents |
|-----------|--------|-----------|
| **Mental Model** | Recipe cards, plugins | Team members, consultants |
| **Context Window** | Shared main context | Separate isolated context |
| **Invocation** | Automatic only | Automatic AND explicit |
| **Token Overhead** | 30-50 tokens until used | 15x full conversations |
| **Best For** | Single tasks, utilities | Multi-step workflows |
| **Tool Access** | Inherits all main tools | Can be restricted |
| **Composability** | Stack multiple skills | Coordinate multiple agents |
| **Control** | Automatic discovery | Explicit or automatic |

### Invocation Pattern Examples

**Skills Invocation:**
```
User: "Convert this PDF to Excel"
[Claude evaluates skill descriptions]
[pdf-processing skill automatically loaded]
[Task completed in main conversation]
```

**Subagents Invocation:**
```
User: "Review this codebase for security issues"
[Claude recognizes complex multi-step task]
[Spawns security-reviewer subagent]
[Subagent works in isolated context]
[Returns comprehensive report]
```

### Token Efficiency Comparison

**Skills Example:**
- Metadata: 50 tokens
- SKILL.md when triggered: 800 tokens
- **Total: 850 tokens**

**Subagent Example:**
- Full system prompt: 2,000 tokens
- Conversation history: 3,000 tokens
- Analysis output: 2,000 tokens
- **Total: 7,000 tokens (8.2x more)**

Multi-agent systems use approximately 15x more tokens than single conversations. Justified untuk complex, high-value tasks.

**For detailed token economics, see:** `05-token-economics.md`

### Tool Access Comparison

**Skills:** Uses all tools available ke main Claude. NO independent tool restrictions. Inherits permissions automatically.

**Subagents:** Can have specific tool permissions (e.g., code-reviewer restricted to Read/Grep/Glob only). Security boundaries maintained.

**Security Implication:** Subagents provide tool isolation - skills do not. Choose subagent when tool restrictions needed.

### Use Case Decision Reference

| Use Case Type | Recommended | Reasoning |
|---------------|-------------|-----------|
| File conversion | Skill | Single task, utility |
| Code review | Subagent | Multi-step analysis |
| Brand guidelines | Skill | Standards reference |
| Security audit | Subagent | Complex workflow |
| Data transformation | Skill | Deterministic utility |
| Exploratory analysis | Subagent | Iterative reasoning |
| API documentation | Skill | Reference knowledge |
| Debugging session | Subagent | Multi-step investigation |

### Maintenance Differences

**Skills:** Update SKILL.md instructions, add/modify scripts, version control straightforward, reusable across contexts, easier to maintain (smaller scope).

**Subagents:** Update system prompts, modify role definitions, test behavior extensively, context-specific tuning, more complex (broader scope).

**Real Example:** Subagent reduced dari 803 lines ke 281 lines (65% reduction) dengan extracting templates ke separate skill file. Skills enable subagent efficiency.

### Performance Validation

**Skills:** Fast invocation, minimal overhead, scales well (50+ skills manageable), consistent behavior.

**Subagents:** Anthropic research shows Claude Opus 4 + Sonnet 4 subagents outperforms single-agent Opus 4 by **90.2%** pada complex research tasks. Higher token cost justified by capability.

---

## V. KEY TAKEAWAYS

### Simple Rule of Thumb

**Start dengan Skill unless you specifically need Subagent features.**

Skills simpler, faster, dan easier to maintain. Upgrade ke Subagent when you're doing actual workflows dengan multiple steps, decision points, dan validation loops.

**For detailed decision framework with scoring system, see:** `03-skills-vs-subagents-decision-tree.md`

### They Work Together (Not Either/Or)

Skills dan Subagents are designed to work together dan highly complementary.

**The Hybrid Pattern:**
- Subagent handles complex workflow dan orchestration
- Skill handles utility functions
- Clean separation of concerns
- Reusable components

**Example:** zahtevki-researcher subagent downloads ticket attachment, invokes document-reader skill untuk convert ke text, continues analysis.

**For hybrid implementation patterns, see:** `04-hybrid-patterns.md`

### Cost vs Capability Trade-off

**Skills:** Very cost-efficient (30-50 tokens overhead). Best for frequent, lightweight tasks. Scale well.

**Subagents:** Higher cost (15x token multiplier). Justified untuk complex, high-value tasks. Best for infrequent, critical workflows.

**Optimization Strategy:** Use Skills untuk reduce duplication across subagents. Extract common templates ke skills. Subagents invoke skills untuk utilities.

**Validated Result:** Subagent system prompt reduced 65% (803â†’281 lines) dengan zero functionality lost.

### When to Choose Each

**Choose Skills When:**
- Repeatable workflows you've figured out
- Tasks requiring organizational standards
- Building blocks reusable across contexts
- Token efficiency critical

**Choose Subagents When:**
- Complex multi-step workflows dengan decision points
- Specialized domain expertise requiring dedicated focus
- Tasks that would clutter main conversation
- Isolated context required

**Choose Both (Hybrid) When:**
- Complex orchestration + reusable utilities
- Multiple specialized agents sharing common functions
- Cost optimization without sacrificing capability

---

## WHEN TO READ NEXT

**For Decision Making:**
- Need decision framework? â†’ `03-skills-vs-subagents-decision-tree.md`
- Want hybrid patterns? â†’ `04-hybrid-patterns.md`

**For Cost Analysis:**
- Token economics details â†’ `05-token-economics.md`

**For Implementation:**
- Technical architecture â†’ `technical-architecture.md`
- Platform constraints â†’ `06-platform-constraints.md`
- Security concerns â†’ `07-security-concerns.md`

**If Clear on Differences:**
- Skip to decision tree â†’ `03-skills-vs-subagents-decision-tree.md`

---

**FILE END - Estimated Token Count: ~2,400 tokens (~335 lines)**
