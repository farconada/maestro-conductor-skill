# Conductor Revert Protocol

Git-aware revert of Conductor tracks, phases, or tasks.

## Prerequisites Check

Verify `conductor/tracks.md` exists and is not empty.

If missing or empty, inform: "No tracks to revert. Please run `/conductor:setup` first."

## Phase 1: Target Selection

### If target provided as argument:
1. Find exact match in tracks/plans
2. Confirm with user: "You asked to revert '<target>'. Is this correct?"

### If no target provided:
1. Scan all tracks and plans
2. Find in-progress items first (`[~]`)
3. If none, find 5 most recent completed items (`[x]`)
4. Present hierarchical menu:

```
I found the following items. Which would you like to revert?

Track: feature_auth_20240115
  A) [Phase] User Authentication
  B) [Task] Create login form
  
Track: bugfix_nav_20240112
  C) [Task] Fix navigation highlight

D) A different Track, Task, or Phase
```

5. Process user choice and confirm

## Phase 2: Git Reconciliation

### 1. Identify Implementation Commits

For each task/phase in target:
- Find commit SHA recorded in plan.md
- Verify SHA exists in git history
- If SHA not found (rewritten history):
  - Search for commit with similar message
  - Ask user to confirm replacement

### 2. Find Plan Update Commits

For each implementation commit:
- Find corresponding plan.md update commit
- Add to revert list

### 3. For Track Reverts

Additionally find:
- The commit that created the track entry in tracks.md
- Add to revert list

### 4. Analyze Commits

For each commit in list:
- Check for merge commits (warn user)
- Check for cherry-picked duplicates (warn user)
- Compile final ordered list

## Phase 3: Execution Plan

Present clear summary:

```
I have analyzed your request. Here is the plan:

Target: Revert Task 'Create login form'
Commits to Revert: 3
  - abc1234 ('feat(auth): Add login form component')
  - def5678 ('test(auth): Add login form tests')  
  - ghi9012 ('conductor(plan): Mark task complete')

Action: I will run `git revert` on these commits in reverse order.

Do you want to proceed? (yes/no)
```

## Phase 4: Execution

### 1. Execute Reverts

For each commit (most recent first):
```bash
git revert --no-edit <sha>
```

### 2. Handle Conflicts

If merge conflict:
1. HALT
2. Inform user: "Merge conflict detected in <file>. Please resolve manually."
3. Provide resolution guidance
4. Wait for user to confirm resolution

### 3. Verify Plan State

After reverts:
- Read affected plan.md
- Verify reverted items show correct status
- If not, edit plan and commit fix

### 4. Announce Completion

"Revert complete. The following items have been reverted:
- <list of reverted items>

The plan has been synchronized. Git history shows the revert commits."

## Error Handling

- Validate every git command success
- If any command fails, halt and inform user
- Provide recovery suggestions
- Never leave repository in inconsistent state