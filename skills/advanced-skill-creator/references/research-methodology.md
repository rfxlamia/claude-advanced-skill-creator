---
title: Research Methodology dengan Verbalized Sampling
purpose: Multi-angle domain research using VS for comprehensive understanding
usage: Loaded during Step 1c of Full Creation Workflow
version: 1.0.0
author: Advanced Skill Creator
---

# Research Methodology: Verbalized Sampling Strategy

**Context:** Step 1c - Research Domain dalam skill creation workflow

**Purpose:** Generate dan execute diverse research strategies untuk memahami domain secara comprehensive menggunakan Verbalized Sampling (VS)

**Key Benefits:**
- ðŸŽ¯ **1.6-2.1Ã— diversity gain** vs standard research
- ðŸ” Explores non-obvious valuable angles (tail sampling p<0.10)
- ðŸ“Š Probability-weighted strategy selection
- âš¡ Research-backed skill proposals (bukan assumptions)

---

## ðŸŽ¯ When to Use This Methodology

### ALWAYS Offer Research When:
- âœ… Domain unfamiliar to Claude (tidak ada dalam pre-training knowledge)
- âœ… User requirements vague atau minimal (<50 words description)
- âœ… Domain dengan rapid change (social media, AI tools, trends)
- âœ… Security-sensitive atau complex domains
- âœ… User explicitly requests comprehensive understanding

### MAY Skip Research When:
- âš ï¸ Domain standard dan familiar (PDF processing, markdown formatting)
- âš ï¸ User provides detailed specification (>200 words with clear structure)
- âš ï¸ User explicitly says "I know exactly what I need, skip research"

**Default stance:** ALWAYS OFFER research - let user decide

---

## ðŸ”¬ VS Research Strategy Generation

### Phase 1: Generate Diverse Research Strategies (INTERNAL)

**VS Prompt Template (Agent-Layer Only):**

```markdown
INTERNAL REASONING TASK:

Using Verbalized Sampling methodology, generate 5 diverse research query 
strategies for understanding [DOMAIN] skill creation.

Context:
- User wants to create skill for: [USER_TASK_DESCRIPTION]
- Domain appears: [familiar/unfamiliar/partially_known]
- User requirements clarity: [vague/moderate/detailed]

Instructions:
1. Sample from FULL distribution including non-obvious angles (p<0.15 acceptable)
2. Each strategy should explore DIFFERENT aspects
3. Estimate probability based on research value and relevance
4. Provide rationale using Chain-of-Thought reasoning

Required Aspects to Cover:
1. **Technical Implementation** (~p=0.30)
   - Standards, patterns, APIs, protocols
   - Common technical approaches and architectures
   - Best practices for implementation
   
2. **User Experience** (~p=0.25)
   - User pain points and workflows
   - Quality criteria users expect
   - Common user journeys and scenarios
   
3. **Competitive Analysis** (~p=0.20)
   - Existing tools and their approaches
   - Gaps in current solutions
   - Differentiation opportunities
   
4. **Edge Cases & Limitations** (~p=0.15)
   - Failure modes to anticipate
   - Platform-specific constraints
   - Non-obvious challenges
   
5. **Innovation & Trends** (~p=0.10)
   - Emerging trends in domain
   - Novel approaches worth exploring
   - Future-proofing considerations

Output Format (JSON):
```json
{
  "domain": "[DOMAIN]",
  "task_context": "[USER_TASK_DESCRIPTION]",
  "strategies": [
    {
      "id": 1,
      "query": "specific web_search query (3-6 words optimal)",
      "probability": 0.XX,
      "aspect": "technical|user|competitive|edge|innovation",
      "rationale": "Chain-of-thought: Why this angle is valuable for [DOMAIN]. What insights it will provide. How it aligns with user needs.",
      "expected_insights": "What we expect to learn from this search"
    }
  ],
  "metadata": {
    "total_probability": 1.0,
    "diversity_score": "high|medium|low",
    "tail_inclusion": "count of strategies with p<0.15"
  }
}
```

Constraints:
- Probabilities MUST sum to ~1.0 (Â±0.05 acceptable)
- Queries optimized for web_search (3-6 words)
- Include current year (2025) for trend-dependent searches
- Favor diverse angles over redundant queries
- At least 1 tail strategy (p<0.15) for non-obvious insights
```

**Implementation Note:** This is INTERNAL prompt - user doesn't see this. Claude executes this reasoning internally to generate strategies.

---

