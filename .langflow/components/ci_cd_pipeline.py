#!/usr/bin/env python3
"""
Continuous Integration/Deployment Pipeline for Barry Sharp Pro Mover
Integrates with the existing build system and adds automated testing, validation, and deployment.
"""

import os
import json
import time
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Optional

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


class CICDPipeline(CustomComponent):
    """
    Automated CI/CD pipeline that watches for changes, runs validation,
    builds the ROM, and optionally deploys or notifies stakeholders.
    """

    display_name = "CI/CD Pipeline"
    description = "Automated build, test, and deployment pipeline for GB Studio projects."

    def __init__(self):
        super().__init__()
        self.project_root = Path.cwd()
        self.build_dir = self.project_root / "build"
        self.memory_dir = self.project_root / "memory"
        self.scripts_dir = self.project_root / "scripts"
        
    def build(
        self,
        trigger_event: str = "manual",
        run_validation: bool = True,
        auto_test: bool = True,
        deploy_target: str = "local",  # local | staging | production
        notify_on_completion: bool = True,
        code: str | None = None,
        **_: object,
    ) -> str:
        """
        Execute the full CI/CD pipeline.
        """
        pipeline_start = datetime.datetime.now()
        pipeline_id = f"pipeline_{int(time.time())}"
        
        try:
            # Log pipeline start
            self._log_event("pipeline_start", {
                "pipeline_id": pipeline_id,
                "trigger": trigger_event,
                "timestamp": pipeline_start.isoformat()
            })
            
            results = {
                "pipeline_id": pipeline_id,
                "status": "running",
                "stages": {}
            }
            
            # Stage 1: Pre-build validation
            if run_validation:
                validation_result = self._run_validation()
                results["stages"]["validation"] = validation_result
                if not validation_result["success"]:
                    results["status"] = "failed"
                    return self._format_results(results)
            
            # Stage 2: Build ROM
            build_result = self._run_build()
            results["stages"]["build"] = build_result
            if not build_result["success"]:
                results["status"] = "failed"
                return self._format_results(results)
            
            # Stage 3: Automated testing
            if auto_test:
                test_result = self._run_tests()
                results["stages"]["test"] = test_result
                if not test_result["success"]:
                    results["status"] = "failed"
                    return self._format_results(results)
            
            # Stage 4: Deployment
            deploy_result = self._deploy(deploy_target)
            results["stages"]["deploy"] = deploy_result
            
            # Stage 5: Notification
            if notify_on_completion:
                notify_result = self._send_notifications(results)
                results["stages"]["notify"] = notify_result
            
            results["status"] = "success"
            results["duration"] = str(datetime.datetime.now() - pipeline_start)
            
            # Log pipeline completion
            self._log_event("pipeline_complete", {
                "pipeline_id": pipeline_id,
                "status": results["status"],
                "duration": results["duration"]
            })
            
            return self._format_results(results)
            
        except Exception as e:
            error_result = {
                "pipeline_id": pipeline_id,
                "status": "error",
                "error": str(e),
                "duration": str(datetime.datetime.now() - pipeline_start)
            }
            self._log_event("pipeline_error", error_result)
            return self._format_results(error_result)
    
    def _run_validation(self) -> Dict:
        """Run pre-build validation checks."""
        try:
            # Run existing validation scripts
            validation_commands = [
                ["make", "check-bg"],
                ["make", "check-scenes"],
                ["make", "check-json"]
            ]
            
            validation_results = []
            for cmd in validation_commands:
                result = subprocess.run(
                    cmd, 
                    cwd=self.project_root,
                    capture_output=True, 
                    text=True
                )
                validation_results.append({
                    "command": " ".join(cmd),
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr
                })
            
            overall_success = all(r["success"] for r in validation_results)
            
            return {
                "success": overall_success,
                "checks": validation_results,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }
    
    def _run_build(self) -> Dict:
        """Execute the build process."""
        try:
            # Call make build-rom to generate the ROM
            result = subprocess.run(
                ["make", "build-rom"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            # Check if ROM was created
            rom_path = self.build_dir / "rom.gb"
            rom_exists = rom_path.exists()
            rom_size = rom_path.stat().st_size if rom_exists else 0
            
            return {
                "success": result.returncode == 0 and rom_exists,
                "rom_created": rom_exists,
                "rom_size": rom_size,
                "build_output": result.stdout,
                "build_error": result.stderr,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }
    
    def _run_tests(self) -> Dict:
        """Run automated tests: Check ROM integrity."""
        try:
            rom_path = self.build_dir / "rom.gb"
            rom_exists = rom_path.exists()
            rom_size = rom_path.stat().st_size if rom_exists else 0
            
            test_passed = rom_exists and rom_size > 0
            
            details = {
                "rom_path": str(rom_path),
                "rom_exists": rom_exists,
                "rom_size_bytes": rom_size,
                "check_passed": test_passed
            }
            
            if not rom_exists:
                details["error_message"] = "ROM file not found at expected location."
            elif rom_size == 0:
                details["error_message"] = "ROM file is empty (0 bytes)."

            return {
                "success": test_passed,
                "details": details,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }
    
    def _deploy(self, target: str) -> Dict:
        """Deploy the built ROM to the specified target."""
        try:
            if target == "local":
                # Local deployment - just ensure ROM is in the right place
                rom_source = self.build_dir / "rom.gb"
                if rom_source.exists():
                    return {
                        "success": True,
                        "target": target,
                        "location": str(rom_source),
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": "ROM file not found",
                        "timestamp": datetime.datetime.now().isoformat()
                    }
            
            elif target == "staging":
                # Copy to staging directory
                staging_dir = self.project_root / "staging"
                staging_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                staged_rom = staging_dir / f"barry_sharp_{timestamp}.gb"
                
                subprocess.run([
                    "cp", 
                    str(self.build_dir / "rom.gb"), 
                    str(staged_rom)
                ], check=True)
                
                return {
                    "success": True,
                    "target": target,
                    "location": str(staged_rom),
                    "timestamp": datetime.datetime.now().isoformat()
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown deployment target: {target}",
                    "timestamp": datetime.datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }
    
    def _send_notifications(self, results: Dict) -> Dict:
        """Send notifications about pipeline completion."""
        try:
            status = results.get("status", "unknown")
            pipeline_id = results.get("pipeline_id", "unknown")
            
            message = f"Pipeline {pipeline_id} completed with status: {status}"
            
            # Use existing notification system
            notify_script = self.scripts_dir / "notify_cli.sh"
            if notify_script.exists():
                subprocess.run([
                    str(notify_script),
                    message
                ], check=True)
            
            return {
                "success": True,
                "message": message,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }
    
    def _log_event(self, event_type: str, data: Dict):
        """Log events to the project ledger."""
        try:
            ledger_path = self.memory_dir / "pm_ledger.jsonl"
            ledger_path.parent.mkdir(exist_ok=True)
            
            log_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "event": event_type,
                "agent": "ci_cd_pipeline",
                "task_id": data.get("pipeline_id", "unknown"),
                "details": data
            }
            
            with open(ledger_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
                
        except Exception as e:
            print(f"Failed to log event: {e}")
    
    def _format_results(self, results: Dict) -> str:
        """Format pipeline results for output."""
        status = results.get("status", "unknown")
        pipeline_id = results.get("pipeline_id", "unknown")
        
        output = [f"# CI/CD Pipeline Results\n"]
        output.append(f"**Pipeline ID:** {pipeline_id}")
        output.append(f"**Status:** {status}")
        
        if "duration" in results:
            output.append(f"**Duration:** {results['duration']}")
        
        if "stages" in results:
            output.append("\n## Stage Results\n")
            for stage_name, stage_data in results["stages"].items():
                stage_status = "✅" if stage_data.get("success", False) else "❌"
                output.append(f"- **{stage_name.title()}:** {stage_status}")
        
        if "error" in results:
            output.append(f"\n**Error:** {results['error']}")
        
        return "\n".join(output)


if __name__ == "__main__":
    # Allow running as standalone script
    pipeline = CICDPipeline()
    result = pipeline.build(trigger_event="manual")
    print(result)