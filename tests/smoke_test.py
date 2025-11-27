"""
Simple smoke tests for the Disaster Management System.
Run: python tests/smoke_test.py
"""
import os
import time
import sys
import requests

BASE = os.environ.get('BASE', 'http://127.0.0.1:8000')

session = requests.Session()


def check_health():
    url = f"{BASE}/api/health"
    print('CHECK:', url)
    r = session.get(url, timeout=5)
    print('status:', r.status_code)
    print('body:', r.text)
    return r.status_code == 200


def signup_and_login():
    timestamp = int(time.time())
    test_email = f"smoketest+{timestamp}@example.com"
    signup_url = f"{BASE}/api/auth/signup"
    login_url = f"{BASE}/api/auth/login"

    payload = {
        'name': 'Smoke Tester',
        'email': test_email,
        'password': 'TestPass123!',
        'phone': '9999999999',
        'role': 'CITIZEN'
    }

    print('POST', signup_url, payload)
    r = session.post(signup_url, json=payload, timeout=5)
    print('signup status:', r.status_code)
    try:
        print('signup body:', r.json())
    except Exception:
        print('signup body:', r.text)

    if r.status_code not in (200, 201):
        return False

    # Now try login
    r2 = session.post(login_url, json={'email': test_email, 'password': payload['password']}, timeout=5)
    print('login status:', r2.status_code)
    try:
        print('login body:', r2.json())
    except Exception:
        print('login body:', r2.text)

    return r2.status_code == 200


if __name__ == '__main__':
    ok = True
    try:
        if not check_health():
            print('Health check failed')
            ok = False
        else:
            print('Health ok')

        if not signup_and_login():
            print('Signup/Login smoke test failed')
            ok = False
        else:
            print('Signup/Login ok')
    except Exception as e:
        print('Exception during tests:', e)
        ok = False

    if ok:
        print('\nSMOKE TESTS PASSED')
        sys.exit(0)
    else:
        print('\nSMOKE TESTS FAILED')
        sys.exit(2)