### Phase 2: Strategy Execution (Top-N Selection)

**Execution Rules:**

```python
# Pseudo-code for execution logic
def execute_research_strategies(strategies):
    """
    Execute top strategies based on probability and time budget
    """
    # Sort by probability (highest first)
    sorted_strategies = sort(strategies, key='probability', reverse=True)
    
    # Execution rules
    to_execute = []
    
    # Always execute top 3
    to_execute.extend(sorted_strategies[0:3])
    
    # Execute 4th if p > 0.10 (meaningful probability)
    if len(sorted_strategies) >= 4 and sorted_strategies[3]['probability'] > 0.10:
        to_execute.append(sorted_strategies[3])
    
    # Execute 5th if p > 0.12 AND time allows (optional)
    if len(sorted_strategies) >= 5 and sorted_strategies[4]['probability'] > 0.12:
        to_execute.append(sorted_strategies[4])
    
    # Time budget: ~2-3 minutes total
    # Typical: 3-4 web_search calls
    
    return to_execute
```

**Execution Pattern:**

```bash
# Strategy 1 (Highest p - usually technical)
web_search(strategy_1.query)
# Expected: Technical standards, implementation patterns

# Strategy 2 (User-centric)
web_search(strategy_2.query)
# Expected: User pain points, workflow patterns

# Strategy 3 (Competitive/edge cases)
web_search(strategy_3.query)
# Expected: Existing solutions, gaps, opportunities

# Strategy 4 (If p>0.10 - innovation/trends)
if strategy_4.probability > 0.10:
    web_search(strategy_4.query)
    # Expected: Emerging trends, novel approaches
```

**Quality Check During Execution:**
- âš ï¸ If search returns insufficient results â†’ reformulate query
- âš ï¸ If results too generic â†’ add domain-specific terms
- âš ï¸ If aspect already well-covered â†’ skip redundant search

---

## ðŸ“Š Findings Synthesis & Organization

### Synthesis Framework

**Organize findings by 5 core aspects:**

```markdown
## ðŸ“Š RESEARCH FINDINGS SUMMARY

### Context
Domain: [DOMAIN]
Strategies Executed: [3-4 strategies]
Total Sources Reviewed: [count]
Research Time: [~2-3 minutes]

---

### âœ… Technical Standards & Patterns

**From:** [Strategy 1: {query}]

**Key Findings:**
1. [Technical standard 1] - [source citation if notable]
2. [Implementation pattern 2]
3. [Best practice 3]

**Implications for Skill Design:**
- Structure should include: [sections/files based on findings]
- Must handle: [technical requirements]
- Should support: [standards/formats discovered]

---

### âœ… User Expectations & Pain Points

**From:** [Strategy 2: {query}]

**Key Findings:**
1. **Pain Point:** [User struggle 1] - Common in [context]
2. **Expectation:** [What users expect from tools in this domain]
3. **Quality Criteria:** [What defines "good" output in domain]

**Implications for Skill Design:**
- SKILL.md should address: [pain points]
- Must provide: [expected capabilities]
- Quality target: [criteria from research]

---

### âœ… Competitive Landscape & Gaps

**From:** [Strategy 3: {query}]

**Key Findings:**
1. **Existing Tools:** [Tool 1, Tool 2] - [their approaches]
2. **Common Features:** [What all tools provide]
3. **Identified Gaps:** [What's missing in current solutions]

**Implications for Skill Design:**
- Differentiation opportunity: [gap to address]
- Should match: [industry standard features]
- Can improve on: [weaknesses in existing tools]

---

### âœ… Edge Cases & Limitations (If researched)

**From:** [Strategy 4: {query}] (if executed)

**Key Findings:**
1. **Common Failure Mode:** [Edge case 1]
2. **Platform Constraint:** [Limitation discovered]
3. **Non-Obvious Challenge:** [Hidden complexity]

**Implications for Skill Design:**
- Must handle: [edge cases]
- Should validate: [constraints]
- Include warnings about: [known limitations]

---

### âœ… Innovation Opportunities & Trends (If researched)

**From:** [Strategy 5: {query}] (if executed)

**Key Findings:**
1. **Emerging Trend:** [Trend 1] - [adoption status]
2. **Novel Approach:** [Innovation worth considering]
3. **Future Direction:** [Where domain is heading]

**Implications for Skill Design:**
- Future-proof by: [incorporating trend]
- Consider experimental: [novel approach]
- Prepare for: [anticipated changes]

---

### ðŸŽ¯ Research Summary & Recommendations

**Overall Insights:**
- Primary approach: [workflow-based|task-based|reference-heavy] recommended
- Key requirements: [3-5 critical requirements identified]
- Complexity level: [low|medium|high]
- Token budget: [estimated based on findings]

**Next Steps:**
1. Load relevant knowledge files:
   - IF Skills vs Subagents unclear â†’ `knowledge/foundation/02-skills-vs-subagents.md`
   - IF token efficiency critical â†’ `knowledge/foundation/05-token-economics.md`
   - IF security considerations â†’ `knowledge/foundation/07-security-concerns.md`
2. Proceed to Step 1d: Generate structure proposals based on research

**Quality Score:** [How confident are we in research completeness?]
- Coverage: [technical âœ… | user âœ… | competitive âœ… | edge âš ï¸ | innovation âœ…]
- Confidence: [High|Medium|Low] - based on source quality and consistency
```

