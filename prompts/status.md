# Conductor Status Protocol

Display the current progress of the project's Conductor tracks.

## Prerequisites Check

Verify these files exist:
- `conductor/tracks.md`
- `conductor/product.md`
- `conductor/tech-stack.md`
- `conductor/workflow.md`

If missing, inform: "Conductor is not set up. Please run `/conductor:setup` first."

## Status Collection

### 1. Read Tracks File

Parse `conductor/tracks.md`:
- Count total tracks
- Count by status: pending `[ ]`, in-progress `[~]`, complete `[x]`
- Identify current track (first non-complete)

### 2. Read Current Track Plan

If there's an in-progress or pending track:
- Read `conductor/tracks/<track_id>/plan.md`
- Count total tasks
- Count by status
- Identify current task and phase

### 3. Generate Status Report

```
═══════════════════════════════════════════════════════════════
                    CONDUCTOR PROJECT STATUS
═══════════════════════════════════════════════════════════════

📅 Timestamp: <current date/time>
📊 Project Status: <On Track | Behind | Blocked>

───────────────────────────────────────────────────────────────
                         TRACK OVERVIEW
───────────────────────────────────────────────────────────────

Total Tracks: <N>
├── ✅ Completed: <N>
├── 🔄 In Progress: <N>
└── ⏳ Pending: <N>

Progress: <completed>/<total> (<percentage>%)

───────────────────────────────────────────────────────────────
                       CURRENT TRACK
───────────────────────────────────────────────────────────────

Track: <description>
Status: <status>
Link: conductor/tracks/<track_id>/

Current Phase: <phase name>
Current Task: <task description>

Tasks: <completed>/<total> (<percentage>%)

───────────────────────────────────────────────────────────────
                        NEXT ACTIONS
───────────────────────────────────────────────────────────────

1. <next pending task>
2. <following task>

───────────────────────────────────────────────────────────────
                         BLOCKERS
───────────────────────────────────────────────────────────────

<list any blockers or "None identified">

═══════════════════════════════════════════════════════════════
```

## Commands Reference

- `/conductor:implement` - Continue implementation
- `/conductor:newTrack` - Create new track
- `/conductor:revert` - Revert work