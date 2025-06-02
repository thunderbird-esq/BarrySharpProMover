import subprocess
import sys

def notify_cli(message):
    try:
        subprocess.call(["./scripts/notify_cli.sh", message])
    except Exception as e:
        print(f"[Notifier] CLI notify failed: {e}")

def notify(message, method="cli"):
    if method == "cli":
        notify_cli(message)
    # Extend for more: elif method == "email": ...

if __name__ == "__main__":
    # Accepts a message argument from LangFlow (or CLI)
    msg = sys.argv[1] if len(sys.argv) > 1 else "[PM] No message specified."
    notify(msg)
