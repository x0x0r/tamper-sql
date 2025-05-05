#!/usr/bin/env python

"""
Copyright (c) 2006-2023 sqlmap developers (https://sqlmap.org/)
Lihat file 'LICENSE' untuk izin penyalinan
"""

import re
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Memodifikasi payload dengan pola spesifik yang diberikan
    """
    # Pola regex untuk deteksi
    patterns = [
        # Pattern group 1: Time-based functions
        r"(?i)(SLEEP\s*\(\s*5\s*|=SLEEP\s*5|benchmark\([^)]+\)|SELECT\s+SLEEP|RANDOMBLOB\([^)]+\))",
        
        # Pattern group 2: Encoded characters and special syntax
        r"(%5c|%27|%22|%23|%3B|%00|\|\||\b(XOR|OR|AND)\b.*?(SLEEP|BENCHMARK))",
        
        # Pattern group 3: JSON-like patterns
        r"(\"emails\"\s*:\s*\[.*?(SLEEP|BENCHMARK).*?\])",
        
        # Pattern group 4: Mathematical injection patterns
        r"([-+=](0|1)\s*[\'\"XOR].*?(SLEEP|BENCHMARK))"
    ]

    combined_pattern = re.compile("|".join(patterns))

    def replacement(match):
        original = match.group(0).lower()
        
        # Handle time-based functions
        if any(key in original for key in ['sleep', 'benchmark', 'randomblob']):
            if 'randomblob' in original:
                return 'RANDOMBLOB(1)'  # Replace with minimal value
            return '1'  # Replace time-based functions with 1
            
        # Handle encoded characters
        if any(enc in original for enc in ['%5c', '%27', '%22', '%23']):
            return ''  # Remove dangerous encoded characters
            
        # Handle mathematical patterns
        if any(op in original for op in ['xor', 'or ', 'and']):
            return '1'  # Neutralize boolean logic
            
        return '[REMOVED]'  # Default replacement

    return combined_pattern.sub(replacement, payload)
