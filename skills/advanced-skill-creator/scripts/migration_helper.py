#!/usr/bin/env python3
"""
Convert existing documentation to skill format.
Supports Markdown and text files with intelligent structure generation.

AGENT-LAYER TOOL: Called by Claude via bash_tool, outputs JSON for parsing.

This script automates the conversion of existing documentation into Claude skill format:
- Parses source documents (MD, TXT)
- Classifies sections (core vs reference)
- Generates proper skill structure
- Creates YAML frontmatter
- Organizes references/ directory
- Produces conversion report

References:
    File 10: Technical architecture (skill structure)
    File 05: Token economics (progressive disclosure)
    Files 01-13: Best practices for skill design

Usage (Agent-Layer):
    python migration_helper.py source.md --format json
    # Returns JSON: {"status": "success", "skill_path": "...", "report": {...}}

Usage (Human-Readable):
    python migration_helper.py source.md
    python migration_helper.py source.md --preview
    python migration_helper.py source.md --skill-name my-skill --output-dir ./skills/
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MigrationHelper:
    """Convert documentation to skill format."""
    
    def __init__(self, 
                 source_path: str,
                 skill_name: Optional[str] = None,
                 output_dir: Optional[str] = None,
                 preview: bool = False):
        """
        Initialize migration helper.
        
        Args:
            source_path: Path to source document
            skill_name: Optional skill name override
            output_dir: Output directory for skill
            preview: If True, show plan without executing
        
        References: File 10 (skill structure standards)
        """
        self.source_path = Path(source_path)
        self.skill_name = skill_name or self._generate_skill_name()
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.preview = preview
        self.source_content = None
        self.source_format = None
        self.sections = []
        self.frontmatter = {}
    
    # ========== PARSING ==========
    
    def parse_source(self) -> Dict:
        """
        Parse source document.
        
        Supports:
        - Markdown files (.md, .markdown)
        - Plain text files (.txt)
        
        Returns:
            Dict with parsed structure:
            {
                'format': 'markdown' or 'text',
                'sections': int,
                'total_lines': int,
                'has_headers': bool
            }
        
        Raises:
            FileNotFoundError: If source doesn't exist
            ValueError: If format unsupported
        
        References: File 10 (content structure)
        """
        if not self.source_path.exists():
            raise FileNotFoundError(f"Source not found: {self.source_path}")
        
        with open(self.source_path, encoding='utf-8', errors='ignore') as f:
            self.source_content = f.read()
        
        # Detect format
        suffix = self.source_path.suffix.lower()
        if suffix in ['.md', '.markdown']:
            return self._parse_markdown()
        elif suffix in ['.txt', '']:
            return self._parse_plaintext()
        else:
            raise ValueError(f"Unsupported format: {suffix}")
    
    def _parse_markdown(self) -> Dict:
        """Parse Markdown document into sections."""
        self.source_format = 'markdown'
        lines = self.source_content.split('\n')
        
        # Extract sections based on headers
        current_section = {'title': 'Introduction', 'content': [], 'level': 0, 'line_start': 0}
        sections = []
        
        for i, line in enumerate(lines):
            # Match markdown headers (# Header)
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if header_match:
                # Save previous section
                if current_section['content'] or current_section['title'] != 'Introduction':
                    current_section['line_count'] = len(current_section['content'])
                    sections.append(current_section)
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = {
                    'title': title,
                    'content': [],
                    'level': level,
                    'line_start': i
                }
            else:
                current_section['content'].append(line)
        
        # Add last section
        if current_section['content']:
            current_section['line_count'] = len(current_section['content'])
            sections.append(current_section)
        
        self.sections = sections
        
        return {
            'format': 'markdown',
            'sections': len(sections),
            'total_lines': len(lines),
            'has_headers': True
        }
    
    def _parse_plaintext(self) -> Dict:
        """Parse plain text into sections."""
        self.source_format = 'text'
        lines = self.source_content.split('\n')
        
        # For plain text, treat each paragraph as a section
        sections = []
        current_section = {'title': 'Content', 'content': [], 'level': 1, 'line_start': 0}
        
        for i, line in enumerate(lines):
            if line.strip() == '':
                # Empty line might indicate section break
                if current_section['content']:
                    current_section['line_count'] = len(current_section['content'])
                    sections.append(current_section)
                    current_section = {'title': f'Section {len(sections)+1}', 'content': [], 'level': 1, 'line_start': i}
            else:
                current_section['content'].append(line)
        
        # Add last section
        if current_section['content']:
            current_section['line_count'] = len(current_section['content'])
            sections.append(current_section)
        
        self.sections = sections
        
        return {
            'format': 'text',
            'sections': len(sections),
            'total_lines': len(lines),
            'has_headers': False
        }
    
    # ========== CLASSIFICATION ==========
    
    def classify_sections(self) -> Dict:
        """
        Classify sections as core or reference.
        
        Classification rules:
        - Core: overview, setup, quick start, basic usage, workflow
        - Reference: advanced, troubleshooting, examples, detailed, edge cases
        - Heuristic: sections >100 lines â†’ reference
        
        Returns:
            Dict with classification results
        
        References: File 05 (progressive disclosure)
        """
        core_keywords = [
            'overview', 'introduction', 'setup', 'installation', 'install',
            'quick start', 'getting started', 'basic', 'usage', 'workflow',
            'how to use', 'core', 'main', 'primary'
        ]
        
        reference_keywords = [
            'advanced', 'troubleshoot', 'example', 'reference', 'api',
            'edge case', 'detailed', 'appendix', 'additional', 'extended',
            'deep dive', 'technical', 'specification', 'cookbook'
        ]
        
        core_sections = []
        reference_sections = []
        
        for section in self.sections:
            title_lower = section['title'].lower()
            line_count = section['line_count']
            
            # Heuristic: large sections go to reference
            if line_count > 100:
                reference_sections.append(section)
                continue
            
            # Check keywords
            is_core = any(kw in title_lower for kw in core_keywords)
            is_reference = any(kw in title_lower for kw in reference_keywords)
            
            if is_reference and not is_core:
                reference_sections.append(section)
            else:
                # Default to core if ambiguous or clearly core
                core_sections.append(section)
        
        return {
            'core_sections': len(core_sections),
            'reference_sections': len(reference_sections),
            'core': core_sections,
            'reference': reference_sections
        }
    
    # ========== FRONTMATTER GENERATION ==========
    
    def generate_frontmatter(self, parsed: Dict) -> str:
        """
        Generate YAML frontmatter for SKILL.md.
        
        Args:
            parsed: Parsed source structure
        
        Returns:
            YAML frontmatter string
        
        References: File 10 (frontmatter requirements)
        """
        # Extract potential description from first section
        description = "Converted from external documentation"
        if self.sections:
            first_content = '\n'.join(self.sections[0]['content'][:3])
            if first_content.strip():
                # Take first sentence as description
                sentences = re.split(r'[.!?]\s+', first_content)
                if sentences:
                    description = sentences[0].strip()[:200]  # Max 200 chars
        
        frontmatter = f"""---