---

## ðŸŽ¯ Example: Instagram Caption Maker Research

### Generated Strategies (VS Output)

```json
{
  "domain": "Instagram Caption Generation",
  "task_context": "User wants skill to generate engaging Instagram captions for e-commerce fashion brand with brand voice consistency",
  "strategies": [
    {
      "id": 1,
      "query": "Instagram caption best practices 2025",
      "probability": 0.32,
      "aspect": "technical",
      "rationale": "CoT: Instagram captions have specific technical constraints (character limits, hashtag rules, emoji usage). Understanding current 2025 best practices ensures skill aligns with platform standards. Will provide: optimal length, hashtag count, formatting rules.",
      "expected_insights": "Character limits, optimal posting patterns, hashtag strategies, platform-specific features"
    },
    {
      "id": 2,
      "query": "e-commerce social media caption pain points",
      "probability": 0.28,
      "aspect": "user",
      "rationale": "CoT: E-commerce brands have unique challenges (product focus vs engagement, brand voice consistency, conversion-driven content). Identifying pain points helps skill directly address user frustrations. Will provide: common struggles, time constraints, quality expectations.",
      "expected_insights": "Time-to-create bottlenecks, brand voice challenges, A/B testing needs, batch generation requirements"
    },
    {
      "id": 3,
      "query": "AI caption generator tools comparison 2025",
      "probability": 0.22,
      "aspect": "competitive",
      "rationale": "CoT: Multiple caption tools exist (Jasper, Copy.ai, Later). Understanding their approaches reveals what works, what users like, and what gaps exist. Will provide: feature comparison, differentiation opportunities, pricing models.",
      "expected_insights": "Standard features, premium capabilities, unmet needs, pricing expectations, integration points"
    },
    {
      "id": 4,
      "query": "Instagram caption character limits edge cases",
      "probability": 0.11,
      "aspect": "edge",
      "rationale": "CoT: Character counting isn't straightforward (emojis = 2+ chars, Unicode issues, display vs actual length). Edge cases can break caption generation. Will provide: technical constraints, common errors, validation rules.",
      "expected_insights": "Unicode handling, emoji sizing, line break behavior, hashtag placement rules"
    },
    {
      "id": 5,
      "query": "social media caption AI trends 2025",
      "probability": 0.07,
      "aspect": "innovation",
      "rationale": "CoT: AI caption generation is evolving (personalization, performance prediction, trend integration). Understanding trends helps future-proof skill. Lower probability as not critical for MVP. Will provide: emerging capabilities, user expectations shift.",
      "expected_insights": "AI-powered personalization, predictive analytics, trend-aware generation, multimodal integration"
    }
  ],
  "metadata": {
    "total_probability": 1.00,
    "diversity_score": "high",
    "tail_inclusion": 1
  }
}
```

### Execution & Synthesis

**Executed Strategies:** Top 4 (strategies 1-4, since strategy 4 p=0.11 > 0.10)

**Research Findings:**

