#!/usr/bin/env python3
"""
Token cost estimation tool for Claude skills.
Predicts token consumption and monthly costs using progressive disclosure analysis.

Usage:
    python token_estimator.py <skill_path> [--volume N] [--model MODEL] [--format FORMAT]

References:
    - File 05: Token economics and optimization strategies
    - File 10: Progressive disclosure architecture (3-level model)
    - File 15: Cost optimization techniques
"""

import sys
import json
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

# Import shared utilities for standardized output
try:
    from utils.output_formatter import add_format_argument, format_success_response, format_error_response, output_json
except ImportError:
    # Fallback if utils not in path
    sys.path.insert(0, str(Path(__file__).parent))
    from utils.output_formatter import add_format_argument, format_success_response, format_error_response, output_json


@dataclass
class CostBreakdown:
    """Token and cost breakdown for a usage scenario."""
    scenario: str
    tokens: int
    cost_per_use: float
    monthly_cost: float


class TokenEstimator:
    """Token cost estimation and progressive disclosure analysis."""
    
    # Pricing per million tokens (November 2024)
    PRICING = {
        'claude-sonnet-4.5': {
            'input': 3.00,
            'output': 15.00
        },
        'claude-opus-4': {
            'input': 15.00,
            'output': 75.00
        }
    }
    
    def __init__(self, skill_path: str, model: str = 'claude-sonnet-4.5', output_format: str = 'text'):
        """Initialize estimator with skill path, pricing model, and output format."""
        self.skill_path = Path(skill_path)
        self.model = model
        self.output_format = output_format
        self.pricing = self.PRICING.get(model, self.PRICING['claude-sonnet-4.5'])
        
        if not self.skill_path.exists():
            raise FileNotFoundError(f"Skill path not found: {skill_path}")
    
    # ========== TOKEN COUNTING ==========
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count using averaged method.
        
        Combines two approaches:
        1. Word count * 1.3 (conservative estimate)
        2. Character count / 4 (average estimate)
        
        Returns average of both methods for accuracy.
        Reference: File 05 (token estimation methodology)
        """
        words = len(text.split())
        chars = len(text)
        
        token_by_words = int(words * 1.3)
        token_by_chars = int(chars / 4)
        
        return int((token_by_words + token_by_chars) / 2)
    
    def _extract_frontmatter(self, content: str) -> str:
        """Extract YAML frontmatter from markdown."""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return f"---{parts[1]}---"
        return ""
    
    def _extract_body(self, content: str) -> str:
        """Extract body content (excluding frontmatter)."""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()
        return content
    
    # ========== PROGRESSIVE DISCLOSURE ANALYSIS ==========
    
    def analyze_progressive_disclosure(self) -> Dict:
        """
        Analyze skill using 3-level progressive disclosure model.
        
        Levels:
        - Level 1: Metadata (always loaded)
        - Level 2: SKILL.md body (loaded when triggered)
        - Level 3: References (loaded on-demand)
        
        Returns:
            Dict with token counts per level
        
        Reference: File 10 (progressive disclosure architecture)
        """
        breakdown = {
            'level_1_metadata': 0,
            'level_2_skill_body': 0,
            'level_3_references': {},
            'scripts': []
        }
        
        # Level 1: Metadata (YAML frontmatter)
        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            frontmatter = self._extract_frontmatter(content)
            breakdown['level_1_metadata'] = self.count_tokens(frontmatter)
            
            # Level 2: Body content
            body = self._extract_body(content)
            breakdown['level_2_skill_body'] = self.count_tokens(body)
        
        # Level 3: Reference files
        refs_dir = self.skill_path / 'references'
        if refs_dir.exists():
            for ref_file in refs_dir.glob('*.md'):
                content = ref_file.read_text(encoding='utf-8')
                tokens = self.count_tokens(content)
                breakdown['level_3_references'][ref_file.name] = tokens
        
        # Scripts (output only, conservative 200 tokens estimate)
        scripts_dir = self.skill_path / 'scripts'
        if scripts_dir.exists():
            for script in scripts_dir.glob('*.py'):
                breakdown['scripts'].append({
                    'name': script.name,
                    'estimated_output': 200
                })
        
        return breakdown
    
    # ========== USAGE SCENARIOS ==========
    
    def estimate_usage_scenarios(self, breakdown: Dict) -> Dict[str, int]:
        """
        Calculate token usage for different scenarios.
        
        Scenarios:
        - idle: Only metadata (skill in context but not triggered)
        - typical: Metadata + SKILL.md body (normal skill use)
        - with_reference: + smallest reference file (common case)
        - worst_case: All content loaded (rare but possible)
        
        Reference: File 15 (cost scenarios)
        """
        scenarios = {}
        
        # Idle: Just metadata
        scenarios['idle'] = breakdown['level_1_metadata']
        
        # Typical: Metadata + body
        scenarios['typical'] = (
            breakdown['level_1_metadata'] + 
            breakdown['level_2_skill_body']
        )
        
        # With reference: + most common (smallest) reference
        if breakdown['level_3_references']:
            smallest_ref = min(breakdown['level_3_references'].values())
            scenarios['with_reference'] = scenarios['typical'] + smallest_ref
        else:
            scenarios['with_reference'] = scenarios['typical']
        
        # Worst-case: Everything
        total_refs = sum(breakdown['level_3_references'].values())
        scenarios['worst_case'] = (
            breakdown['level_1_metadata'] + 
            breakdown['level_2_skill_body'] + 
            total_refs
        )
        
        return scenarios
    
    # ========== COST CALCULATION ==========
    
    def calculate_costs(
        self, 
        scenarios: Dict[str, int], 
        monthly_volume: int,
        avg_output_tokens: int = 500
    ) -> Dict[str, CostBreakdown]:
        """
        Calculate monthly cost projections for each scenario.
        
        Args:
            scenarios: Token counts per scenario
            monthly_volume: Projected monthly usage
            avg_output_tokens: Average response length
        
        Reference: File 05 (token economics)
        """
        costs = {}
        
        for scenario_name, input_tokens in scenarios.items():
            # Input cost
            input_cost = (input_tokens / 1_000_000) * self.pricing['input']
            
            # Output cost (estimated response)
            output_cost = (avg_output_tokens / 1_000_000) * self.pricing['output']
            
            # Per-use and monthly
            cost_per_use = input_cost + output_cost
            monthly_cost = cost_per_use * monthly_volume
            
            costs[scenario_name] = CostBreakdown(
                scenario=scenario_name,
                tokens=input_tokens,
                cost_per_use=cost_per_use,
                monthly_cost=monthly_cost
            )
        
        return costs
    
    # ========== RECOMMENDATIONS ==========
    
    def generate_recommendations(
        self, 
        breakdown: Dict, 
        scenarios: Dict[str, int]
    ) -> List[str]:
        """
        Generate optimization recommendations.
        
        Analyzes token distribution and suggests improvements.
        Reference: File 15 (optimization strategies)
        """
        recs = []
        
        total_refs = sum(breakdown['level_3_references'].values())
        
        # Check if references dominate
        if total_refs > breakdown['level_2_skill_body'] * 2:
            recs.append(f"âš ï¸  References ({total_refs} tokens) >> SKILL.md. Consider splitting further.")
        
        # Check for large individual references
        for ref_name, tokens in breakdown['level_3_references'].items():
            if tokens > 1000:
                recs.append(f"âš ï¸  {ref_name} is large ({tokens} tokens). Consider splitting.")
        
        # Efficiency praise
        typical = scenarios.get('typical', 0)
        if typical < 500 and not recs:
            recs.append(f"âœ… Excellent efficiency ({typical} tokens typical). Well-optimized!")
        
        if not recs:
            recs.append("âœ… Token efficiency looks good. No optimization needed.")
        
        return recs
    
    # ========== OUTPUT METHODS ==========
    
    def _output_json(self, breakdown: Dict, scenarios: Dict, costs: Dict, recommendations: List, monthly_volume: int) -> str:
        """Generate JSON output for agent-layer."""
        # Convert CostBreakdown objects to dicts
        costs_dict = {}
        for scenario, cost_obj in costs.items():
            costs_dict[scenario] = {
                'tokens': cost_obj.tokens,
                'cost_per_use': round(cost_obj.cost_per_use, 6),
                'monthly_cost': round(cost_obj.monthly_cost, 2)
            }
        
        output = {
            'status': 'success',
            'skill_name': self.skill_path.name,
            'model': self.model,
            'token_breakdown': {
                'level_1_metadata': breakdown['level_1_metadata'],
                'level_2_skill_body': breakdown['level_2_skill_body'],
                'level_3_references': breakdown['level_3_references'],
                'total_references_tokens': sum(breakdown['level_3_references'].values()),
                'scripts': breakdown.get('scripts', [])
            },
            'usage_scenarios': scenarios,
            'cost_analysis': {
                'pricing': {
                    'input': self.pricing['input'],
                    'output': self.pricing['output'],
                    'unit': 'per_million_tokens'
                },
                'scenarios': costs_dict,
                'monthly_volume': monthly_volume
            },
            'recommendations': recommendations
        }
        
        return json.dumps(output, indent=2)
    
    def _output_text(self, breakdown: Dict, scenarios: Dict, costs: Dict, recommendations: List, monthly_volume: int) -> str:
        """Generate text output for human reading."""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"Token Cost Estimation: {self.skill_path.name}")
        lines.append('='*60 + '\n')
        
        # Progressive disclosure breakdown
        lines.append("Progressive Disclosure Breakdown:")
        lines.append(f"â”œâ”€ Level 1 (Metadata): {breakdown['level_1_metadata']} tokens")
        lines.append(f"â”œâ”€ Level 2 (SKILL.md): {breakdown['level_2_skill_body']} tokens")
        
        if breakdown['level_3_references']:
            total_refs = sum(breakdown['level_3_references'].values())
            lines.append(f"â””â”€ Level 3 (References): {total_refs} tokens total")
            for ref_name, tokens in breakdown['level_3_references'].items():
                lines.append(f"   â”œâ”€ {ref_name}: {tokens} tokens")
        else:
            lines.append(f"â””â”€ Level 3: No references")
        
        lines.append("")
        
        # Usage scenarios
        lines.append("Usage Scenarios:")
        lines.append("â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”")
        lines.append("â”‚ Scenario            â”‚ Tokens  â”‚ Frequencyâ”‚")
        lines.append("â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤")
        
        frequency_map = {
            'idle': 'Always',
            'typical': 'Common',
            'with_reference': 'Sometimes',
            'worst_case': 'Rare'
        }
        
        for scenario, tokens in scenarios.items():
            freq = frequency_map.get(scenario, 'Unknown')
            lines.append(f"â”‚ {scenario:19} â”‚ {tokens:7} â”‚ {freq:8} â”‚")
        
        lines.append("â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜")
        lines.append("")
        
        # Cost projections
        lines.append(f"Cost Projection ({self.model}):")
        lines.append(f"â”œâ”€ Input: ${self.pricing['input']:.2f}/M tokens")
        lines.append(f"â”œâ”€ Output: ${self.pricing['output']:.2f}/M tokens")
        lines.append(f"â”‚")
        lines.append(f"â”œâ”€ Per-Use Costs:")
        lines.append(f"â”‚  â”œâ”€ Idle: ${costs['idle'].cost_per_use:.4f} per use")
        lines.append(f"â”‚  â”œâ”€ Typical: ${costs['typical'].cost_per_use:.4f} per use")
        lines.append(f"â”‚  â”œâ”€ With reference: ${costs['with_reference'].cost_per_use:.4f} per use")
        lines.append(f"â”‚  â””â”€ Worst-case: ${costs['worst_case'].cost_per_use:.4f} per use")
        lines.append(f"â”‚")
        lines.append(f"â””â”€ Monthly Projection ({monthly_volume:,} uses/month):")
        
        typical_cost = costs['typical'].monthly_cost
        worst_cost = costs['worst_case'].monthly_cost
        
        lines.append(f"   â”œâ”€ Typical: ${typical_cost:.2f}/month")
        lines.append(f"   â””â”€ Worst-case: ${worst_cost:.2f}/month")
        lines.append("")
        
        # Recommendations
        lines.append("Recommendations:")
        for rec in recommendations:
            lines.append(f"  {rec}")
        
        lines.append("")
        
        return '\n'.join(lines)
    
    # ========== REPORT GENERATION ==========
    
    def generate_report(self, monthly_volume: int = 1000) -> str:
        """Generate comprehensive cost estimation report."""
        # Gather data
        breakdown = self.analyze_progressive_disclosure()
        scenarios = self.estimate_usage_scenarios(breakdown)
        costs = self.calculate_costs(scenarios, monthly_volume)
        recommendations = self.generate_recommendations(breakdown, scenarios)
        
        # Output based on format
        if self.output_format == 'json':
            return self._output_json(breakdown, scenarios, costs, recommendations, monthly_volume)
        else:
            return self._output_text(breakdown, scenarios, costs, recommendations, monthly_volume)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Estimate token costs for Claude skills',
        epilog='References: Files 05, 10, 15 for cost optimization'
    )
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--volume', type=int, default=1000,
                        help='Monthly usage volume (default: 1000)')
    parser.add_argument('--model', default='claude-sonnet-4.5',
                        choices=['claude-sonnet-4.5', 'claude-opus-4'],
                        help='Pricing model (default: claude-sonnet-4.5)')
    add_format_argument(parser)  # Standardized --format argument

    args = parser.parse_args()

    try:
        estimator = TokenEstimator(args.skill_path, model=args.model, output_format=args.format)
        report = estimator.generate_report(monthly_volume=args.volume)
        print(report)
        sys.exit(0)
    
    except FileNotFoundError as e:
        if args.format == 'json':
            response = format_error_response(
                error_type='FileNotFoundError',
                message=str(e),
                tool_name='token_estimator',
                help_text='Ensure skill directory exists and contains SKILL.md'
            )
            output_json(response)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        if args.format == 'json':
            response = format_error_response(
                error_type=type(e).__name__,
                message=str(e),
                tool_name='token_estimator',
                help_text='Check skill structure and permissions'
            )
            output_json(response)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
