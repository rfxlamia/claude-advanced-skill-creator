#!/usr/bin/env python3
"""
Standardized output formatting utilities for automation scripts.

Provides consistent JSON/text output patterns across all tools based on
proven patterns from validate_skill.py and quality_scorer.py.

Usage:
    from utils import add_format_argument, output_json, output_error

    parser = argparse.ArgumentParser(...)
    add_format_argument(parser)

    if args.format == 'json':
        output_json(data, tool_name="my_tool")
    else:
        print(human_readable_output)

Version: 1.0
Author: Advanced Skill Creator Project
"""

import json
import sys
from typing import Dict, Any, Optional
from datetime import datetime


def add_format_argument(parser, default='text'):
    """
    Add standardized --format argument to argparse parser.

    Based on proven pattern from validate_skill.py (line 516) and
    quality_scorer.py.

    Args:
        parser: argparse.ArgumentParser instance
        default: Default format ('text' or 'json')

    Example:
        >>> parser = argparse.ArgumentParser(description='My tool')
        >>> add_format_argument(parser)
        >>> args = parser.parse_args()
        >>> print(args.format)  # 'text' or 'json'
    """
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default=default,
        help='Output format: text (human-readable) or json (machine-readable)'
    )


def format_success_response(
    data: Dict[str, Any],
    tool_name: str,
    skill_name: Optional[str] = None,
    skill_path: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create standardized success response structure.

    Based on quality_scorer.py pattern (lines 817-838).

    Args:
        data: Tool-specific result data
        tool_name: Name of the tool (e.g., 'token_estimator', 'validator')
        skill_name: Optional skill name
        skill_path: Optional skill path
        metadata: Optional additional metadata

    Returns:
        Standardized dictionary ready for JSON serialization

    Example:
        >>> response = format_success_response(
        ...     data={'tokens': 500, 'cost': 0.02},
        ...     tool_name='token_estimator',
        ...     skill_name='my-skill'
        ... )
        >>> print(response['status'])
        'success'
    """
    response = {
        'status': 'success',
        'tool': tool_name,
        'timestamp': datetime.now().isoformat(),
        'data': data
    }

    # Add optional fields if provided
    if skill_name:
        response['skill_name'] = skill_name

    if skill_path:
        response['skill_path'] = skill_path

    if metadata:
        response['metadata'] = metadata

    return response


def format_error_response(
    error_type: str,
    message: str,
    tool_name: str,
    help_text: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create standardized error response structure.

    Based on quality_scorer.py pattern (lines 864-874, 876-886).

    Args:
        error_type: Error category (e.g., 'FileNotFound', 'ValidationError')
        message: Error message
        tool_name: Name of the tool
        help_text: Optional helpful guidance for user
        details: Optional additional error details

    Returns:
        Standardized error dictionary ready for JSON serialization

    Example:
        >>> response = format_error_response(
        ...     error_type='FileNotFoundError',
        ...     message='SKILL.md not found',
        ...     tool_name='validator',
        ...     help_text='Ensure skill directory contains SKILL.md'
        ... )
        >>> print(response['status'])
        'error'
    """
    response = {
        'status': 'error',
        'tool': tool_name,
        'timestamp': datetime.now().isoformat(),
        'error_type': error_type,
        'message': message
    }

    if help_text:
        response['help'] = help_text

    if details:
        response['details'] = details

    return response


def output_json(
    response: Dict[str, Any],
    file=None
) -> None:
    """
    Output JSON response to stdout or file.

    Based on quality_scorer.py pattern (line 838).

    Args:
        response: Response dictionary (from format_success_response or format_error_response)
        file: Optional file object (default: sys.stdout)

    Example:
        >>> response = format_success_response(data={'result': 'ok'}, tool_name='my_tool')
        >>> output_json(response)
        {
          "status": "success",
          "tool": "my_tool",
          ...
        }
    """
    if file is None:
        file = sys.stdout

    print(json.dumps(response, indent=2), file=file)


def output_error(
    error_type: str,
    message: str,
    tool_name: str,
    help_text: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    file=None
) -> None:
    """
    Convenience function to format and output error in one call.

    Args:
        error_type: Error category
        message: Error message
        tool_name: Name of the tool
        help_text: Optional helpful guidance
        details: Optional additional details
        file: Optional file object (default: sys.stdout)

    Example:
        >>> output_error(
        ...     error_type='FileNotFoundError',
        ...     message='File not found: skill.md',
        ...     tool_name='validator',
        ...     help_text='Check file path'
        ... )
    """
    response = format_error_response(
        error_type=error_type,
        message=message,
        tool_name=tool_name,
        help_text=help_text,
        details=details
    )
    output_json(response, file=file)


# Convenience function for backward compatibility
def output_success(
    data: Dict[str, Any],
    tool_name: str,
    skill_name: Optional[str] = None,
    skill_path: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    file=None
) -> None:
    """
    Convenience function to format and output success response in one call.

    Args:
        data: Tool-specific result data
        tool_name: Name of the tool
        skill_name: Optional skill name
        skill_path: Optional skill path
        metadata: Optional additional metadata
        file: Optional file object (default: sys.stdout)

    Example:
        >>> output_success(
        ...     data={'score': 85, 'grade': 'B'},
        ...     tool_name='quality_scorer',
        ...     skill_name='my-skill'
        ... )
    """
    response = format_success_response(
        data=data,
        tool_name=tool_name,
        skill_name=skill_name,
        skill_path=skill_path,
        metadata=metadata
    )
    output_json(response, file=file)


# Exit code constants for consistency
class ExitCode:
    """Standardized exit codes across all tools."""
    SUCCESS = 0
    ERROR = 1
    VALIDATION_ERROR = 1
    FILE_NOT_FOUND = 1
    UNEXPECTED_ERROR = 2
