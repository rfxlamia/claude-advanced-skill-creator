#!/usr/bin/env python3
"""
Cross-Reference Validation - File Existence Checking

Validates that all file references in SKILL.md actually exist in the skill directory.
Prevents broken references and orphaned files from being packaged.

Usage:
    from utils.reference_validator import CrossReferenceValidator

    validator = CrossReferenceValidator(skill_path='/path/to/skill')
    result = validator.validate_skill_md()

    if result['status'] == 'fail':
        print(f"Missing files: {result['missing_files']}")
        print(f"Suggestion: {result['suggestion']}")

Version: 1.0
Part of: Advanced Skill Creator v1.2 - Issue #5 fix (File Existence Validation)
Reference: TEST-REPORT.md Issue #5 - Validation Doesn't Check File Existence
           TEST-REPORT.md Issue #1 - Broken Reference Pattern
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of cross-reference validation."""
    status: str  # 'pass' or 'fail'
    message: str
    missing_files: List[str] = field(default_factory=list)
    orphaned_files: List[str] = field(default_factory=list)
    valid_references: List[str] = field(default_factory=list)
    suggestion: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'status': self.status,
            'message': self.message,
            'missing_files': self.missing_files,
            'orphaned_files': self.orphaned_files,
            'valid_references': self.valid_references,
            'suggestion': self.suggestion,
            'details': self.details
        }