name: {self.skill_name}
description: "{description}"
source: "{self.source_path.name}"
converted_at: "auto-generated"
format: "{parsed['format']}"
---
"""
        return frontmatter
    
    # ========== CONVERSION PLANNING ==========
    
    def plan_conversion(self) -> Dict:
        """
        Create conversion plan.
        
        Returns:
            Dict with conversion plan:
            {
                'skill_name': str,
                'output_path': Path,
                'core_sections': int,
                'reference_sections': int,
                'estimated_tokens': int,
                'skill_md_lines': int
            }
        
        References: File 05 (token estimation)
        """
        classified = self.classify_sections()
        
        # Estimate tokens (rough: chars / 4)
        total_chars = len(self.source_content)
        estimated_tokens = total_chars // 4
        
        # Calculate SKILL.md size (core + frontmatter + links)
        core_lines = sum(s['line_count'] for s in classified['core'])
        frontmatter_lines = 8
        links_lines = len(classified['reference']) * 2  # 2 lines per reference link
        skill_md_lines = core_lines + frontmatter_lines + links_lines + 10  # +10 for Additional Resources section
        
        output_path = self.output_dir / self.skill_name
        
        return {
            'skill_name': self.skill_name,
            'output_path': output_path,
            'core_sections': classified['core_sections'],
            'reference_sections': classified['reference_sections'],
            'core': classified['core'],
            'reference': classified['reference'],
            'estimated_tokens': estimated_tokens,
            'skill_md_lines': skill_md_lines,
            'source_lines': len(self.source_content.split('\n'))
        }
    
    # ========== EXECUTION ==========
    
    def execute_conversion(self, plan: Dict) -> Dict:
        """
        Execute conversion plan.
        
        Args:
            plan: Conversion plan from plan_conversion()
        
        Returns:
            Dict with execution results
        
        Raises:
            IOError: If file operations fail
        
        References: File 10 (skill directory structure)
        """
        if self.preview:
            return self._generate_preview_report(plan)
        
        output_path = plan['output_path']
        
        # Create skill directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create references directory if needed
        if plan['reference_sections'] > 0:
            references_dir = output_path / 'references'
            references_dir.mkdir(exist_ok=True)
        
        # Generate SKILL.md
        skill_md_path = output_path / 'SKILL.md'
        parsed = {'format': self.source_format}
        skill_content = self._build_skill_md(plan, parsed)
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(skill_content)
        
        # Create reference files
        reference_files = []
        if plan['reference_sections'] > 0:
            references_dir = output_path / 'references'
            for section in plan['reference']:
                filename = self._sanitize_filename(section['title']) + '.md'
                ref_path = references_dir / filename
                ref_content = self._build_reference_file(section)
                
                with open(ref_path, 'w', encoding='utf-8') as f:
                    f.write(ref_content)
                
                reference_files.append(filename)
        
        # Generate conversion report
        report = self._generate_conversion_report(plan, reference_files)
        report_path = output_path / 'conversion_report.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return {
            'skill_path': str(output_path),
            'skill_md': str(skill_md_path),
            'references': reference_files,
            'report': str(report_path),
            'core_sections': plan['core_sections'],
            'reference_sections': plan['reference_sections'],
            'reduction_percent': round((1 - plan['skill_md_lines'] / plan['source_lines']) * 100, 1) if plan['source_lines'] > 0 else 0
        }
    
    def _build_skill_md(self, plan: Dict, parsed: Dict) -> str:
        """Build SKILL.md content."""
        # Frontmatter
        content = self.generate_frontmatter(parsed)
        content += '\n'
        
        # Core sections
        for section in plan['core']:
            # Add section header
            if section['level'] > 0:
                content += '#' * section['level'] + ' ' + section['title'] + '\n\n'
            
            # Add section content
            content += '\n'.join(section['content']) + '\n\n'
        
        # Additional Resources section (if references exist)
        if plan['reference_sections'] > 0:
            content += '## Additional Resources\n\n'
            content += 'For detailed information, see:\n\n'
            
            for section in plan['reference']:
                filename = self._sanitize_filename(section['title'])
                content += f"- [{section['title']}](references/{filename}.md)\n"
            
            content += '\n'
        
        return content
    
    def _build_reference_file(self, section: Dict) -> str:
        """Build reference file content."""
        content = f"# {section['title']}\n\n"
        content += '\n'.join(section['content'])
        return content
    
    def _generate_conversion_report(self, plan: Dict, reference_files: List[str]) -> str:
        """Generate conversion report."""
        report = f"""# Conversion Report

