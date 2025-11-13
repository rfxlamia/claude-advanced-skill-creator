#!/usr/bin/env python3
"""
Security vulnerability scanner for Claude skills.
Detects common security anti-patterns and provides remediation guidance.

Usage:
    python security_scanner.py <skill_path> [--severity LEVEL] [--format FORMAT]

References:
    - File 07: Security concerns and best practices
    - File 16: Vulnerability patterns and prevention
"""

import re
import sys
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Security finding severity levels."""
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    INFO = 4


@dataclass
class Finding:
    """Single security finding."""
    severity: Severity
    finding_type: str
    file: str
    line: int
    description: str
    evidence: str
    remediation: str


class SecurityScanner:
    """Automated security vulnerability detection for skills."""
    
    def __init__(self, skill_path: str):
        """Initialize scanner with skill directory path."""
        self.skill_path = Path(skill_path)
        self.findings: List[Finding] = []
        
        if not self.skill_path.exists():
            raise FileNotFoundError(f"Skill path not found: {skill_path}")
    
    # ========== SECRET DETECTION ==========
    
    def scan_hardcoded_secrets(self) -> List[Finding]:
        """
        Scan for hardcoded secrets in all files.
        Reference: File 07 (credential management)
        """
        findings = []
        
        secret_patterns = [
            (r'api[_-]?key\s*=\s*["\'][\w\-]+["\']', 'API key'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Password'),
            (r'token\s*=\s*["\'][\w\-]+["\']', 'Token'),
            (r'secret\s*=\s*["\'][\w\-]+["\']', 'Secret'),
            (r'Authorization:\s*Bearer\s+[\w\-\.]+', 'Bearer token'),
            (r'sk-[a-zA-Z0-9]{32,}', 'API key pattern'),
        ]
        
        for file_path in self._get_scannable_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            for pattern, secret_type in secret_patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(Finding(
                        severity=Severity.CRITICAL,
                        finding_type='Hardcoded Secret',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'{secret_type} detected in code',
                        evidence=match.group(0)[:50] + '...',
                        remediation='Use environment variables or secret management (File 07)'
                    ))
        
        return findings
    
    # ========== COMMAND INJECTION ==========
    
    def scan_command_injection(self) -> List[Finding]:
        """
        Scan for command injection vulnerabilities.
        Reference: File 07 (injection risks)
        """
        findings = []
        
        dangerous_patterns = [
            (r'subprocess\.\w+\([^)]*shell\s*=\s*True', 'shell=True', Severity.CRITICAL),
            (r'os\.system\s*\(', 'os.system()', Severity.CRITICAL),
            (r'\beval\s*\(', 'eval()', Severity.CRITICAL),
            (r'\bexec\s*\(', 'exec()', Severity.CRITICAL),
        ]
        
        for file_path in self._get_python_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            for pattern, name, severity in dangerous_patterns:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(Finding(
                        severity=severity,
                        finding_type='Command Injection Risk',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'Dangerous function: {name}',
                        evidence=match.group(0),
                        remediation='Use parameterized commands, avoid shell=True/eval/exec'
                    ))
        
        return findings
    
    # ========== SQL INJECTION ==========
    
    def scan_sql_injection(self) -> List[Finding]:
        """
        Scan for SQL injection patterns.
        Reference: File 16 (SQL injection prevention)
        """
        findings = []
        
        sql_patterns = [
            (r'(SELECT|INSERT|UPDATE|DELETE).*\+.*', 'string concatenation'),
            (r'(SELECT|INSERT|UPDATE|DELETE).*f["\'].*\{', 'f-string formatting'),
            (r'(SELECT|INSERT|UPDATE|DELETE).*\.format\(', '.format() usage'),
        ]
        
        for file_path in self._get_python_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            for pattern, name in sql_patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(Finding(
                        severity=Severity.HIGH,
                        finding_type='SQL Injection Risk',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'SQL query with {name}',
                        evidence=match.group(0)[:80],
                        remediation='Use parameterized queries with placeholders (?)'
                    ))
        
        return findings
    
    # ========== PATH TRAVERSAL ==========
    
    def scan_path_traversal(self) -> List[Finding]:
        """
        Scan for path traversal vulnerabilities.
        Reference: File 16 (path security)
        """
        findings = []
        
        file_operations = [
            'open(', 'Path(', 'read_text(', 'write_text(',
            'os.path.join(', 'shutil.copy(', 'shutil.move('
        ]
        
        for file_path in self._get_python_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Heuristic: file operations + user input handling
            has_file_ops = any(op in content for op in file_operations)
            has_user_input = 'input(' in content or 'args.' in content or 'argv' in content
            
            if has_file_ops and has_user_input:
                findings.append(Finding(
                    severity=Severity.MEDIUM,
                    finding_type='Path Traversal Risk',
                    file=str(file_path.relative_to(self.skill_path)),
                    line=0,
                    description='File operations with potential user input',
                    evidence='File has both file operations and user input handling',
                    remediation='Validate paths, use Path.resolve(), check for .. patterns'
                ))
        
        return findings
    
    # ========== DANGEROUS IMPORTS ==========
    
    def scan_dangerous_imports(self) -> List[Finding]:
        """
        Scan for dangerous library imports.
        Reference: File 16 (dangerous imports)
        """
        findings = []
        
        dangerous_imports = [
            ('import pickle', 'pickle', Severity.HIGH, 
             'Arbitrary code execution via deserialization. Use json instead.'),
            ('from pickle', 'pickle', Severity.HIGH,
             'Arbitrary code execution via deserialization. Use json instead.'),
            ('yaml.load(', 'yaml.load()', Severity.HIGH,
             'Unsafe YAML loading. Use yaml.safe_load() instead.'),
        ]
        
        for file_path in self._get_python_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            for pattern, name, severity, remediation in dangerous_imports:
                if pattern in content:
                    line_num = content.split(pattern)[0].count('\n') + 1
                    findings.append(Finding(
                        severity=severity,
                        finding_type='Dangerous Import',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'Risky library: {name}',
                        evidence=pattern,
                        remediation=remediation
                    ))
        
        return findings
    
    # ========== NETWORK CONNECTIONS ==========
    
    def scan_network_connections(self) -> List[Finding]:
        """
        Scan for external network connections.
        Reference: File 16 (network security)
        """
        findings = []
        
        network_patterns = [
            (r'https?://(?!localhost|127\.0\.0\.1)[^\s\'"]+', 'External URL'),
            (r'requests\.get\(', 'HTTP GET request'),
            (r'requests\.post\(', 'HTTP POST request'),
            (r'socket\.connect\(', 'Socket connection'),
            (r'urllib\.request\.urlopen\(', 'URL open'),
        ]
        
        for file_path in self._get_scannable_files():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            for pattern, name in network_patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(Finding(
                        severity=Severity.MEDIUM,
                        finding_type='External Network Connection',
                        file=str(file_path.relative_to(self.skill_path)),
                        line=line_num,
                        description=f'{name} detected',
                        evidence=match.group(0)[:60],
                        remediation='Validate necessity, use HTTPS, verify certificates'
                    ))
        
        return findings
    
    # ========== PROMPT INJECTION ==========
    
    def scan_prompt_injection(self) -> List[Finding]:
        """
        Scan for prompt injection vulnerabilities in SKILL.md.
        Reference: File 07 (prompt injection prevention)
        """
        findings = []
        
        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            
            # Check for user input handling without validation mention
            has_user_input = 'user input' in content.lower() or 'user data' in content.lower()
            has_validation = 'validat' in content.lower() or 'sanitiz' in content.lower()
            
            if has_user_input and not has_validation:
                findings.append(Finding(
                    severity=Severity.MEDIUM,
                    finding_type='Prompt Injection Risk',
                    file='SKILL.md',
                    line=0,
                    description='User input mentioned without validation guidance',
                    evidence='Instructions reference user input without validation',
                    remediation='Add input validation/sanitization instructions (File 07)'
                ))
        
        return findings
    
    # ========== UTILITY METHODS ==========
    
    def _get_scannable_files(self) -> List[Path]:
        """Get all files that should be scanned."""
        extensions = ['.py', '.md', '.sh', '.yaml', '.yml']
        files = []
        for ext in extensions:
            files.extend(self.skill_path.rglob(f'*{ext}'))
        return files
    
    def _get_python_files(self) -> List[Path]:
        """Get all Python files in skill directory."""
        return list(self.skill_path.rglob('*.py'))
    
    # ========== SCAN EXECUTION ==========
    
    def run_all_scans(self) -> List[Finding]:
        """Run all security scans and return findings."""
        self.findings = []
        
        self.findings.extend(self.scan_hardcoded_secrets())
        self.findings.extend(self.scan_command_injection())
        self.findings.extend(self.scan_sql_injection())
        self.findings.extend(self.scan_path_traversal())
        self.findings.extend(self.scan_dangerous_imports())
        self.findings.extend(self.scan_network_connections())
        self.findings.extend(self.scan_prompt_injection())
        
        return self.findings
    
    # ========== REPORT GENERATION ==========
    
    def generate_report(self, min_severity: Severity = Severity.LOW, format: str = 'text') -> str:
        """Generate security scan report."""
        if format == 'json':
            return self._generate_json_report(min_severity)
        return self._generate_text_report(min_severity)
    
    def _generate_text_report(self, min_severity: Severity) -> str:
        """Generate human-readable text report."""
        # Filter by severity
        filtered = [f for f in self.findings if f.severity.value <= min_severity.value]
        
        # Categorize
        critical = [f for f in filtered if f.severity == Severity.CRITICAL]
        high = [f for f in filtered if f.severity == Severity.HIGH]
        medium = [f for f in filtered if f.severity == Severity.MEDIUM]
        low = [f for f in filtered if f.severity == Severity.LOW]
        
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"Security Scan Report: {self.skill_path.name}")
        lines.append('='*60 + '\n')
        
        # Critical issues
        if critical:
            lines.append("ðŸ”´ CRITICAL ISSUES (must fix before deployment):\n")
            for i, finding in enumerate(critical, 1):
                lines.append(f"{i}. {finding.finding_type}")
                lines.append(f"   File: {finding.file}:{finding.line}")
                lines.append(f"   Issue: {finding.description}")
                lines.append(f"   Evidence: {finding.evidence}")
                lines.append(f"   Fix: {finding.remediation}\n")
        
        # High severity
        if high:
            lines.append("ðŸŸ  HIGH SEVERITY (review and fix):\n")
            for i, finding in enumerate(high, 1):
                lines.append(f"{i}. {finding.finding_type}")
                lines.append(f"   File: {finding.file}:{finding.line}")
                lines.append(f"   Issue: {finding.description}")
                lines.append(f"   Fix: {finding.remediation}\n")
        
        # Medium severity
        if medium:
            lines.append("ðŸŸ¡ MEDIUM SEVERITY (review required):\n")
            for i, finding in enumerate(medium, 1):
                lines.append(f"{i}. {finding.finding_type} in {finding.file}")
                lines.append(f"   {finding.description}\n")
        
        # Summary
        total_issues = len(filtered)
        if total_issues == 0:
            lines.append("ðŸŸ¢ No security issues found!\n")
        else:
            lines.append('-'*60)
            lines.append(f"Security Score: {len(critical)} critical, "
                        f"{len(high)} high, {len(medium)} medium, {len(low)} low\n")
            
            if critical:
                lines.append("âš ï¸  CRITICAL ISSUES FOUND - Do NOT deploy until fixed!")
            elif high:
                lines.append("âš ï¸  HIGH SEVERITY ISSUES - Fix before production")
        
        # Recommendations
        lines.append("\nGeneral Security Best Practices:")
        lines.append("  â€¢ Never hardcode credentials - use environment variables")
        lines.append("  â€¢ Never use shell=True with user input")
        lines.append("  â€¢ Always validate and sanitize inputs")
        lines.append("  â€¢ Use parameterized queries for SQL")
        lines.append("  â€¢ Test skills in isolated environment first")
        lines.append("\nReferences: File 07 (security-concerns.md) for guidance\n")
        
        return '\n'.join(lines)
    
    def _generate_json_report(self, min_severity: Severity) -> str:
        """Generate machine-readable JSON report."""
        import json
        
        filtered = [f for f in self.findings if f.severity.value <= min_severity.value]
        
        report = {
            'skill_name': self.skill_path.name,
            'findings': [
                {
                    'severity': f.severity.name,
                    'type': f.finding_type,
                    'file': f.file,
                    'line': f.line,
                    'description': f.description,
                    'evidence': f.evidence,
                    'remediation': f.remediation
                }
                for f in filtered
            ],
            'summary': {
                'total': len(filtered),
                'critical': len([f for f in filtered if f.severity == Severity.CRITICAL]),
                'high': len([f for f in filtered if f.severity == Severity.HIGH]),
                'medium': len([f for f in filtered if f.severity == Severity.MEDIUM]),
                'low': len([f for f in filtered if f.severity == Severity.LOW])
            }
        }
        return json.dumps(report, indent=2)
    
    def get_exit_code(self) -> int:
        """Get appropriate exit code based on findings."""
        if any(f.severity == Severity.CRITICAL for f in self.findings):
            return 2  # Critical issues
        if any(f.severity == Severity.HIGH for f in self.findings):
            return 1  # High severity
        return 0  # All clear


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Scan Claude skill for security vulnerabilities',
        epilog='References: Files 07, 16 for security guidance'
    )
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--severity', 
                        choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                        default='LOW',
                        help='Minimum severity to report (default: LOW)')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='Output format (default: text)')
    
    args = parser.parse_args()
    
    try:
        scanner = SecurityScanner(args.skill_path)
        scanner.run_all_scans()
        
        min_sev = Severity[args.severity]
        report = scanner.generate_report(min_severity=min_sev, format=args.format)
        
        print(report)
        sys.exit(scanner.get_exit_code())
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
