import subprocess
from fastapi import HTTPException

ALLOWED_SCRIPTS = {"process_quote.py", "send_notification.py"}

def run_external_script(script_name: str, args: list):
    if script_name not in ALLOWED_SCRIPTS:
        raise ValueError(f"Script {script_name} not allowed")
    result = subprocess.run(
        ["python", script_name, *args],
        capture_output=True,
        text=True,
        check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"Script failed: {result.stderr}")
    return result.stdout