**Source:** {self.source_path}  
**Skill Name:** {self.skill_name}  
**Output:** {plan['output_path']}

---

## Conversion Summary

| Metric | Value |
|--------|-------|
| Source format | {self.source_format} |
| Total sections | {plan['core_sections'] + plan['reference_sections']} |
| Core sections | {plan['core_sections']} |
| Reference sections | {plan['reference_sections']} |
| Source lines | {plan['source_lines']} |
| SKILL.md lines | {plan['skill_md_lines']} |
| Reduction | {round((1 - plan['skill_md_lines'] / plan['source_lines']) * 100, 1)}% |
| Estimated tokens | {plan['estimated_tokens']} |

---

## Structure Created

```
{self.skill_name}/
â”œâ”€â”€ SKILL.md ({plan['skill_md_lines']} lines)
â”œâ”€â”€ conversion_report.md (this file)
"""

        if reference_files:
            report += "â””â”€â”€ references/\n"
            for i, ref_file in enumerate(reference_files):
                prefix = 'â”œâ”€â”€' if i < len(reference_files) - 1 else 'â””â”€â”€'
                report += f"    {prefix} {ref_file}\n"
        
        report += "```\n\n---\n\n"
        
        report += "## Next Steps\n\n"
        report += "1. Review SKILL.md and update frontmatter description\n"
        report += "2. Add trigger phrases (WHEN to use)\n"
        report += "3. Validate structure: `python validate_skill.py " + self.skill_name + "/`\n"
        report += "4. Test the skill in Claude\n"
        report += "5. Optimize if needed: `python quality_scorer.py " + self.skill_name + "/ --format json`\n\n"
        
        report += "---\n\n"
        report += "**References:** Files 01-13 for best practices | File 10 for structure standards\n"
        
        return report
    
    def _generate_preview_report(self, plan: Dict) -> Dict:
        """Generate preview report without executing."""
        return {
            'preview': True,
            'skill_name': plan['skill_name'],
            'output_path': str(plan['output_path']),
            'core_sections': plan['core_sections'],
            'reference_sections': plan['reference_sections'],
            'estimated_lines': plan['skill_md_lines'],
            'source_lines': plan['source_lines'],
            'reduction_percent': round((1 - plan['skill_md_lines'] / plan['source_lines']) * 100, 1) if plan['source_lines'] > 0 else 0
        }
    
    # ========== HELPERS ==========
    
    def _sanitize_filename(self, title: str) -> str:
        """Convert section title to valid filename."""
        # Remove special characters
        filename = re.sub(r'[^\w\s-]', '', title)
        # Replace spaces with hyphens
        filename = filename.lower().replace(' ', '-')
        # Remove multiple hyphens
        filename = re.sub(r'-+', '-', filename)
        return filename.strip('-')
    
    def _generate_skill_name(self) -> str:
        """Auto-generate skill name from source."""
        name = self.source_path.stem
        name = re.sub(r'[^\w-]', '-', name)
        name = re.sub(r'-+', '-', name)
        return name.lower().strip('-')


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert documentation to skill format (AGENT-LAYER TOOL)",
        epilog="References: File 10 for skill structure | Files 01-13 for best practices"
    )
    parser.add_argument(
        'source',
        type=str,
        help='Source document path (MD or TXT)'
    )
    parser.add_argument(
        '--skill-name',
        type=str,
        help='Skill name (auto-generated if not specified)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory (current dir if not specified)'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview conversion without executing'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (json for agent-layer, text for human)'
    )
    
    args = parser.parse_args()
    
    try:
        helper = MigrationHelper(
            args.source,
            skill_name=args.skill_name,
            output_dir=args.output_dir,
            preview=args.preview
        )
        
        # Parse source
        parsed = helper.parse_source()
        
        # Plan conversion
        plan = helper.plan_conversion()
        
        # Execute or preview
        result = helper.execute_conversion(plan)
        
        # Agent-layer JSON output
        if args.format == 'json':
            report = {
                'status': 'success',
                'source': str(helper.source_path),
                'format': parsed['format'],
                'skill_name': result.get('skill_path', plan['skill_name']),
                'preview': args.preview,
                'conversion': {
                    'source_lines': plan['source_lines'],
                    'skill_md_lines': plan['skill_md_lines'],
                    'core_sections': result['core_sections'],
                    'reference_sections': result['reference_sections'],
                    'reduction_percent': result.get('reduction_percent', 0)
                },
                'output': {
                    'skill_path': result.get('skill_path'),
                    'skill_md': result.get('skill_md'),
                    'references': result.get('references', []),
                    'report': result.get('report')
                }
            }
            print(json.dumps(report, indent=2))
            return 0
        
        # Human-readable text output
        if args.preview:
            print("\n" + "="*60)
            print("CONVERSION PREVIEW")
            print("="*60)
            print(f"\nSource: {helper.source_path}")
            print(f"Format: {parsed['format']}")
            print(f"Skill name: {plan['skill_name']}")
            print(f"Output: {plan['output_path']}")
            print(f"\nSections:")
            print(f"  Core (â†’ SKILL.md): {plan['core_sections']}")
            print(f"  Reference (â†’ references/): {plan['reference_sections']}")
            print(f"\nEstimates:")
            print(f"  Source lines: {plan['source_lines']}")
            print(f"  SKILL.md lines: {plan['skill_md_lines']}")
            print(f"  Reduction: {round((1 - plan['skill_md_lines'] / plan['source_lines']) * 100, 1)}%")
            print(f"  Tokens: ~{plan['estimated_tokens']}")
            print("="*60)
            print("\nUse without --preview to execute conversion.")
        else:
            print("\n" + "="*60)
            print("CONVERSION COMPLETE")
            print("="*60)
            print(f"\nâœ… Skill created: {result['skill_path']}")
            print(f"   SKILL.md: {plan['skill_md_lines']} lines")
            print(f"   Core sections: {result['core_sections']}")
            print(f"   Reference files: {result['reference_sections']}")
            print(f"   Reduction: {result['reduction_percent']}%")
            print(f"\nðŸ“„ Files created:")
            print(f"   - SKILL.md")
            if result['references']:
                print(f"   - references/ ({len(result['references'])} files)")
            print(f"   - conversion_report.md")
            print("\n" + "="*60)
            print("Next steps:")
            print("  1. Review SKILL.md")
            print("  2. Update frontmatter description")
            print(f"  3. Validate: python validate_skill.py {result['skill_path']}/")
            print("="*60 + "\n")
        
        return 0
        
    except FileNotFoundError as e:
        if args.format == 'json':
            error_report = {
                'status': 'error',
                'error_type': 'FileNotFound',
                'message': str(e),
                'help': 'Ensure source file exists and path is correct'
            }
            print(json.dumps(error_report, indent=2))
        else:
            print(f"âŒ Error: {e}")
        return 1
    
    except ValueError as e:
        if args.format == 'json':
            error_report = {
                'status': 'error',
                'error_type': 'UnsupportedFormat',
                'message': str(e),
                'help': 'Only .md, .markdown, and .txt files are supported'
            }
            print(json.dumps(error_report, indent=2))
        else:
            print(f"âŒ Error: {e}")
        return 1
    
    except Exception as e:
        if args.format == 'json':
            error_report = {
                'status': 'error',
                'error_type': 'UnexpectedError',
                'message': str(e),
                'help': 'Check file permissions and content format'
            }
            print(json.dumps(error_report, indent=2))
        else:
            print(f"âŒ Unexpected error: {e}")
        return 2


if __name__ == "__main__":
    exit(main())
