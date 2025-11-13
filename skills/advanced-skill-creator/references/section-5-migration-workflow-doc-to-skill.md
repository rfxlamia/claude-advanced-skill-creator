# Section 5: Migration Workflow (Doc to Skill)

**Use when:** User has existing document, wants to convert to skill

**Entry Point:** User says "convert this doc to skill" or "migrate document"

**Prerequisites:**
- Document file available (markdown, text, PDF, docx)
- User confirms content ownership

### Migration Steps

1. **Decision Check** (Step 0)
   - Run decision_helper.py to confirm Skills appropriate
   - Proceed only if recommendation = "Skills"

2. **Migration Analysis** (Enhanced Step 2)
   ```bash
   python scripts/migration_helper.py user-doc.md --format json
   ```
   
   **JSON Output:**
   ```json
   {
     "analysis": {
       "content_type": "technical_guide",
       "structure_detected": "sequential_workflow",
       "token_count": 5200,
       "complexity": "medium"
     },
     "recommendations": {
       "skill_structure": "workflow-based",
       "split_needed": true,
       "references_suggested": ["detailed-examples.md", "edge-cases.md"]
     }
   }
   ```

3. **Structure Creation** (Step 2)
   - Create skill folder
   - Initialize SKILL.md with frontmatter
   - Organize content per recommendations

4. **Execute Steps 3-8**
   - Validation (Step 3)
   - Security (Step 4)
   - Token optimization (Step 5)
   - Progressive disclosure (Step 6)
   - Testing (Step 7)
   - Quality assessment (Step 8)

5. **Package** (Step 9)
   - Run package_skill.py
   - Deploy and test

**Tool Guide:** `knowledge/tools/22-migration-helper-guide.md`

---
