"""
Maestro Conductor Skill

Integrates Gemini CLI's Conductor methodology for Context-Driven Development.
Provides structured project setup, track management, and TDD workflow execution.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any


class ConductorSkill:
    """
    Maestro skill for Conductor-based Context-Driven Development.
    
    Conductor organizes development into:
    - Project context (product, tech-stack, workflow, guidelines)
    - Tracks (features, bugs, chores) with specs and plans
    - TDD-driven task execution with git integration
    """
    
    CONDUCTOR_DIR = "conductor"
    TRACKS_DIR = "conductor/tracks"
    ARCHIVE_DIR = "conductor/archive"
    
    # Required files for a properly configured project
    REQUIRED_FILES = [
        "conductor/product.md",
        "conductor/tech-stack.md", 
        "conductor/workflow.md"
    ]
    
    # Status markers
    STATUS_PENDING = "[ ]"
    STATUS_IN_PROGRESS = "[~]"
    STATUS_COMPLETE = "[x]"
    
    def __init__(self, project_root: str = "."):
        """Initialize the Conductor skill with project root path."""
        self.project_root = Path(project_root)
        
    # =========================================================================
    # Setup Operations
    # =========================================================================
    
    def is_setup_complete(self) -> bool:
        """Check if Conductor environment is properly set up."""
        for filepath in self.REQUIRED_FILES:
            if not (self.project_root / filepath).exists():
                return False
        return True
    
    def get_setup_state(self) -> Optional[Dict[str, Any]]:
        """Read the setup state file if it exists."""
        state_file = self.project_root / self.CONDUCTOR_DIR / "setup_state.json"
        if state_file.exists():
            return json.loads(state_file.read_text())
        return None
    
    def save_setup_state(self, last_successful_step: str) -> None:
        """Save the setup state to track progress."""
        state_file = self.project_root / self.CONDUCTOR_DIR / "setup_state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps({
            "last_successful_step": last_successful_step
        }))
    
    def detect_project_type(self) -> str:
        """
        Detect if project is Greenfield (new) or Brownfield (existing).
        
        Returns: "greenfield" or "brownfield"
        """
        brownfield_indicators = [
            ".git", ".svn", ".hg",  # Version control
            "package.json", "pom.xml", "requirements.txt", "go.mod",  # Dependencies
            "src", "app", "lib"  # Source directories
        ]
        
        for indicator in brownfield_indicators:
            if (self.project_root / indicator).exists():
                return "brownfield"
        
        return "greenfield"
    
    def create_conductor_directory(self) -> None:
        """Create the conductor directory structure."""
        dirs = [
            self.CONDUCTOR_DIR,
            f"{self.CONDUCTOR_DIR}/code_styleguides",
            self.TRACKS_DIR,
        ]
        for d in dirs:
            (self.project_root / d).mkdir(parents=True, exist_ok=True)
    
    # =========================================================================
    # Track Operations
    # =========================================================================
    
    def generate_track_id(self, description: str) -> str:
        """Generate a unique track ID from description."""
        # Create short name from description
        words = description.lower().split()[:3]
        short_name = "_".join(w for w in words if w.isalnum())
        date_str = datetime.now().strftime("%Y%m%d")
        return f"{short_name}_{date_str}"
    
    def get_tracks(self) -> List[Dict[str, Any]]:
        """Parse and return all tracks from tracks.md."""
        tracks_file = self.project_root / self.CONDUCTOR_DIR / "tracks.md"
        if not tracks_file.exists():
            return []
        
        content = tracks_file.read_text()
        tracks = []
        
        # Split by --- separator
        sections = content.split("---")
        
        for section in sections[1:]:  # Skip header section
            section = section.strip()
            if not section:
                continue
                
            # Parse track status and description
            for line in section.split("\n"):
                line = line.strip()
                if line.startswith("## "):
                    # Extract status
                    if "[ ]" in line:
                        status = "pending"
                    elif "[~]" in line:
                        status = "in_progress"
                    elif "[x]" in line:
                        status = "complete"
                    else:
                        status = "unknown"
                    
                    # Extract description (after "Track: ")
                    if "Track:" in line:
                        desc = line.split("Track:")[-1].strip()
                    else:
                        desc = line.lstrip("#").strip()
                    
                    tracks.append({
                        "description": desc,
                        "status": status,
                        "raw_line": line
                    })
                
                elif line.startswith("*Link:"):
                    # Extract track folder link
                    if tracks:
                        # Parse link from markdown format
                        import re
                        match = re.search(r'\[([^\]]+)\]', line)
                        if match:
                            tracks[-1]["link"] = match.group(1)
        
        return tracks
    
    def get_next_pending_track(self) -> Optional[Dict[str, Any]]:
        """Get the next track that is not completed."""
        tracks = self.get_tracks()
        for track in tracks:
            if track["status"] != "complete":
                return track
        return None
    
    def create_track(self, description: str, track_type: str = "feature") -> str:
        """
        Create a new track with directory structure.
        
        Returns the track_id.
        """
        track_id = self.generate_track_id(description)
        track_dir = self.project_root / self.TRACKS_DIR / track_id
        track_dir.mkdir(parents=True, exist_ok=True)
        
        # Create metadata.json
        metadata = {
            "track_id": track_id,
            "type": track_type,
            "status": "new",
            "created_at": datetime.now().isoformat() + "Z",
            "updated_at": datetime.now().isoformat() + "Z",
            "description": description
        }
        (track_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
        
        return track_id
    
    def update_track_status(self, track_description: str, new_status: str) -> bool:
        """Update a track's status in tracks.md."""
        tracks_file = self.project_root / self.CONDUCTOR_DIR / "tracks.md"
        if not tracks_file.exists():
            return False
        
        content = tracks_file.read_text()
        
        # Map status to marker
        status_map = {
            "pending": "[ ]",
            "in_progress": "[~]",
            "complete": "[x]"
        }
        new_marker = status_map.get(new_status, "[ ]")
        
        # Find and replace the track line
        lines = content.split("\n")
        updated = False
        
        for i, line in enumerate(lines):
            if track_description in line and line.strip().startswith("## "):
                # Replace status marker
                for old_marker in ["[ ]", "[~]", "[x]"]:
                    if old_marker in line:
                        lines[i] = line.replace(old_marker, new_marker)
                        updated = True
                        break
        
        if updated:
            tracks_file.write_text("\n".join(lines))
        
        return updated
    
    # =========================================================================
    # Plan Operations
    # =========================================================================
    
    def get_plan_tasks(self, track_id: str) -> List[Dict[str, Any]]:
        """Parse tasks from a track's plan.md."""
        plan_file = self.project_root / self.TRACKS_DIR / track_id / "plan.md"
        if not plan_file.exists():
            return []
        
        content = plan_file.read_text()
        tasks = []
        current_phase = None
        
        for line in content.split("\n"):
            line_stripped = line.strip()
            
            # Detect phase headers
            if line_stripped.startswith("## "):
                current_phase = line_stripped.lstrip("#").strip()
                continue
            
            # Detect tasks (lines starting with - [ ], - [~], or - [x])
            if line_stripped.startswith("- [ ]") or \
               line_stripped.startswith("- [~]") or \
               line_stripped.startswith("- [x]"):
                
                # Extract status
                if "[ ]" in line_stripped:
                    status = "pending"
                elif "[~]" in line_stripped:
                    status = "in_progress"
                else:
                    status = "complete"
                
                # Extract task description
                desc = line_stripped.split("]", 1)[-1].strip()
                
                tasks.append({
                    "phase": current_phase,
                    "description": desc,
                    "status": status,
                    "raw_line": line
                })
        
        return tasks
    
    def get_next_pending_task(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Get the next pending task in a track's plan."""
        tasks = self.get_plan_tasks(track_id)
        for task in tasks:
            if task["status"] == "pending":
                return task
        return None
    
    def update_task_status(self, track_id: str, task_description: str, 
                          new_status: str, commit_sha: Optional[str] = None) -> bool:
        """Update a task's status in plan.md."""
        plan_file = self.project_root / self.TRACKS_DIR / track_id / "plan.md"
        if not plan_file.exists():
            return False
        
        content = plan_file.read_text()
        
        # Map status to marker
        status_map = {
            "pending": "[ ]",
            "in_progress": "[~]",
            "complete": "[x]"
        }
        new_marker = status_map.get(new_status, "[ ]")
        
        lines = content.split("\n")
        updated = False
        
        for i, line in enumerate(lines):
            if task_description in line:
                for old_marker in ["[ ]", "[~]", "[x]"]:
                    if old_marker in line:
                        new_line = line.replace(old_marker, new_marker)
                        # Append SHA if provided and marking complete
                        if commit_sha and new_status == "complete":
                            new_line = f"{new_line} [{commit_sha[:7]}]"
                        lines[i] = new_line
                        updated = True
                        break
        
        if updated:
            plan_file.write_text("\n".join(lines))
        
        return updated
    
    # =========================================================================
    # Status Operations
    # =========================================================================
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get comprehensive project status."""
        if not self.is_setup_complete():
            return {
                "setup_complete": False,
                "message": "Conductor is not set up. Run /conductor:setup first."
            }
        
        tracks = self.get_tracks()
        
        total_tracks = len(tracks)
        completed_tracks = len([t for t in tracks if t["status"] == "complete"])
        in_progress_tracks = len([t for t in tracks if t["status"] == "in_progress"])
        pending_tracks = len([t for t in tracks if t["status"] == "pending"])
        
        # Find current track
        current_track = None
        for track in tracks:
            if track["status"] == "in_progress":
                current_track = track
                break
        
        if not current_track:
            for track in tracks:
                if track["status"] == "pending":
                    current_track = track
                    break
        
        return {
            "setup_complete": True,
            "timestamp": datetime.now().isoformat(),
            "tracks": {
                "total": total_tracks,
                "completed": completed_tracks,
                "in_progress": in_progress_tracks,
                "pending": pending_tracks
            },
            "current_track": current_track,
            "progress_percentage": (completed_tracks / total_tracks * 100) if total_tracks > 0 else 0
        }
    
    # =========================================================================
    # File Generation Templates
    # =========================================================================
    
    def generate_tracks_file_header(self) -> str:
        """Generate the initial tracks.md header."""
        return """# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.
"""
    
    def generate_track_entry(self, track_id: str, description: str) -> str:
        """Generate a track entry for tracks.md."""
        return f"""
---

## [ ] Track: {description}
*Link: [./conductor/tracks/{track_id}/](./conductor/tracks/{track_id}/)*
"""
    
    def generate_spec_template(self, description: str, requirements: List[str]) -> str:
        """Generate a spec.md template."""
        req_list = "\n".join(f"- {r}" for r in requirements) if requirements else "- TBD"
        
        return f"""# Specification: {description}

## Overview

{description}

## Functional Requirements

{req_list}

## Non-Functional Requirements

- Performance: TBD
- Security: TBD
- Accessibility: TBD

## Acceptance Criteria

- [ ] All functional requirements implemented
- [ ] All tests passing
- [ ] Code coverage >80%
- [ ] Documentation updated

## Out of Scope

- TBD
"""
    
    def generate_plan_template(self, description: str, phases: List[Dict]) -> str:
        """Generate a plan.md template."""
        plan_content = f"""# Implementation Plan: {description}

## Status Legend
- `[ ]` Pending
- `[~]` In Progress  
- `[x]` Complete

"""
        for phase in phases:
            plan_content += f"\n## {phase['name']}\n\n"
            for task in phase.get("tasks", []):
                plan_content += f"- [ ] {task}\n"
            # Add phase verification task
            plan_content += f"- [ ] Task: Conductor - User Manual Verification '{phase['name']}' (Protocol in workflow.md)\n"
        
        return plan_content


# Convenience functions for direct usage
def setup_conductor(project_root: str = ".") -> ConductorSkill:
    """Initialize Conductor for a project."""
    skill = ConductorSkill(project_root)
    skill.create_conductor_directory()
    return skill


def get_status(project_root: str = ".") -> Dict[str, Any]:
    """Get project status."""
    skill = ConductorSkill(project_root)
    return skill.get_project_status()