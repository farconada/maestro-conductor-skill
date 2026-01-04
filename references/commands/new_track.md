# Conductor New Track Protocol

You are creating a new Track (feature, bug fix, or chore) using the Conductor methodology.

## Prerequisites Check

Verify these files exist:
- `conductor/product.md`
- `conductor/tech-stack.md`
- `conductor/workflow.md`

If missing, inform: "Conductor is not set up. Please run `/conductor:setup` first."

## Track Creation Steps

### 1. Get Track Description

If not provided as argument, ask: "Please describe the feature, bug fix, or task you want to work on."

### 2. Determine Track Type

Analyze the description to classify:
- **Feature**: New functionality
- **Bug**: Fix for existing issue
- **Chore**: Maintenance, refactoring, documentation

### 3. Interactive Specification Gathering

Ask 3-5 targeted questions based on track type:

**For Features:**
- What should this feature do?
- What are the inputs and outputs?
- Any UI/UX requirements?
- Integration points with existing code?
- Edge cases to handle?

**For Bugs:**
- Steps to reproduce?
- Expected vs actual behavior?
- Affected components?

**For Chores:**
- What's the scope?
- Success criteria?

### 4. Generate spec.md

Create specification with:
- Overview
- Functional Requirements
- Non-Functional Requirements
- Acceptance Criteria
- Out of Scope

Present to user for approval. Iterate until confirmed.

### 5. Generate plan.md

Based on approved spec and `workflow.md`:
- Create phased task breakdown
- Follow TDD structure (Write Tests → Implement → Refactor)
- Include phase verification tasks
- Use status markers: `[ ]` pending, `[~]` in progress, `[x]` complete

Present to user for approval. Iterate until confirmed.

### 6. Create Track Artifacts

Generate track_id: `shortname_YYYYMMDD`

Create:
```
conductor/tracks/<track_id>/
├── spec.md
├── plan.md
└── metadata.json
```

### 7. Update Tracks File

Append to `conductor/tracks.md`:
```markdown
---

## [ ] Track: <Description>
*Link: [./conductor/tracks/<track_id>/](./conductor/tracks/<track_id>/)*
```

### 8. Completion

Announce: "Track '<track_id>' created! Run `/conductor:implement` to start working on it."