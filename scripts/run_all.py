from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import sys

CASES = (9964, 9974, 9771, 9894, 9846, 9834, 8464, 9916)


def run(number):
    subprocess.run([sys.executable, 'scripts/diagnose.py'], check=True, env={**os.environ, 'CASE_ID': str(number)})


with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(run, CASES))