```markdown
## ðŸ“Š RESEARCH FINDINGS SUMMARY

### Context
Domain: Instagram Caption Generation
Strategies Executed: 4 strategies (technical, user, competitive, edge)
Total Sources Reviewed: 12 articles
Research Time: ~2.5 minutes

---

### âœ… Technical Standards & Patterns

**From:** "Instagram caption best practices 2025"

**Key Findings:**
1. **Optimal length:** 100-125 characters for highest engagement (first 2 lines visible)
2. **Hashtags:** 5-8 hashtags optimal (mix: 3 brand + 2-3 trending + 2 niche)
3. **Emoji usage:** Strategic placement (1-3 emojis max, avoid overuse)
4. **Hook placement:** First 40 characters critical (appears in feed preview)
5. **Posting patterns:** Captions with questions get 23% more engagement

**Implications for Skill Design:**
- Structure should include: Caption types by goal (engagement, conversion, storytelling)
- Must handle: Character counting with emoji consideration
- Should support: Hashtag research and mixing strategies

---

### âœ… User Expectations & Pain Points

**From:** "e-commerce social media caption pain points"

**Key Findings:**
1. **Pain Point:** Time-consuming (average 15-20 min per caption)
2. **Pain Point:** Brand voice inconsistency across team members
3. **Expectation:** Generate 3-5 variants for A/B testing
4. **Quality Criteria:** Must sound human, not robotic AI
5. **Workflow:** Need batch generation for weekly content planning

**Implications for Skill Design:**
- SKILL.md should address: Quick generation (<30 sec target)
- Must provide: Brand voice guidelines integration
- Quality target: Human-like, on-brand captions with testing variants

---

### âœ… Competitive Landscape & Gaps

**From:** "AI caption generator tools comparison 2025"

**Key Findings:**
1. **Existing Tools:** Copy.ai, Jasper, Later AI, Predis.ai
2. **Common Features:** Template-based, hashtag suggestions, emoji integration
3. **Identified Gaps:** 
   - Generic output (no brand voice customization)
   - No A/B variant generation
   - Weak hashtag mixing (just trending vs strategic)
   - No performance prediction

**Implications for Skill Design:**
- Differentiation opportunity: Brand voice customization + A/B variants
- Should match: Hashtag suggestions (industry standard)
- Can improve on: Strategic hashtag mixing (brand + trending + niche)

---

### âœ… Edge Cases & Limitations

**From:** "Instagram caption character limits edge cases"

**Key Findings:**
1. **Common Failure Mode:** Emoji counted incorrectly (Unicode 2-4 bytes)
2. **Platform Constraint:** 2,200 character max but display cuts at ~125
3. **Non-Obvious Challenge:** Hashtags at end vs inline behavior different
4. **Validation Issue:** Instagram censors certain word combinations

**Implications for Skill Design:**
- Must handle: Proper character counting (Unicode-aware)
- Should validate: Display length vs actual length
- Include warnings about: Censored words, hashtag placement effects

---

### ðŸŽ¯ Research Summary & Recommendations

**Overall Insights:**
- Primary approach: **Task-based** recommended (by caption goal: product launch, engagement, storytelling)
- Key requirements: Brand voice integration, A/B variants, strategic hashtags, <125 char optimal
- Complexity level: Medium (Unicode handling, brand voice, multiple variants)
- Token budget: ~2,500-3,000 tokens estimated (SKILL.md + brand voice reference)

**Next Steps:**
1. Load relevant knowledge files:
   - `knowledge/foundation/05-token-economics.md` (for efficient design)
   - `knowledge/application/09-case-studies.md` (for content generation patterns)
2. Proceed to Step 1d: Generate 3-5 structure proposals optimized for caption generation

**Quality Score:**
- Coverage: technical âœ… | user âœ… | competitive âœ… | edge âœ… | innovation âš ï¸ (not executed)
- Confidence: High - consistent findings across multiple sources, clear user needs identified
```

---

## ðŸ“ Quality Metrics & Validation

### Research Completeness Checklist

Before proceeding to Step 1d, verify:

- [ ] **Aspect Coverage:** At least 3 of 5 aspects researched
  - [ ] Technical standards identified
  - [ ] User expectations documented
  - [ ] Competitive landscape analyzed
  - [ ] Edge cases considered (if domain complex)
  - [ ] Innovation opportunities noted (nice-to-have)

- [ ] **Source Quality:** 
  - [ ] Multiple sources per aspect (not single source)
  - [ ] Recent sources (2024-2025 for trend-dependent domains)
  - [ ] Authoritative sources (not just blog posts)

- [ ] **Actionable Insights:**
  - [ ] Can inform structure proposals (Step 1d)
  - [ ] Identifies specific requirements
  - [ ] Reveals differentiation opportunities
  - [ ] Clarifies complexity level

- [ ] **Synthesis Quality:**
  - [ ] Findings organized clearly
  - [ ] Implications stated explicitly
  - [ ] Recommendations actionable
  - [ ] Conflicts/contradictions noted

**If any aspect missing:** Consider additional targeted search before Step 1d

