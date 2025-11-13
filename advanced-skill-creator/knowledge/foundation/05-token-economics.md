---
title: "Token Economics: Cost Analysis Skills vs Subagents"
purpose: "Understanding cost implications dan optimization strategies"
token_estimate: "2500"
read_priority: "high"
read_when:
  - "User asking about costs"
  - "User asking 'How much will this cost?'"
  - "Budget planning"
  - "ROI calculation needed"
  - "Optimizing existing implementation"
  - "Comparing cost of approaches"
related_files:
  must_read_first:
    - "02-skills-vs-subagents-comparison.md"
  read_together:
    - "04-hybrid-patterns.md"
  read_next: []
avoid_reading_when:
  - "User not concerned with costs"
  - "Cost not decision factor"
  - "Just exploring concepts"
last_updated: "2025-11-01"
---

# Token Economics: Cost Analysis Skills vs Subagents

## I. PENDAHULUAN

Token efficiency adalah foundational advantage Skills vs traditional approaches. Understanding token economics critical untuk budget planning, architecture decisions, dan cost optimization strategies.

**Key Insight:** Skills use progressive disclosure untuk extreme efficiency (30-50 tokens overhead). Subagents use dedicated context windows (15Ã— token multiplier). Neither approach inherently "expensive" - appropriateness depends on use case frequency dan value.

**Pricing Context (Claude Sonnet 4.5):**
- Input: $3 per million tokens
- Output: $15 per million tokens

**For architectural differences, see:** `02-skills-vs-subagents-comparison.md`

---

## II. SKILLS TOKEN MODEL

### A. Progressive Disclosure Architecture (3 Levels)

**Level 1 - Metadata (Always Loaded):**
- Content: YAML frontmatter (name + description)
- Token Cost: ~50 tokens per skill
- When: Startup, every conversation
- Purpose: Enable automatic discovery

**Level 2 - Instructions (Triggered Loading):**
- Content: Full SKILL.md body
- Token Cost: <5,000 tokens (typically 800-2,800)
- When: Skill determined relevant
- Mechanism: `bash: read skill-name/SKILL.md`

**Level 3+ - Resources (On-Demand):**
- Content: References, documentation, datasets
- Token Cost: 0 until accessed
- When: Explicitly needed
- Critical: Scripts execute WITHOUT loading contents - only output costs tokens

### B. Token Efficiency Breakdown

**Idle State (Skills Installed, Not Used):**
```
50 skills installed
Each: ~50 tokens metadata
Total overhead: 2,500 tokens
Cost: $0.0075 per conversation
```

**Active State (Skill Triggered):**
```
Metadata: 50 tokens
SKILL.md body: 800 tokens
Total: 850 tokens
Cost: $0.00255 per use
```

**Heavy Usage (With References):**
```
Metadata: 50 tokens
SKILL.md: 800 tokens
Reference file: 1,200 tokens
Total: 2,050 tokens
Cost: $0.00615 per use
```

### C. Real-World Example: PDF Processing Skill

**Startup Loading:**
- Description: "Extract text from PDFs, fill forms, merge documents"
- Tokens: 50
- Impact: Every conversation

**User Request:** "Extract text from this PDF"

**Skill Activation:**
- Read SKILL.md: 800 tokens
- Determines form filling NOT needed â†’ FORMS.md: 0 tokens (not accessed)
- Execute extraction script output: ~200 tokens
- Total: 1,050 tokens

**Cost Calculation:**
- Input tokens: 850 (metadata + SKILL.md)
- Output tokens: 200 (extraction results)
- Cost: (850 Ã— $3/M) + (200 Ã— $15/M) = $0.00255 + $0.003 = $0.00555

### D. Scaling Characteristics

**Installing Many Skills:**
- 10 skills: ~500 tokens overhead
- 50 skills: ~2,500 tokens overhead
- 100 skills: ~5,000 tokens overhead
- Cost negligible until triggered

**Key Advantage:** Unlimited bundled content (references, documentation, examples) with ZERO token penalty until accessed. Can include comprehensive materials without context window impact.

**For optimization strategies combining multiple skills, see:** `04-hybrid-patterns.md`

---

## III. SUBAGENTS TOKEN MODEL

### A. Full Context Architecture

**Dedicated Context Window:**
Subagents operate dengan separate, isolated context window containing:
- Complete system prompt (1,500-3,000 tokens)
- Full conversation history with subagent
- All intermediate steps dan reasoning
- Final output synthesis

**No Progressive Disclosure:** Unlike Skills, subagents load entire context immediately. All instructions present throughout conversation.

### B. Token Consumption Breakdown

**Single Subagent Invocation:**
```
System prompt: 2,000 tokens
User query: 100 tokens
Subagent reasoning: 500 tokens (multiple turns)
Intermediate steps: 1,500 tokens
Final output: 300 tokens
Conversation history: 2,000 tokens
Total: ~6,400 tokens per invocation
```

**Cost Calculation:**
- Input: 6,100 tokens Ã— $3/M = $0.0183
- Output: 300 tokens Ã— $15/M = $0.0045
- Total: ~$0.023 per invocation

