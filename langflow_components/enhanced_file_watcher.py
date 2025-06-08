#!/usr/bin/env python3
"""
Enhanced File Watcher for Barry Sharp Pro Mover
Monitors project files and automatically triggers CI/CD pipeline when changes are detected.
"""

import os
import json
import time
import hashlib
import threading
from pathlib import Path
from typing import Dict, Set, List, Optional
from datetime import datetime

# LangFlow 1.4.x locates CustomComponent here ↓
try:
    from langflow.components.base.custom import CustomComponent
    LANGFLOW_AVAILABLE = True
except ImportError:
    # Fallback for standalone usage
    class CustomComponent:
        def __init__(self):
            pass
    LANGFLOW_AVAILABLE = False


class EnhancedFileWatcher(CustomComponent):
    """
    Advanced file watcher that monitors multiple directories and triggers
    automated workflows based on file changes.
    """

    display_name = "Enhanced File Watcher"
    description = "Monitors project files and triggers automated CI/CD workflows on changes."

    def __init__(self):
        super().__init__()
        self.project_root = Path.cwd()
        self.memory_dir = self.project_root / "memory"
        self.is_watching = False
        self.watch_thread = None
        self.file_hashes = {}
        
    def build(
        self,
        watch_directories: List[str] = None,
        ignore_patterns: List[str] = None,
        auto_trigger_pipeline: bool = True,
        debounce_seconds: int = 5,
        watch_duration: int = 0,  # 0 = infinite
        code: str | None = None,
        **_: object,
    ) -> str:
        """
        Start enhanced file watching with automatic pipeline triggering.
        """
        if watch_directories is None:
            watch_directories = [
                "assets/sprites/",
                "assets/backgrounds/",
                "assets/music/",
                "assets/sounds/",
                "scripts/",
                "docs/",
                "BARRY-SHARP-PRO-MOVER-1.gbsproj"
            ]
        
        if ignore_patterns is None:
            ignore_patterns = [
                "*.tmp",
                "*.bak",
                "*~",
                ".DS_Store",
                "*.swp",
                "*.swo",
                "build/*",
                "memory/*",
                ".git/*"
            ]
        
        try:
            # Initialize file hash cache
            self._initialize_file_cache(watch_directories, ignore_patterns)
            
            # Start watching
            self.is_watching = True
            self.watch_thread = threading.Thread(
                target=self._watch_loop,
                args=(watch_directories, ignore_patterns, auto_trigger_pipeline, debounce_seconds, watch_duration)
            )
            self.watch_thread.daemon = True
            self.watch_thread.start()
            
            # Log watcher start
            self._log_event("watcher_start", {
                "directories": watch_directories,
                "auto_trigger": auto_trigger_pipeline,
                "debounce": debounce_seconds
            })
            
            return f"""# Enhanced File Watcher Started

**Status:** Active
**Watching:** {len(watch_directories)} directories
**Auto-trigger CI/CD:** {'Yes' if auto_trigger_pipeline else 'No'}
**Debounce:** {debounce_seconds} seconds
**Duration:** {'Infinite' if watch_duration == 0 else f'{watch_duration} seconds'}

## Monitored Directories
{chr(10).join(f'- {d}' for d in watch_directories)}

## Ignored Patterns
{chr(10).join(f'- {p}' for p in ignore_patterns)}

Watcher is running in background thread.
"""
            
        except Exception as e:
            return f"**Error starting file watcher:** {str(e)}"
    
    def stop_watching(self) -> str:
        """Stop the file watcher."""
        self.is_watching = False
        if self.watch_thread and self.watch_thread.is_alive():
            self.watch_thread.join(timeout=5)
        
        self._log_event("watcher_stop", {})
        return "File watcher stopped."
    
    def _initialize_file_cache(self, watch_directories: List[str], ignore_patterns: List[str]):
        """Initialize the file hash cache for change detection."""
        self.file_hashes = {}
        
        for watch_dir in watch_directories:
            full_path = self.project_root / watch_dir
            
            if full_path.is_file():
                # Single file
                if not self._should_ignore(str(full_path), ignore_patterns):
                    self.file_hashes[str(full_path)] = self._get_file_hash(full_path)
            elif full_path.is_dir():
                # Directory - scan recursively
                for file_path in full_path.rglob("*"):
                    if file_path.is_file() and not self._should_ignore(str(file_path), ignore_patterns):
                        self.file_hashes[str(file_path)] = self._get_file_hash(file_path)
    
    def _watch_loop(self, watch_directories: List[str], ignore_patterns: List[str], 
                   auto_trigger_pipeline: bool, debounce_seconds: int, watch_duration: int):
        """Main watching loop."""
        start_time = time.time()
        last_change_time = 0
        pending_changes = set()
        
        while self.is_watching:
            try:
                # Check if we should stop based on duration
                if watch_duration > 0 and (time.time() - start_time) > watch_duration:
                    break
                
                # Scan for changes
                current_changes = self._scan_for_changes(watch_directories, ignore_patterns)
                
                if current_changes:
                    pending_changes.update(current_changes)
                    last_change_time = time.time()
                    
                    # Log detected changes
                    self._log_event("files_changed", {
                        "files": list(current_changes),
                        "count": len(current_changes)
                    })
                
                # Check if debounce period has passed and we have pending changes
                if (pending_changes and 
                    time.time() - last_change_time >= debounce_seconds):
                    
                    # Process the changes
                    self._process_changes(list(pending_changes), auto_trigger_pipeline)
                    pending_changes.clear()
                
                # Sleep before next scan
                time.sleep(1)
                
            except Exception as e:
                self._log_event("watcher_error", {"error": str(e)})
                time.sleep(5)  # Wait longer on error
        
        self._log_event("watcher_stopped", {})
    
    def _scan_for_changes(self, watch_directories: List[str], ignore_patterns: List[str]) -> Set[str]:
        """Scan watched directories for file changes."""
        changes = set()
        current_files = {}
        
        # Scan all watched locations
        for watch_dir in watch_directories:
            full_path = self.project_root / watch_dir
            
            if full_path.is_file():
                if not self._should_ignore(str(full_path), ignore_patterns):
                    current_files[str(full_path)] = self._get_file_hash(full_path)
            elif full_path.is_dir():
                for file_path in full_path.rglob("*"):
                    if file_path.is_file() and not self._should_ignore(str(file_path), ignore_patterns):
                        current_files[str(file_path)] = self._get_file_hash(file_path)
        
        # Compare with cached hashes
        for file_path, current_hash in current_files.items():
            cached_hash = self.file_hashes.get(file_path)
            if cached_hash != current_hash:
                changes.add(file_path)
                self.file_hashes[file_path] = current_hash
        
        # Check for deleted files
        for cached_file in list(self.file_hashes.keys()):
            if cached_file not in current_files:
                changes.add(cached_file)
                del self.file_hashes[cached_file]
        
        return changes
    
    def _process_changes(self, changed_files: List[str], auto_trigger_pipeline: bool):
        """Process detected file changes."""
        try:
            # Categorize changes
            asset_changes = [f for f in changed_files if "/assets/" in f]
            script_changes = [f for f in changed_files if "/scripts/" in f]
            project_changes = [f for f in changed_files if f.endswith(".gbsproj")]
            doc_changes = [f for f in changed_files if "/docs/" in f]
            
            # Create approval queue entry
            self._create_approval_entry({
                "asset_changes": asset_changes,
                "script_changes": script_changes,
                "project_changes": project_changes,
                "doc_changes": doc_changes,
                "total_changes": len(changed_files)
            })
            
            # Auto-trigger pipeline if enabled and we have significant changes
            if auto_trigger_pipeline and (asset_changes or script_changes or project_changes):
                self._trigger_pipeline(changed_files)
            
        except Exception as e:
            self._log_event("process_changes_error", {"error": str(e)})
    
    def _trigger_pipeline(self, changed_files: List[str]):
        """Trigger the CI/CD pipeline."""
        try:
            # Import and run the CI/CD pipeline
            from .ci_cd_pipeline import CICDPipeline
            
            pipeline = CICDPipeline()
            result = pipeline.build(
                trigger_event="file_change",
                run_validation=True,
                auto_test=True,
                deploy_target="local",
                notify_on_completion=True
            )
            
            self._log_event("pipeline_triggered", {
                "trigger_files": changed_files,
                "pipeline_result": "success" if "success" in result else "failed"
            })
            
        except Exception as e:
            self._log_event("pipeline_trigger_error", {"error": str(e)})
    
    def _create_approval_entry(self, change_summary: Dict):
        """Create an entry in the approval queue for detected changes."""
        try:
            queue_path = self.memory_dir / "approval_queue.json"
            queue_path.parent.mkdir(exist_ok=True)
            
            # Load existing queue
            if queue_path.exists():
                with open(queue_path, "r") as f:
                    queue_data = json.load(f)
            else:
                queue_data = {"queue": []}
            
            # Create new entry
            entry = {
                "task_id": f"file_change_{int(time.time())}",
                "agent": "enhanced_file_watcher",
                "task_type": "file_change_detection",
                "description": f"Detected {change_summary['total_changes']} file changes",
                "details": change_summary,
                "status": "detected",
                "submitted_at": datetime.now().isoformat(),
                "comments": ""
            }
            
            queue_data["queue"].append(entry)
            
            # Save updated queue
            with open(queue_path, "w") as f:
                json.dump(queue_data, f, indent=2)
                
        except Exception as e:
            self._log_event("approval_entry_error", {"error": str(e)})
    
    def _should_ignore(self, file_path: str, ignore_patterns: List[str]) -> bool:
        """Check if a file should be ignored based on patterns."""
        import fnmatch
        
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(os.path.basename(file_path), pattern):
                return True
        return False
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of a file for change detection."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return "error"
    
    def _log_event(self, event_type: str, data: Dict):
        """Log events to the project ledger."""
        try:
            ledger_path = self.memory_dir / "pm_ledger.jsonl"
            ledger_path.parent.mkdir(exist_ok=True)
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event": event_type,
                "agent": "enhanced_file_watcher",
                "task_id": f"watcher_{int(time.time())}",
                "details": data
            }
            
            with open(ledger_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
                
        except Exception as e:
            print(f"Failed to log event: {e}")


if __name__ == "__main__":
    # Allow running as standalone script
    watcher = EnhancedFileWatcher()
    result = watcher.build(watch_duration=30)  # Watch for 30 seconds
    print(result)
    time.sleep(35)
    print(watcher.stop_watching())