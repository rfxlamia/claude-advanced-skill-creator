#!/usr/bin/env python3
"""
Workflow pattern detector and recommender for Claude skills.
Analyzes use cases and suggests appropriate proven patterns.

Usage:
    python pattern_detector.py "convert PDF to Word" [--format json]
    python pattern_detector.py --interactive
    python pattern_detector.py --list [--format json]

References:
    - File 04: Hybrid patterns and combinations
    - File 09: Case studies and real-world examples
    - Panduan Komprehensif: 8 proven patterns
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Import shared utilities for standardized output
try:
    from utils.output_formatter import add_format_argument, format_success_response, format_error_response, output_json
except ImportError:
    # Fallback if utils not in path
    sys.path.insert(0, str(Path(__file__).parent))
    from utils.output_formatter import add_format_argument, format_success_response, format_error_response, output_json


class PatternDetector:
    """Detect and recommend workflow patterns for skills."""
    
    # 8 proven patterns from comprehensive research
    PATTERNS = {
        'read-process-write': {
            'name': 'Read-Process-Write',
            'description': 'File transformation and data cleanup',
            'keywords': ['convert', 'transform', 'format', 'cleanup', 'process file', 'parse'],
            'use_when': 'Clear input â†’ output transformations',
            'examples': ['PDF to Word conversion', 'Data cleanup', 'Format normalization']
        },
        'search-analyze-report': {
            'name': 'Search-Analyze-Report',
            'description': 'Codebase analysis and pattern detection',
            'keywords': ['search', 'scan', 'find', 'analyze', 'detect', 'audit', 'grep'],
            'use_when': 'Large-scale code/content analysis',
            'examples': ['Security scanning', 'Code quality audit', 'Dependency analysis']
        },
        'script-automation': {
            'name': 'Script Automation',
            'description': 'Complex multi-step operations',
            'keywords': ['automate', 'pipeline', 'workflow', 'test', 'ci/cd', 'orchestrate', 'run'],
            'use_when': 'Complex automation required',
            'examples': ['CI/CD pipeline', 'Test automation', 'Build orchestration']
        },
        'wizard-multi-step': {
            'name': 'Wizard-Style Multi-Step',
            'description': 'Setup wizards and guided processes',
            'keywords': ['setup', 'init', 'configure', 'wizard', 'interactive', 'guide', 'create project'],
            'use_when': 'Complex setup processes',
            'examples': ['Project initialization', 'Configuration wizard', 'Onboarding']
        },
        'template-generation': {
            'name': 'Template Generation',
            'description': 'Structured document creation',
            'keywords': ['generate', 'template', 'create document', 'report', 'fill', 'populate'],
            'use_when': 'Repetitive document creation',
            'examples': ['Report generation', 'Email templates', 'Documentation']
        },
        'iterative-refinement': {
            'name': 'Iterative Refinement',
            'description': 'Code review and quality analysis',
            'keywords': ['review', 'refine', 'improve', 'iterate', 'quality', 'optimize'],
            'use_when': 'Quality improvement cycles',
            'examples': ['Code review', 'Architecture review', 'Performance tuning']
        },
        'context-aggregation': {
            'name': 'Context Aggregation',
            'description': 'Project summaries and documentation',
            'keywords': ['summarize', 'aggregate', 'combine', 'collect', 'dashboard', 'overview'],
            'use_when': 'Multi-source information synthesis',
            'examples': ['Project status', 'Documentation gen', 'Knowledge base']
        },
        'validation-pipeline': {
            'name': 'Validation Pipeline',
            'description': 'Data quality and compliance checking',
            'keywords': ['validate', 'check', 'verify', 'compliance', 'quality', 'assurance'],
            'use_when': 'Quality assurance required',
            'examples': ['Data validation', 'Compliance check', 'Configuration audit']
        }
    }
    
    def analyze_use_case(self, description: str) -> List[Tuple[str, float]]:
        """
        Analyze use case and recommend patterns.
        
        Returns list of (pattern_id, confidence) sorted by confidence.
        Reference: Panduan Komprehensif (8 patterns)
        """
        desc_lower = description.lower()
        scores = []
        
        for pattern_id, pattern in self.PATTERNS.items():
            # Count keyword matches
            matches = sum(1 for kw in pattern['keywords'] if kw in desc_lower)
            
            # Normalize by keyword count
            confidence = matches / len(pattern['keywords']) if pattern['keywords'] else 0.0
            
            scores.append((pattern_id, confidence))
        
        # Sort by confidence (highest first)
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
    
    def interactive_selection(self) -> str:
        """
        Interactive questionnaire for pattern selection.
        Returns recommended pattern ID.
        """
        print("\n=== Workflow Pattern Selector ===\n")
        print("Answer questions to find the best pattern:\n")
        
        # Question 1: Primary pattern
        print("1. What's your primary input/output pattern?")
        print("   a) Files in â†’ Files out (conversion/transformation)")
        print("   b) Search/scan â†’ Report (analysis)")
        print("   c) Questions â†’ Generated structure (wizard)")
        print("   d) Multiple sources â†’ Aggregated report (synthesis)")
        choice = input("   Choice [a/b/c/d]: ").strip().lower()
        
        if choice == 'a':
            return 'read-process-write'
        elif choice == 'b':
            print("\n2. What type of analysis?")
            print("   a) Code quality/security patterns")
            print("   b) Validation/compliance checking")
            choice2 = input("   Choice [a/b]: ").strip().lower()
            return 'search-analyze-report' if choice2 == 'a' else 'validation-pipeline'
        elif choice == 'c':
            return 'wizard-multi-step'
        elif choice == 'd':
            return 'context-aggregation'
        
        # Question 2: Automation
        print("\n2. Does this involve multiple automation steps?")
        choice = input("   [y/n]: ").strip().lower()
        if choice == 'y':
            return 'script-automation'
        
        # Question 3: Templates
        print("\n3. Are you generating documents from templates?")
        choice = input("   [y/n]: ").strip().lower()
        if choice == 'y':
            return 'template-generation'
        
        # Default
        return 'iterative-refinement'
    
    def generate_recommendation(self, pattern_id: str, confidence: float = None) -> str:
        """Generate detailed pattern recommendation."""
        pattern = self.PATTERNS.get(pattern_id)
        
        if not pattern:
            return f"Error: Unknown pattern '{pattern_id}'"
        
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"Recommended Pattern: {pattern['name']}")
        lines.append('='*60 + '\n')
        
        if confidence is not None:
            lines.append(f"Match confidence: {confidence:.0%}\n")
        
        lines.append(f"Description: {pattern['description']}\n")
        lines.append(f"Use When: {pattern['use_when']}\n")
        
        lines.append("Example Use Cases:")
        for example in pattern['examples']:
            lines.append(f"  â€¢ {example}")
        lines.append("")
        
        lines.append("References:")
        lines.append("  â€¢ File 04 (hybrid-patterns.md) - Combining patterns")
        lines.append("  â€¢ File 09 (case-studies.md) - Real-world examples")
        lines.append("  â€¢ Panduan Komprehensif - Detailed pattern docs\n")
        
        return '\n'.join(lines)
    
    def list_all_patterns(self) -> str:
        """List all available patterns with brief descriptions."""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append("Available Workflow Patterns")
        lines.append('='*60 + '\n')
        
        for i, (pattern_id, pattern) in enumerate(self.PATTERNS.items(), 1):
            lines.append(f"{i}. {pattern['name']}")
            lines.append(f"   {pattern['description']}")
            lines.append(f"   Use when: {pattern['use_when']}\n")
        
        lines.append(f"Total: {len(self.PATTERNS)} proven patterns")
        lines.append("\nReferences:")
        lines.append("  â€¢ Panduan Komprehensif - Full pattern documentation")
        lines.append("  â€¢ File 04 - Hybrid pattern combinations")
        lines.append("  â€¢ File 09 - Case studies\n")

        return '\n'.join(lines)

    # ========== JSON OUTPUT METHODS ==========

    def list_all_patterns_json(self) -> Dict:
        """List all patterns in JSON format."""
        patterns_list = []
        for pattern_id, pattern in self.PATTERNS.items():
            patterns_list.append({
                'id': pattern_id,
                'name': pattern['name'],
                'description': pattern['description'],
                'use_when': pattern['use_when'],
                'examples': pattern['examples'],
                'keywords': pattern['keywords']
            })

        return {
            'patterns': patterns_list,
            'total': len(self.PATTERNS),
            'references': {
                'comprehensive_guide': 'Panduan Komprehensif',
                'hybrid_patterns': 'File 04',
                'case_studies': 'File 09'
            }
        }

    def generate_recommendation_json(self, pattern_id: str, confidence: float = None) -> Dict:
        """Generate pattern recommendation in JSON format."""
        pattern = self.PATTERNS.get(pattern_id)

        if not pattern:
            return {
                'error': f"Unknown pattern '{pattern_id}'"
            }

        result = {
            'pattern_id': pattern_id,
            'pattern_name': pattern['name'],
            'description': pattern['description'],
            'use_when': pattern['use_when'],
            'examples': pattern['examples'],
            'references': [
                'File 04 (hybrid-patterns.md) - Combining patterns',
                'File 09 (case-studies.md) - Real-world examples',
                'Panduan Komprehensif - Detailed pattern docs'
            ]
        }

        if confidence is not None:
            result['confidence'] = round(confidence, 2)

        return result


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Recommend workflow patterns for Claude skills',
        epilog='References: Files 04, 09, Panduan Komprehensif'
    )
    parser.add_argument('description', nargs='?',
                        help='Use case description (or use --interactive)')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Interactive pattern selection mode')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List all available patterns')
    add_format_argument(parser)  # Standardized --format argument

    args = parser.parse_args()

    detector = PatternDetector()

    # List mode
    if args.list:
        if args.format == 'json':
            data = detector.list_all_patterns_json()
            response = format_success_response(
                data=data,
                tool_name='pattern_detector'
            )
            output_json(response)
        else:
            print(detector.list_all_patterns())
        sys.exit(0)


    # Interactive mode
    if args.interactive or not args.description:
        if args.format == 'json':
            response = format_error_response(
                error_type='InteractiveModeNotSupported',
                message='Interactive mode does not support JSON output',
                tool_name='pattern_detector',
                help_text='Use analysis mode with description for JSON output'
            )
            output_json(response)
            sys.exit(1)
        pattern_id = detector.interactive_selection()
        print(detector.generate_recommendation(pattern_id))
        sys.exit(0)

    # Analysis mode
    matches = detector.analyze_use_case(args.description)
    best_match, confidence = matches[0]

    if confidence < 0.1:
        if args.format == 'json':
            response = format_error_response(
                error_type='NoPatternMatch',
                message='No clear pattern match found',
                tool_name='pattern_detector',
                help_text='Try providing more keywords in description, use --interactive mode, or --list to see all patterns',
                details={'confidence': round(confidence, 2)}
            )
            output_json(response)
        else:
            print("No clear pattern match found.")
            print("\nSuggestions:")
            print("  - Try --interactive mode for guided selection")
            print("  - Try --list to see all available patterns")
            print("  - Provide more keywords in your description")
        sys.exit(1)

    # Show primary recommendation
    if args.format == 'json':
        recommendation = detector.generate_recommendation_json(best_match, confidence)

        # Add alternatives if confidence is moderate
        alternatives = []
        if confidence < 0.5 and len(matches) > 1:
            for pattern_id, score in matches[1:3]:
                if score > 0:
                    pattern = detector.PATTERNS[pattern_id]
                    alternatives.append({
                        'pattern_id': pattern_id,
                        'pattern_name': pattern['name'],
                        'description': pattern['description'],
                        'confidence': round(score, 2)
                    })

        data = {
            'primary_recommendation': recommendation,
            'alternatives': alternatives if alternatives else None
        }

        response = format_success_response(
            data=data,
            tool_name='pattern_detector'
        )
        output_json(response)
    else:
        print(detector.generate_recommendation(best_match, confidence))

        # Show alternatives if confidence is moderate
        if confidence < 0.5 and len(matches) > 1:
            print("\n" + "-"*60)
            print("Alternative patterns to consider:")
            print("-"*60)
            for pattern_id, score in matches[1:3]:
                if score > 0:
                    pattern = detector.PATTERNS[pattern_id]
                    print(f"  - {pattern['name']} ({score:.0%} match)")
                    print(f"    {pattern['description']}")
            print()

    sys.exit(0)


if __name__ == '__main__':
    main()

