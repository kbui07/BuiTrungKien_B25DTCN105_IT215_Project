import time

login_attempts = {}

MAX_ATTEMPTS = 5
WINDOW = 60


def check_login_rate_limit(ip: str):

    now = time.time()

    if ip not in login_attempts:
        login_attempts[ip] = []

    login_attempts[ip] = [
        attempt
        for attempt in login_attempts[ip]
        if now - attempt < WINDOW
    ]

    if len(login_attempts[ip]) >= MAX_ATTEMPTS:
        return False

    login_attempts[ip].append(now)

    return True