### C. Multi-Agent Multiplier Effect

**Critical Finding:** Multi-agent systems use approximately **15Ã— more tokens** than single conversations.

**Why 15Ã— Multiplier:**
1. Each agent: Dedicated context window
2. Orchestration overhead: Agent coordination
3. Context sharing: Information passed between agents
4. Synthesis: Combining outputs
5. Iteration: Multi-turn agent interactions

**Example: 3-Agent System**
```
Main conversation: 2,000 tokens
Agent A context: 5,000 tokens
Agent B context: 4,500 tokens
Agent C context: 4,000 tokens
Orchestration: 1,500 tokens
Synthesis: 1,000 tokens
Total: ~18,000 tokens (9Ã— single conversation)
```

**When 15Ã— Justified:**
- Complex, high-value workflows
- Infrequent operations (not every conversation)
- Quality improvement outweighs cost
- Validated: Anthropic research shows 90.2% performance improvement Opus 4 + Sonnet 4 subagents

### D. Cost-Benefit Analysis

**Subagent Strengths:**
- Isolated context prevents pollution
- Specialized expertise per agent
- Parallel processing capability
- Superior untuk multi-step reasoning

**Cost Reality:**
- 7-15Ã— more expensive than Skills
- Justified untuk complex workflows
- NOT appropriate untuk frequent, simple tasks
- Use Skills untuk utilities, Subagents untuk orchestration

**Validated Example:** Subagent system prompt reduced 65% (803â†’281 lines) dengan zero functionality lost by extracting templates to Skills.

**For decision framework, see:** `03-skills-vs-subagents-decision-tree.md`

---

## IV. COST COMPARISON SCENARIOS

**Comparison Table: Skills vs Subagents vs Hybrid**

| Scenario | Frequency | Skills Cost/Use | Subagents Cost/Use | Monthly Cost (Skills) | Monthly Cost (Subagents) | Winner | Key Reason |
|----------|-----------|-----------------|--------------------|-----------------------|--------------------------|--------|------------|
| **Brand Guidelines** (Apply standards to docs) | 100Ã—/month | $0.00255 (850t) | $0.015 (5,000t) | $0.26 | $1.50 | Skills | 83% savings, frequent simple task |
| **Security Audit** (Multi-stage analysis) | 5Ã—/month | $0.012 (4,000t) | $0.024 (8,000t) | $0.06 | $0.12 | Subagent | Multi-step reasoning, quality justified |
| **Data Pipeline** (Extract, transform, analyze) | 50Ã—/month | N/A (cannot orchestrate) | $0.03 (10,000t) | N/A | $1.50 | **Hybrid: $1.10** | Subagent (6kt) + Skills (1.4kt) = 7.4kt optimal |
| **Document Processing** (PDF to Excel at scale) | 1,000Ã—/month | $0.00255 (850t) | $0.015 (5,000t) | $2.55 | $15.00 | Skills | 83% savings at scale |

**Key Insights:**
- Frequent simple tasks â†’ Skills (80%+ cost savings)
- Infrequent complex workflows â†’ Subagents (capability justifies cost)
- Moderate complexity â†’ Hybrid (optimizes both capability AND efficiency)

**For hybrid implementation patterns, see:** `04-hybrid-patterns.md`

---

## V. OPTIMIZATION STRATEGIES

### Architecture Optimization

**1. Tiered Model Architecture**
Use Opus 4 for orchestration + Sonnet 4.5 subagents for execution. Research validated: 40-60% cost reduction while maintaining quality.

**2. Hybrid Pattern**
Subagents orchestrate workflows, Skills provide utilities. Best balance of capability and cost.

### Skills Optimization

**3. Extract Duplication to Skills**
Move common templates/knowledge from subagent prompts to Skills. Real validation: Subagent reduced 65% (803â†’281 lines) with zero functionality lost.

**4. Progressive Loading**
Structure Skills dengan granular references. Load only necessary sections. Avoid loading unused documentation.

### Routing Optimization

**5. Frequency-Based Routing**
Frequent tasks â†’ Skills. Infrequent, complex tasks â†’ Subagents. Use conditional invocation pattern for dynamic routing.

**6. Batch Processing**
Group similar tasks to amortize subagent context setup costs. Single subagent invocation handles multiple items.

### Monitoring & Iteration

**7. Track Actual Usage**
Monitor real token consumption. Optimize based on measured costs, not assumptions. Premature optimization wastes time - iterate based on data.

**For conditional invocation pattern, see:** `04-hybrid-patterns.md` (Pattern 3)

---

## WHEN TO READ NEXT

**For Implementation:**
- Hybrid patterns â†’ `04-hybrid-patterns.md`
- Platform limits â†’ `06-platform-constraints.md`

**For Decision Making:**
- Should I use Skills or Subagents? â†’ `03-skills-vs-subagents-decision-tree.md`
- Conceptual differences â†’ `02-skills-vs-subagents-comparison.md`

**For Strategic Context:**
- Why Skills exist â†’ `01-why-skills-exist.md`
- Real-world validation â†’ `case-studies.md`

---

**FILE END - Estimated Token Count: ~2,500 tokens (~218 lines)**
