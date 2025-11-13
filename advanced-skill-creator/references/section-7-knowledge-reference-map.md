# Section 7: Knowledge Reference Map

**When Claude needs strategic context:**

### Foundation Concepts (Read First for New Skills)

**Essential reading:**
- `knowledge/foundation/01-why-skills-exist.md` - START HERE (4 core problems Skills solve)
- `knowledge/foundation/02-skills-vs-subagents.md` - Critical distinction and decision framework
- `knowledge/foundation/03-decision-tree.md` - When to use Skills vs alternatives

**Optimization knowledge:**
- `knowledge/foundation/05-token-economics.md` - Cost models and efficiency patterns
- `knowledge/foundation/06-platform-constraints.md` - Technical limitations and workarounds
- `knowledge/foundation/07-security-concerns.md` - Security threats and mitigation
- `knowledge/foundation/08-when-not-to-use.md` - Anti-patterns and failure modes

### Application Knowledge (Read for Real-World Context)

**Case studies and patterns:**
- `knowledge/application/09-case-studies.md` - Rakuten, Box, Notion examples (learn from real implementations)
- `knowledge/application/10-technical-architecture.md` - Progressive disclosure mechanics
- `knowledge/application/11-adoption-strategy.md` - Team rollout and change management
- `knowledge/application/12-testing-validation.md` - QA framework and quality assurance
- `knowledge/application/13-competitive-landscape.md` - Market analysis and positioning

### Tool Guides (Read Before Running Scripts)

**One guide per script:**
- `knowledge/tools/14-validation-tools-guide.md` - validate_skill.py usage
- `knowledge/tools/15-cost-tools-guide.md` - token_estimator.py usage
- `knowledge/tools/16-security-tools-guide.md` - security_scanner.py usage
- `knowledge/tools/17-pattern-tools-guide.md` - pattern_detector.py usage
- `knowledge/tools/18-decision-helper-guide.md` - decision_helper.py usage
- `knowledge/tools/19-test-generator-guide.md` - test_generator.py usage
- `knowledge/tools/20-split-skill-guide.md` - split_skill.py usage
- `knowledge/tools/21-quality-scorer-guide.md` - quality_scorer.py usage
- `knowledge/tools/22-migration-helper-guide.md` - migration_helper.py usage

### Reference Files (Loaded During Workflow)

**Research methodology (Step 1c):**
- `references/research-methodology.md` - Verbalized Sampling research strategy
  - Load when: Step 1c triggered (user accepts research offer)
  - Purpose: Generate diverse research strategies, execute web searches, synthesize findings
  - Token cost: ~4,200 tokens

**Proposal generation (Step 1d):**
- `references/proposal-generation.md` - Multi-option proposal generation with VS
  - Load when: Step 1d triggered (after requirements/research gathered)
  - Purpose: Generate 3-5 structure proposals, calculate probabilities, present options
  - Token cost: ~4,500 tokens

### Load Strategy

**Progressive loading principles:**
1. Load foundation files when user is new to Skills concept
2. Load application files when implementing specific patterns
3. Load tool guides when uncertain about script usage
4. Load reference files only during specific workflow steps (1c, 1d)
5. Never load all at once (36,000+ tokens) - use on-demand strategy

**Typical load patterns:**
- Beginner: foundation/01 + foundation/02 (~3,500 tokens)
- Decision making: foundation/02 + foundation/03 (~3,800 tokens)
- Implementation: foundation/01 + application/09 + tool guide (~5,000 tokens)
- Research workflow: references/research-methodology.md (~4,200 tokens)
- Proposal workflow: references/proposal-generation.md (~4,500 tokens)

**Knowledge files are 200-350 lines each. Load only what's needed for current task.**

---
