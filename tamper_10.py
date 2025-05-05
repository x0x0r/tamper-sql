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
    # Regex pattern untuk mendeteksi semua varian yang diberikan
    patterns = [
        r"(?i)(?:'\){0,3}\s*AND\s*1337\s*=\s*BENCHMARK\([^)]+\)[^--]*--?\s*\d*)",
        r"(?i)(?:['\"]\s*AND\s*1337\s*=\s*BENCHMARK\([^)]+\)\s*AND\s*['\"][^=]+=)",
        r"(?i)(?:;?WAITFOR\s+DELAY\s+'0:0:5'[\s--]*)",
        r"(?i)(?:pg_sleep\(\s*5\s*\)[#--]*)",
        r"(?i)(?:DBMS_PIPE\.RECEIVE_MESSAGE\([^)]+,\s*5\))",
        r"(?i)(?:sleep\(\s*5\s*\)[#--]*)",
        r"(?i)(?:SELECT\s+pg_sleep\(\s*5\s*\))"
    ]

    # Gabungkan semua pola menjadi satu regex
    combined_pattern = re.compile("|".join(patterns))

    # Lakukan substitusi
    def replace_match(match):
        original = match.group(0)
        
        # Jika mengandung BENCHMARK, ganti dengan 1=1
        if "BENCHMARK" in original.upper():
            return "1=1"
            
        # Jika mengandung waktu tunggu, ganti dengan operasi kosong
        return ""

    return combined_pattern.sub(replace_match, payload)
