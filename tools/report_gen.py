import os
import json
from datetime import datetime

LEDGER_PATH = os.path.join(os.getcwd(), "memory/pm_ledger.jsonl")
QUEUE_PATH = os.path.join(os.getcwd(), "memory/approval_queue.json")
OUTPUT_PATH = os.path.join(os.getcwd(), f"docs/status_report_{datetime.now().strftime('%Y%m%d')}.md")

def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        return []
    with open(LEDGER_PATH, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def load_queue():
    if not os.path.exists(QUEUE_PATH):
        return {"queue": []}
    with open(QUEUE_PATH, "r") as f:
        return json.load(f).get("queue", [])

def generate_report():
    ledger = load_ledger()
    queue = load_queue()
    report = []
    report.append(f"# Status Report - {datetime.now().strftime('%Y-%m-%d')}\n")

    # Summarize approval queue
    report.append("## Tasks Awaiting Approval\n")
    if queue:
        for item in queue:
            report.append(f"- **[{item.get('task_type', 'task')}]** `{item.get('description', '')}` (Submitted: {item.get('submitted_at', '-')}) — *{item.get('status', '-')}")
    else:
        report.append("- No pending approvals.\n")

    # Summarize activity from ledger
    report.append("\n## Recent Activity (Ledger)\n")
    if ledger:
        for entry in ledger[-25:]:
            ts = entry.get("timestamp", "-")
            evt = entry.get("event", "-")
            agt = entry.get("agent", "-")
            tid = entry.get("task_id", "-")
            det = entry.get("details", "")
            report.append(f"- `{ts}` [{evt}] ({agt}) task `{tid}` — {det}")
    else:
        report.append("- Ledger is empty.\n")

    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(report))
    print(f"[ReportGen] Report generated: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_report()
