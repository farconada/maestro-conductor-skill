# Conductor Implement Protocol

You are implementing a Track using the Conductor TDD workflow.

## Prerequisites Check

Verify these files exist:
- `conductor/product.md`
- `conductor/tech-stack.md`
- `conductor/workflow.md`

If missing, inform: "Conductor is not set up. Please run `/conductor:setup` first."

## Track Selection

### If track name provided:
Find matching track in `conductor/tracks.md` (case-insensitive).

### If no track name:
1. Find first incomplete track (not `[x]`)
2. Announce: "Selecting next incomplete track: '<description>'"

### If no incomplete tracks:
Announce: "All tracks are complete! Create a new track with `/conductor:newTrack`."

## Implementation Loop

### 1. Load Track Context

Read:
- `conductor/tracks/<track_id>/plan.md`
- `conductor/tracks/<track_id>/spec.md`
- `conductor/workflow.md`

### 2. Update Track Status

Change track status to `[~]` in `conductor/tracks.md`.

### 3. For Each Task in Plan

**a. Select Next Pending Task**
Find first `[ ]` task in plan.md.

**b. Mark In Progress**
Change task from `[ ]` to `[~]`.

**c. Execute TDD Workflow**

1. **Red Phase**: Write failing tests
   - Create test file for the task
   - Write tests defining expected behavior
   - Run tests - confirm they FAIL

2. **Green Phase**: Implement to pass
   - Write minimum code to pass tests
   - Run tests - confirm they PASS

3. **Refactor Phase** (optional):
   - Improve code quality
   - Ensure tests still pass

**d. Verify Coverage**
Run coverage tool, target >80%.

**e. Commit Changes**
```bash
git add .
git commit -m "feat(<scope>): <description>"
```

**f. Attach Git Note**
```bash
SHA=$(git log -1 --format="%H")
git notes add -m "Task: <name>\nChanges: <summary>\nFiles: <list>" $SHA
```

**g. Update Plan**
- Mark task `[x]` with SHA: `[x] Task description [abc1234]`
- Commit plan update: `conductor(plan): Mark task 'name' complete`

### 4. Phase Completion

When a phase completes:

1. **Ensure Test Coverage**
   - Identify files changed in phase
   - Verify test files exist
   - Create missing tests

2. **Run All Tests**
   - Execute test suite
   - Debug failures (max 2 attempts, then ask user)

3. **Manual Verification**
   - Present step-by-step verification plan
   - Ask: "Does this meet your expectations?"
   - Wait for explicit confirmation

4. **Create Checkpoint**
   ```bash
   git add .
   git commit -m "conductor(checkpoint): End of Phase X"
   ```

5. **Attach Verification Report**
   - Document test results
   - Document user confirmation
   - Attach as git note

6. **Update Plan**
   - Add checkpoint SHA to phase header
   - Commit plan update

### 5. Track Completion

When all tasks complete:

1. Update track status to `[x]` in `conductor/tracks.md`
2. Sync project documentation (product.md, tech-stack.md) if needed
3. Offer cleanup options:
   - **Archive**: Move to `conductor/archive/`
   - **Delete**: Remove permanently (with confirmation)
   - **Skip**: Keep in tracks file

## Error Handling

- If any operation fails, halt and inform user
- Provide clear error messages
- Suggest recovery actions