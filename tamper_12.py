#!/usr/bin/env python

"""
Copyright (c) 2006-2023 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import re
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Neutralizes common SQL injection patterns while maintaining query structure
    """
    # Pattern 1: Encoded characters and special syntax
    encoded_pattern = r"(%27%29%29|%27%27|%60|%60%60|%2C|%22%22|%2F%2F|%5C%5C|%7C%7C|28\s%|%2A%7C|\/\/\*|%7C|29\s%|\*\/\*|\|)"

    # Pattern 2: Basic SQLi patterns with quotes
    basic_sqli = r"([\'\"](?:\s*=\s*[\'\"]|\s*or\s*[\'\"]{1,2}=\s*[\'\"]|[\s-*^&]|or\s*[\'\"]{1,2}[-*^&]|\s*or\s*[\'\"]{1,2}\s))"

    # Pattern 3: Admin bypass patterns
    admin_bypass = r"(admin\s*[\'\"][\s-]*or\s*[\'\"]?\d=\d[\'\"]?[#--/*]*)"

    # Pattern 4: OR true patterns
    or_true = r"(\sor\s+true\s*--|\" or true\s*--|\' or true\s*--|\)\)? or true\s*--)"

    # Pattern 5: x=x patterns
    x_equal = r"([\'\"][\)]*\s*or\s*[\'\"][x]?[\'\"][\)]*\s*=\s*[\'\"][x]?[\'\"]\))"

    # Pattern 6: 1=1 patterns
    one_equal = r"(\sor\s+\d=\d|\d[\'\"]or[\'\"]\d=\d)"

    combined_pattern = re.compile("|".join([
        encoded_pattern,
        basic_sqli,
        admin_bypass,
        or_true,
        x_equal,
        one_equal
    ]), re.IGNORECASE)

    def replacement(match):
        original = match.group(0)
        
        # Handle encoded characters
        if any(enc in original.lower() for enc in ['%27', '%60', '%22', '%2f', '%5c']):
            return ''
            
        # Handle admin bypass
        if 'admin' in original.lower():
            return 'admin'
            
        # Handle or true patterns
        if 'or true' in original.lower():
            return ''
            
        # Handle x=x patterns
        if 'x' in original.lower() and '=' in original:
            return '\'1\'=\'1\''
            
        # Handle 1=1 patterns
        if '1=1' in original or 'or 1=1' in original.lower():
            return '1=1'
            
        # Default: remove dangerous patterns but keep basic structure
        if any(op in original for op in ['*', '|', '^', '&']):
            return ''
            
        return original.split()[0] if original.split() else ''

    # First pass: Handle complex patterns
    payload = combined_pattern.sub(replacement, payload)
    
    # Second pass: Clean up any residual dangerous chars
    payload = re.sub(r"([*|^&\\/])", '', payload)
    
    # Final cleanup of multiple spaces
    payload = re.sub(r"\s+", " ", payload).strip()
    
    return payload
