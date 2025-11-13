#!/usr/bin/env python3
"""
Auto-split large SKILL.md for progressive disclosure optimization.
Based on token economics from File 05 and architecture from File 10.

References: Files 05, 10 (token optimization, architecture)
"""

import re
import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Import shared utilities for standardized output
try:
    from utils.output_formatter import add_format_argument, format_success_response, format_error_response, output_json
except ImportError:
    # Fallback if utils not in path
    sys.path.insert(0, str(Path(__file__).parent))
    from utils.output_formatter import add_format_argument, format_success_response, format_error_response, output_json

class SkillSplitter:
    """Intelligently split SKILL.md into main + references."""
    
    def __init__(self, 
                 skill_path: str, 
                 threshold: int = 500, 
                 preview: bool = False,
                 auto: bool = False,
                 output_format: str = 'text'):
        """
        Initialize splitter.
        
        Args:
            skill_path: Path to skill directory
            threshold: Line count threshold for splitting
            preview: If True, show changes without applying
            auto: If True, split without confirmation
            output_format: 'text' or 'json' for agent-layer
        
        References: File 10 (progressive disclosure architecture)
        """
        self.skill_path = Path(skill_path)
        self.threshold = threshold
        self.preview = preview
        self.auto = auto
        self.output_format = output_format
        self.skill_md_content = None
        self.frontmatter = ''
        self.sections = []
        self.core_sections = []
        self.reference_sections = []
    
    # ========== ANALYSIS ==========
    
    def analyze_skill(self) -> Dict:
        """
        Analyze SKILL.md structure and identify split candidates.
        
        Returns:
            Dict with analysis results including:
            - needs_split: bool
            - total_lines: int
            - sections: int
            - core_sections: int
            - reference_sections: int
        
        Raises:
            FileNotFoundError: If SKILL.md doesn't exist
        
        References: File 05 (token optimization strategies)
        """
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            raise FileNotFoundError(f"SKILL.md not found in {self.skill_path}")
        
        with open(skill_md, encoding='utf-8') as f:
            self.skill_md_content = f.read()
            lines = self.skill_md_content.split('\n')
        
        total_lines = len(lines)
        
        if self.output_format == 'text':
            print(f"\nAnalyzing SKILL.md...")
            print(f"  Current size: {total_lines} lines")
            print(f"  Threshold: {self.threshold} lines")
        
        if total_lines < self.threshold:
            if self.output_format == 'text':
                print(f"\nâœ” SKILL.md already optimal (<{self.threshold} lines)")
                print("   No split needed.")
            return {
                'needs_split': False,
                'total_lines': total_lines,
                'threshold': self.threshold
            }
        
        if self.output_format == 'text':
            print(f"\nâš ï¸  SKILL.md exceeds threshold ({total_lines} > {self.threshold})")
        
        # Parse structure
        self._parse_structure()
        self._classify_sections()
        
        core_lines = sum(s['lines'] for s in self.core_sections)
        ref_lines = sum(s['lines'] for s in self.reference_sections)
        
        return {
            'needs_split': True,
            'total_lines': total_lines,
            'threshold': self.threshold,
            'core_sections': len(self.core_sections),
            'reference_sections': len(self.reference_sections),
            'core_lines': core_lines,
            'reference_lines': ref_lines,
            'reduction_percent': (ref_lines / total_lines * 100) if total_lines > 0 else 0
        }
    
    def _parse_structure(self):
        """Parse SKILL.md into sections."""
        lines = self.skill_md_content.split('\n')
        
        # Extract frontmatter
        in_frontmatter = False
        frontmatter_lines = []
        content_start = 0
        
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    frontmatter_lines.append(line)
                elif in_frontmatter:
                    frontmatter_lines.append(line)
                    self.frontmatter = '\n'.join(frontmatter_lines)
                    content_start = i + 1
                    break
            elif in_frontmatter:
                frontmatter_lines.append(line)
        
        # Parse sections (## headers)
        current_section = None
        
        for i in range(content_start, len(lines)):
            line = lines[i]
            
            # Check for ## header
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    self.sections.append(current_section)
                
                # Start new section
                current_section = {
                    'header': line,
                    'title': line.strip('# ').strip(),
                    'content': '',
                    'lines': 0,
                    'type': 'unknown'
                }
            elif current_section:
                current_section['content'] += line + '\n'
                current_section['lines'] += 1
        
        # Save last section
        if current_section:
            self.sections.append(current_section)
    
    def _classify_sections(self):
        """Classify sections as core or reference."""
        # Core section patterns
        core_patterns = [
            r'overview',
            r'quick start',
            r'installation',
            r'usage',
            r'basic',
            r'getting started',
            r'introduction'
        ]
        
        # Reference section patterns
        reference_patterns = [
            r'advanced',
            r'detailed',
            r'examples',
            r'reference',
            r'appendix',
            r'troubleshooting',
            r'faq',
            r'api',
            r'configuration'
        ]
        
        for section in self.sections:
            title_lower = section['title'].lower()
            
            # Check if core
            if any(re.search(pattern, title_lower) for pattern in core_patterns):
                section['type'] = 'core'
                self.core_sections.append(section)
            # Check if reference
            elif any(re.search(pattern, title_lower) for pattern in reference_patterns):
                section['type'] = 'reference'
                self.reference_sections.append(section)
            # Default: keep in core if short, move to reference if long
            elif section['lines'] < 50:
                section['type'] = 'core'
                self.core_sections.append(section)
            else:
                section['type'] = 'reference'
                self.reference_sections.append(section)
    
    # ========== SPLITTING ==========
    
    def perform_split(self) -> Dict:
        """
        Perform the actual split operation.
        
        Returns:
            Dict with split results
        """
        if not self.sections:
            raise ValueError("No sections found. Run analyze_skill() first.")
        
        core_lines = sum(s['lines'] for s in self.core_sections)
        ref_lines = sum(s['lines'] for s in self.reference_sections)
        total_lines = core_lines + ref_lines
        
        # Show preview if requested
        if self.preview:
            if self.output_format == 'text':
                self._show_split_preview()
            return {
                'executed': False,
                'preview_mode': True,
                'core_lines': core_lines,
                'reference_lines': ref_lines,
                'total_lines': total_lines,
                'core_sections': [{'title': s['title'], 'lines': s['lines']} for s in self.core_sections],
                'reference_sections': [{'title': s['title'], 'lines': s['lines']} for s in self.reference_sections],
                'reduction_percent': (ref_lines / total_lines * 100) if total_lines > 0 else 0
            }
        
        # Confirm with user (unless auto mode or JSON output)
        if not self.auto and self.output_format == 'text':
            print()
            response = input("Proceed with split? [y/n]: ")
            if response.lower() != 'y':
                print("Split cancelled.")
                return {
                    'executed': False,
                    'cancelled': True
                }
        
        # Execute split
        if self.output_format == 'text':
            print("\nExecuting split...")
        
        # Create references directory
        refs_dir = self.skill_path / "references"
        refs_dir.mkdir(exist_ok=True)
        if self.output_format == 'text':
            print(f"  â€¢ Created directory: references/")
        
        # Move reference sections
        created_files = []
        for section in self.reference_sections:
            filename = self._create_reference_file(section, refs_dir)
            created_files.append(filename)
        
        # Update SKILL.md
        self._update_skill_md()
        
        # Generate report
        self._generate_split_report(core_lines, ref_lines, total_lines)
        
        if self.output_format == 'text':
            print(f"\nâœ” Split completed successfully!")
        
        return {
            'executed': True,
            'core_lines': core_lines,
            'reference_lines': ref_lines,
            'total_lines': total_lines,
            'files_created': created_files,
            'core_sections': [{'title': s['title'], 'lines': s['lines']} for s in self.core_sections],
            'reference_sections': [{'title': s['title'], 'lines': s['lines'], 'file': s.get('reference_file', '')} for s in self.reference_sections],
            'reduction_percent': (ref_lines / total_lines * 100) if total_lines > 0 else 0
        }
    
    def _create_reference_file(self, section: Dict, refs_dir: Path) -> str:
        """
        Create a reference file from a section.
        
        Args:
            section: Section dictionary
            refs_dir: References directory path
        
        Returns:
            Filename created
        """
        # Generate filename from title
        filename = self._sanitize_filename(section['title']) + '.md'
        filepath = refs_dir / filename
        
        # Write content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {section['title']}\n\n")
            f.write(section['content'].strip())
            f.write('\n')  # Ensure trailing newline
        
        if self.output_format == 'text':
            print(f"  â€¢ Created: references/{filename} ({section['lines']} lines)")
        
        # Store reference for updating SKILL.md
        section['reference_file'] = filename
        
        return filename
    
    def _sanitize_filename(self, title: str) -> str:
        """
        Convert section title to valid filename.
        
        Args:
            title: Section title
        
        Returns:
            Sanitized filename (lowercase, hyphens, no special chars)
        """
        # Remove special chars, convert spaces to hyphens
        filename = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
        filename = filename.lower().replace(' ', '-')
        # Remove multiple consecutive hyphens
        filename = re.sub(r'-+', '-', filename)
        # Remove leading/trailing hyphens
        filename = filename.strip('-')
        return filename
    
    def _update_skill_md(self):
        """
        Update SKILL.md with core sections and cross-references.
        
        New structure:
        1. Frontmatter (preserved)
        2. Core sections (preserved)
        3. Additional Resources section (new, with links)
        """
        # Build new SKILL.md
        new_content = []
        
        # Add frontmatter
        if self.frontmatter:
            new_content.append(self.frontmatter.rstrip())
        
        # Add core sections
        for section in self.core_sections:
            new_content.append(f"\n{section['header']}")
            new_content.append(section['content'].strip())
        
        # Add reference links section
        new_content.append("\n## Additional Resources")
        new_content.append("\nFor detailed information, see:")
        new_content.append("")
        
        for section in self.reference_sections:
            ref_file = section['reference_file']
            new_content.append(f"- [{section['title']}](references/{ref_file})")
        
        # Write updated SKILL.md
        skill_md = self.skill_path / "SKILL.md"
        with open(skill_md, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_content))
            f.write('\n')  # Ensure trailing newline
        
        if self.output_format == 'text':
            print(f"  â€¢ Updated: SKILL.md")
    
    def _show_split_preview(self):
        """Show preview of split without applying changes."""
        print("\n" + "="*70)
        print("SPLIT PREVIEW")
        print("="*70)
        
        print("\nðŸ“„ Core Sections (will remain in SKILL.md):")
        for i, section in enumerate(self.core_sections, 1):
            print(f"  {i}. {section['title']} ({section['lines']} lines)")
        
        print(f"\nðŸ“š Reference Sections (will move to references/):")
        for i, section in enumerate(self.reference_sections, 1):
            filename = self._sanitize_filename(section['title']) + '.md'
            print(f"  {i}. {section['title']}")
            print(f"     â†’ references/{filename} ({section['lines']} lines)")
        
        print("\n" + "="*70)
        core_lines = sum(s['lines'] for s in self.core_sections)
        ref_lines = sum(s['lines'] for s in self.reference_sections)
        total_lines = core_lines + ref_lines
        
        print(f"Summary:")
        print(f"  Current SKILL.md: {total_lines} lines")
        print(f"  After split: {core_lines} lines (SKILL.md)")
        print(f"  References: {len(self.reference_sections)} files, {ref_lines} lines total")
        print(f"  Reduction: {ref_lines/total_lines*100:.1f}%")
        print("="*70)
    
    def _generate_split_report(self, core_lines: int, ref_lines: int, total_lines: int):
        """
        Generate and save split report.
        
        Args:
            core_lines: Lines remaining in SKILL.md
            ref_lines: Lines moved to references
            total_lines: Original total lines
        """
        report_path = self.skill_path / "split_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Skill Split Report\n\n")
            f.write(f"**Date:** {self._get_date()}\n")
            f.write(f"**Threshold:** {self.threshold} lines\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Original size:** {total_lines} lines\n")
            f.write(f"- **New SKILL.md size:** {core_lines} lines\n")
            f.write(f"- **References created:** {len(self.reference_sections)} files\n")
            f.write(f"- **Total reference lines:** {ref_lines} lines\n")
            f.write(f"- **Size reduction:** {ref_lines/total_lines*100:.1f}%\n\n")
            
            f.write("## Core Sections (in SKILL.md)\n\n")
            for section in self.core_sections:
                f.write(f"- {section['title']} ({section['lines']} lines)\n")
            
            f.write("\n## Reference Sections (in references/)\n\n")
            for section in self.reference_sections:
                f.write(f"- [{section['title']}](references/{section['reference_file']}) ")
                f.write(f"({section['lines']} lines)\n")
        
        if self.output_format == 'text':
            print(f"  â€¢ Generated: split_report.md")
    
    def _get_date(self) -> str:
        """Get current date in YYYY-MM-DD format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Auto-split large SKILL.md for progressive disclosure",
        epilog="References: Files 05, 10 for optimization strategies"
    )
    parser.add_argument(
        'skill_path',
        type=str,
        help='Path to skill directory'
    )
    parser.add_argument(
        '--threshold',
        type=int,
        default=500,
        help='Line count threshold for splitting (default: 500)'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview changes without applying'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Automatic split without confirmation'
    )
    add_format_argument(parser)  # Standardized --format argument

    args = parser.parse_args()
    
    try:
        splitter = SkillSplitter(
            args.skill_path,
            threshold=args.threshold,
            preview=args.preview,
            auto=args.auto,
            output_format=args.format
        )

        analysis = splitter.analyze_skill()

        if args.format == 'json':
            # JSON output mode
            if analysis.get('needs_split'):
                result = splitter.perform_split()
                output = {
                    'status': 'success',
                    'analysis': analysis,
                    'split_result': result
                }
            else:
                output = {
                    'status': 'success',
                    'analysis': analysis,
                    'message': 'No split needed - skill already optimal'
                }
            print(json.dumps(output, indent=2))
        else:
            # Text output mode (existing behavior)
            if analysis.get('needs_split'):
                splitter.perform_split()
        
        return 0
    
    except FileNotFoundError as e:
        if args.format == 'json':
            response = format_error_response(
                error_type='FileNotFoundError',
                message=str(e),
                tool_name='split_skill',
                help_text='Ensure skill directory exists and contains SKILL.md'
            )
            output_json(response)
        else:
            print(f"\nâœ— Error: {e}")
        return 1
    except Exception as e:
        if args.format == 'json':
            response = format_error_response(
                error_type=type(e).__name__,
                message=str(e),
                tool_name='split_skill',
                help_text='Check skill structure and permissions'
            )
            output_json(response)
        else:
            print(f"\nâœ— Unexpected error: {e}")
        return 2

if __name__ == "__main__":
    exit(main())