---

## ðŸŽ¯ Optimization Guidelines

### Adaptive Strategy Selection

```python
def adjust_research_depth(context):
    """
    Adjust research depth based on context
    """
    # Factors to consider
    domain_familiarity = context.get('familiarity')  # high|medium|low
    requirements_clarity = context.get('clarity')     # clear|moderate|vague
    domain_complexity = context.get('complexity')     # simple|moderate|complex
    
    # Decision logic
    if domain_familiarity == 'low' or requirements_clarity == 'vague':
        # MUST research thoroughly
        return {
            'strategies_count': 5,
            'execute_count': 4,
            'time_budget': '3-4 minutes'
        }
    
    elif domain_complexity == 'complex':
        # Research technical + edge cases
        return {
            'strategies_count': 5,
            'execute_count': 4,
            'time_budget': '2-3 minutes',
            'focus': ['technical', 'edge']
        }
    
    else:
        # Standard research
        return {
            'strategies_count': 5,
            'execute_count': 3,
            'time_budget': '2 minutes',
            'focus': ['technical', 'user', 'competitive']
        }
```

### Temperature Tuning

**Research strategy generation:**
- Temperature: **0.8-0.9** (encourage diverse angles)
- Reason: Want non-obvious strategies to emerge

**Web search execution:**
- Temperature: N/A (deterministic search)

**Findings synthesis:**
- Temperature: **0.7** (balanced, coherent)

---

## ðŸš¨ Common Pitfalls & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| **Strategies too similar** | Prompt not emphasizing diversity | Add "explore DIFFERENT aspects" + tail sampling instruction |
| **Probabilities all ~0.2** | Model defaulting to uniform | Use CoT: "Explain WHY this probability based on research value" |
| **Irrelevant search results** | Query too generic | Add domain-specific terms, current year |
| **Redundant findings** | Similar strategies executed | Validate uniqueness before execution |
| **Synthesis too verbose** | Over-documenting every detail | Focus on ACTIONABLE insights for Step 1d |

---

## ðŸ“š Token Economics

**This file:** ~380 lines = ~4,200 tokens

**Typical usage during Step 1c:**
- SKILL.md Step 1c section: ~500 tokens
- This research-methodology.md: ~4,200 tokens
- VS strategy generation (internal): ~800 tokens
- Web search results (4 searches): ~2,000 tokens
- **Total Step 1c:** ~7,500 tokens

**Optimization:**
- File loaded only during Step 1c
- Not needed for other workflow steps
- Progressive disclosure maintained

---

## âœ… Integration with Workflow

**Workflow Context:**

```
STEP 0: Decide Approach (decision_helper.py)
    â†“
STEP 1a: Gather User Requirements
    â†“
STEP 1b: Identify Knowledge Gaps
    â†“
STEP 1c: Research Domain â† YOU ARE HERE
    â”‚
    â”œâ”€ Load: research-methodology.md
    â”œâ”€ Generate: VS research strategies (JSON)
    â”œâ”€ Execute: Top 3-4 web_search calls
    â”œâ”€ Synthesize: Findings by aspect
    â””â”€ Output: Research summary for Step 1d
    â†“
STEP 1d: Propose Structure (using research findings)
    â†“
STEP 1e: User Validation Checkpoint
    â†“
STEP 2: Initialize Structure
```

**Handoff to Step 1d:**
- âœ… Research findings summary
- âœ… Technical standards identified
- âœ… User expectations clarified
- âœ… Competitive gaps noted
- âœ… Complexity estimate
- âœ… Recommended approach (workflow/task/reference-based)

---

## ðŸŽ“ Learning & Improvement

**After each research session, consider:**

1. **What worked well?**
   - Which strategies provided most valuable insights?
   - Were probabilities accurate in predicting value?
   
2. **What could improve?**
   - Any aspect under-researched?
   - Were search queries optimal?
   - Did synthesis miss key implications?

3. **Pattern recognition:**
   - For similar domains, which aspects most critical?
   - Are there domain-specific research patterns?

**Feedback loop:**
- Track which research findings led to better proposals (Step 1d)
- Refine strategy generation based on patterns
- Update aspect priorities for domain families

---

**File Status:** Production-ready âœ…  
**Integration:** Phase 4 - Step 1c enhancement  
**VS Methodology:** Based on Zhang et al. (2024) research  
**Last Updated:** 2025-11-09

---

*"Research-driven skill creation: From assumptions to evidence-based design"*