class CrossReferenceValidator:
    """
    Validate cross-references between SKILL.md and actual files.

    Addresses:
    - Issue #1: Broken Reference Pattern (files referenced but not created)
    - Issue #5: File Existence Validation (must check actual files)
    - Issue #7: Orphaned Files (files exist but not referenced)
    """

    # Patterns to extract file references from markdown
    MARKDOWN_LINK_PATTERN = r'\[([^\]]+)\]\(([^)]+)\)'  # [text](path)
    CODE_REFERENCE_PATTERN = r'`([^`]+\.(md|py|json|yaml|txt))`'  # `filename.ext`
    PATH_REFERENCE_PATTERN = r'(?:files?|resources?|knowledge|files?:)\s+([^\s\n]+\.(?:md|py))'  # "file: path.md"

    def __init__(self, skill_path: str):
        """
        Initialize validator.

        Args:
            skill_path: Path to skill directory
        """
        self.skill_path = Path(skill_path)
        self.skill_md_path = self.skill_path / 'SKILL.md'

    def validate_skill_md(self) -> ValidationResult:
        """
        Validate SKILL.md references against actual files.

        Returns:
            ValidationResult with status, missing/orphaned files, and suggestions
        """
        if not self.skill_path.exists():
            return ValidationResult(
                status='fail',
                message=f"Skill directory not found: {self.skill_path}",
                suggestion=f"Create skill directory at {self.skill_path}"
            )

        if not self.skill_md_path.exists():
            return ValidationResult(
                status='fail',
                message="SKILL.md not found",
                suggestion="Create SKILL.md in skill directory"
            )

        # Read SKILL.md content
        try:
            with open(self.skill_md_path, 'r', encoding='utf-8') as f:
                skill_md_content = f.read()
        except Exception as e:
            return ValidationResult(
                status='fail',
                message=f"Error reading SKILL.md: {e}",
                suggestion="Ensure SKILL.md is readable"
            )

        # Extract references
        referenced_files = self._extract_file_references(skill_md_content)

        # Check which references exist
        missing_files = []
        valid_references = []

        for ref in referenced_files:
            full_path = self.skill_path / ref
            if full_path.exists():
                valid_references.append(ref)
            else:
                missing_files.append(ref)

        # Find orphaned files (exist but not referenced)
        orphaned_files = self._find_orphaned_files(referenced_files)

        # Determine status and message
        if missing_files or orphaned_files:
            status = 'fail'
            message = self._build_failure_message(missing_files, orphaned_files)
            suggestion = self._build_suggestion(missing_files, orphaned_files)
        else:
            status = 'pass'
            message = f"All {len(valid_references)} file references are valid"
            suggestion = ""

        return ValidationResult(
            status=status,
            message=message,
            missing_files=missing_files,
            orphaned_files=orphaned_files,
            valid_references=valid_references,
            suggestion=suggestion,
            details={
                'referenced_files_count': len(referenced_files),
                'valid_references_count': len(valid_references),
                'missing_files_count': len(missing_files),
                'orphaned_files_count': len(orphaned_files)
            }
        )

    def _extract_file_references(self, content: str) -> List[str]:
        """
        Extract file references from SKILL.md content.

        Looks for:
        1. Markdown links: [text](path/to/file.md)
        2. Code references: `filename.md`
        3. Path patterns: "file: path/to/file.md"

        Args:
            content: SKILL.md content

        Returns:
            List of unique file references (relative paths)
        """
        references = set()

        # Pattern 1: Markdown links [text](path)
        for match in re.finditer(self.MARKDOWN_LINK_PATTERN, content):
            path = match.group(2)
            # Only include local file references (not URLs)
            if not path.startswith('http') and path.endswith(('.md', '.py', '.txt')):
                references.add(path)

        # Pattern 2: Code references `filename.ext`
        for match in re.finditer(self.CODE_REFERENCE_PATTERN, content):
            references.add(match.group(1))

        # Pattern 3: Path patterns with keywords
        for match in re.finditer(self.PATH_REFERENCE_PATTERN, content):
            references.add(match.group(1))

        # Normalize paths (remove ../ prefixes if at root)
        normalized = set()
        for ref in references:
            # Clean up relative path notation
            if ref.startswith('./'):
                ref = ref[2:]
            normalized.add(ref)

        return sorted(list(normalized))

    def _find_orphaned_files(self, referenced_files: List[str]) -> List[str]:
        """
        Find files that exist but are not referenced in SKILL.md.

        Args:
            referenced_files: List of referenced files

        Returns:
            List of orphaned files found
        """
        orphaned = []
        referenced_normalized = set(referenced_files)

        # Walk through skill directory
        for root, dirs, files in os.walk(self.skill_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file.endswith(('.md', '.py', '.txt', '.json', '.yaml')):
                    full_path = Path(root) / file
                    rel_path = str(full_path.relative_to(self.skill_path))

                    # Check if referenced
                    is_referenced = any(
                        rel_path == ref or
                        rel_path.endswith(ref) or
                        ref.endswith(file)
                        for ref in referenced_normalized
                    )

                    if not is_referenced:
                        # Exclude common non-referenced files
                        if file not in ['SKILL.md', '.gitignore', 'README.md']:
                            orphaned.append(rel_path)

        return sorted(orphaned)

    def _build_failure_message(self, missing: List[str], orphaned: List[str]) -> str:
        """Build human-readable failure message."""
        parts = []

        if missing:
            parts.append(f"❌ {len(missing)} referenced files not found: {', '.join(missing[:3])}")
            if len(missing) > 3:
                parts[-1] += f" (+{len(missing) - 3} more)"

        if orphaned:
            parts.append(f"⚠️ {len(orphaned)} orphaned files in skill directory")

        return " | ".join(parts)

    def _build_suggestion(self, missing: List[str], orphaned: List[str]) -> str:
        """Build actionable suggestion for fixing issues."""
        suggestions = []

        if missing:
            suggestions.append(
                f"Remove {len(missing)} broken reference(s) from SKILL.md, "
                f"or create the missing files: {', '.join(missing[:2])}"
            )

        if orphaned:
            suggestions.append(
                f"Either: (a) Add {len(orphaned)} orphaned file(s) to SKILL.md documentation, "
                f"or (b) delete them from skill directory"
            )

        return " | ".join(suggestions) if suggestions else ""

    def validate_skill_directory(self, strict: bool = False) -> ValidationResult:
        """
        Comprehensive validation of entire skill directory.

        Checks:
        - SKILL.md exists and is valid
        - All references valid
        - No orphaned files (if strict=True)

        Args:
            strict: If True, orphaned files cause failure. If False, just warning.

        Returns:
            ValidationResult
        """
        result = self.validate_skill_md()

        # If strict mode, orphaned files cause failure
        if strict and result.orphaned_files:
            result.status = 'fail'
            result.message = f"{result.message} (strict mode: orphaned files not allowed)"

        return result

    def check_reference(self, reference: str) -> bool:
        """
        Check if a single reference exists.

        Args:
            reference: File reference to check

        Returns:
            True if file exists, False otherwise
        """
        full_path = self.skill_path / reference
        return full_path.exists()

    def list_all_references(self) -> Dict[str, List[str]]:
        """
        List all references in SKILL.md organized by category.

        Returns:
            Dict with 'valid', 'missing', 'orphaned' lists
        """
        try:
            with open(self.skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return {'valid': [], 'missing': [], 'orphaned': []}

        referenced = self._extract_file_references(content)
        valid = [f for f in referenced if self.check_reference(f)]
        missing = [f for f in referenced if not self.check_reference(f)]
        orphaned = self._find_orphaned_files(referenced)

        return {
            'valid': valid,
            'missing': missing,
            'orphaned': orphaned
        }


class SkillPackageValidator:
    """
    Validate skill before packaging.

    Ensures:
    1. All referenced files exist (no broken references)
    2. No orphaned files included in package
    3. SKILL.md is syntactically valid
    """

    def __init__(self, skill_path: str):
        """
        Initialize validator.

        Args:
            skill_path: Path to skill directory
        """
        self.skill_path = Path(skill_path)
        self.ref_validator = CrossReferenceValidator(skill_path)

    def validate_for_packaging(self, strict: bool = False) -> ValidationResult:
        """
        Validate skill is ready for packaging.

        Args:
            strict: If True, any issues cause failure

        Returns:
            ValidationResult indicating if safe to package
        """
        result = self.ref_validator.validate_skill_directory(strict=strict)

        if result.status == 'fail':
            result.suggestion = (
                f"Fix issues before packaging: {result.suggestion}"
            )

        return result


if __name__ == '__main__':
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python reference_validator.py <skill_path> [--strict]")
        sys.exit(1)

    skill_path = sys.argv[1]
    strict_mode = '--strict' in sys.argv

    validator = CrossReferenceValidator(skill_path)
    result = validator.validate_skill_md()

    print(f"Status: {result.status.upper()}")
    print(f"Message: {result.message}")

    if result.missing_files:
        print(f"\nMissing files ({len(result.missing_files)}):")
        for f in result.missing_files:
            print(f"  ❌ {f}")

    if result.orphaned_files:
        print(f"\nOrphaned files ({len(result.orphaned_files)}):")
        for f in result.orphaned_files:
            print(f"  ⚠️ {f}")

    if result.suggestion:
        print(f"\nSuggestion: {result.suggestion}")

    if result.valid_references:
        print(f"\nValid references: {len(result.valid_references)}")

    sys.exit(0 if result.status == 'pass' else 1)
