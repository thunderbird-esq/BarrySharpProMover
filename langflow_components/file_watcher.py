import os
import time
import json
import threading

WATCH_INTERVAL = 2  # seconds between scans

# List of directories to watch (edit as needed)
WATCH_DIRS = [
    os.path.join(os.getcwd(), "assets/sprites/"),
    os.path.join(os.getcwd(), "assets/dialogue/"),
    os.path.join(os.getcwd(), "assets/music/"),
    os.path.join(os.getcwd(), "scripts/"),
    os.path.join(os.getcwd(), "docs/")
]

APPROVAL_QUEUE_PATH = os.path.join(os.getcwd(), "memory/approval_queue.json")

def scan_files(dir_path):
    """Recursively list all files in a directory."""
    file_set = set()
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_set.add(os.path.join(root, file))
    return file_set

def load_approval_queue():
    if not os.path.exists(APPROVAL_QUEUE_PATH):
        return {"queue": []}
    with open(APPROVAL_QUEUE_PATH, "r") as f:
        return json.load(f)

def update_approval_queue(new_file):
    queue = load_approval_queue()
    # Prevent duplicate entries
    already_tracked = any(item.get("output_path") == new_file for item in queue["queue"])
    if not already_tracked:
        entry = {
            "task_id": f"auto-{int(time.time())}",
            "agent": "UNKNOWN",
            "task_type": "file_event",
            "description": f"Detected file update: {new_file}",
            "input_path": new_file,
            "output_path": new_file,
            "status": "awaiting_approval",
            "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "comments": ""
        }
        queue["queue"].append(entry)
        with open(APPROVAL_QUEUE_PATH, "w") as f:
            json.dump(queue, f, indent=2)

def watch():
    print("[FileWatcher] Starting up...")
    file_state = {}
    for d in WATCH_DIRS:
        file_state[d] = scan_files(d) if os.path.exists(d) else set()
    while True:
        for d in WATCH_DIRS:
            if not os.path.exists(d):
                continue
            new_state = scan_files(d)
            added = new_state - file_state[d]
            for file_path in added:
                print(f"[FileWatcher] New file detected: {file_path}")
                update_approval_queue(file_path)
            file_state[d] = new_state
        time.sleep(WATCH_INTERVAL)

if __name__ == "__main__":
    t = threading.Thread(target=watch)
    t.daemon = True
    t.start()
    # Block main thread forever
    while True:
        time.sleep(100)

