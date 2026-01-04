---
name: maestro-conductor
description: |
  Context-Driven Development skill that integrates Conductor methodology for structured software development. 
  Use this skill when you need to: set up a new project with product/tech-stack context, create feature or bug 
  fix specifications (tracks), implement tasks following TDD workflow (Red-Green-Refactor), track progress 
  through phases and tasks, or revert changes with git-aware operations. Ideal for teams wanting structured, 
  spec-first development with quality gates and checkpoints.
license: Apache-2.0
compatibility: |
  Requires git for version control and checkpoint operations. Works with any programming language.
  Optimal for projects using test frameworks that support coverage reporting.
metadata:
  version: "1.0.0"
  author: "farconada"
  repository: "https://github.com/farconada/maestro-conductor-skill"
  based-on: "https://github.com/gemini-cli-extensions/conductor"
---

# Maestro Conductor Skill

A Context-Driven Development methodology that ensures every coding task follows a structured lifecycle: **Context → Spec & Plan → Implement**.

## When to Use This Skill

Activate this skill when the user wants to:
- Set up a new project with structured context (product definition, tech stack, guidelines)
- Create a new feature, bug fix, or chore with specifications
- Implement tasks following Test-Driven Development
- Check project or track progress
- Revert completed work at track, phase, or task level

## Core Concepts

### Tracks
A **Track** is a high-level unit of work (feature, bug, or chore). Each track contains:
- `spec.md` - Detailed requirements and acceptance criteria
- `plan.md` - Phased task breakdown with status markers
- `metadata.json` - Track metadata (type, status, timestamps)

### Status Markers
- `[ ]` Pending
- `[~]` In Progress
- `[x]` Complete

### TDD Workflow
Every task follows Red-Green-Refactor:
1. **Red**: Write failing tests
2. **Green**: Implement minimum code to pass
3. **Refactor**: Improve code quality

## Commands

### Setup (`/conductor:setup`)

Initialize the Conductor environment. Creates:
- `conductor/product.md` - Product definition
- `conductor/product-guidelines.md` - Brand/communication guidelines
- `conductor/tech-stack.md` - Technology choices
- `conductor/workflow.md` - Development workflow configuration
- `conductor/tracks.md` - Track registry

**Process:**
1. Detect project type (greenfield vs brownfield)
2. Ask interactive questions about product, guidelines, tech stack
3. Configure workflow preferences (TDD, coverage target, commit frequency)
4. Generate initial track

### New Track (`/conductor:newTrack [description]`)

Create a new track with specification and plan.

**Process:**
1. Get track description (from argument or ask user)
2. Classify track type (feature/bug/chore)
3. Ask 3-5 targeted questions based on type
4. Generate `spec.md` and get user approval
5. Generate `plan.md` following workflow.md structure
6. Create track directory with artifacts

**Output structure:**
```
conductor/tracks/<track_id>/
├── spec.md
├── plan.md
└── metadata.json
```

### Implement (`/conductor:implement [track_name]`)

Execute tasks following the TDD workflow.

**Process for each task:**
1. Mark task as in-progress `[~]`
2. Write failing tests (Red phase)
3. Implement to pass tests (Green phase)
4. Refactor if needed
5. Verify coverage >80%
6. Commit with structured message: `feat(<scope>): <description>`
7. Attach git note with task summary
8. Mark complete `[x]` with commit SHA

**Phase completion triggers:**
- Run full test suite
- Present manual verification plan
- Await user confirmation
- Create checkpoint commit
- Attach verification report via git note

### Status (`/conductor:status`)

Display project progress.

**Output includes:**
- Overall track counts (completed/in-progress/pending)
- Current track and task
- Progress percentage
- Next actions needed
- Any blockers

### Revert (`/conductor:revert`)

Git-aware revert of tracks, phases, or tasks.

**Process:**
1. Present menu of in-progress or recently completed items
2. User selects target to revert
3. Identify all related commits (implementation + plan updates)
4. Present execution plan
5. Execute `git revert` in correct order
6. Synchronize plan.md status

## File References

For detailed workflow rules, see: `references/workflow.md`

For Python implementation utilities, see: `scripts/conductor_skill.py`

For project templates, see:
- `assets/templates/product.md`
- `assets/templates/product-guidelines.md`
- `assets/templates/tech-stack.md`
- `assets/templates/workflow.md`

## Quality Gates

Before marking any task complete, verify:
- All tests pass
- Code coverage >80%
- Code follows project style guidelines
- Public functions documented
- No linting errors
- Documentation updated if needed

## Example Session

```
User: /conductor:setup

Agent: I've detected a new project. Let me ask some questions...
       What are you building?

User: A task management API

Agent: Who are the target users?
       A) Internal development teams
       B) External customers via SDK
       C) Both
       D) Type your own answer

User: A

[... continues with interactive setup ...]

Agent: ✅ Setup complete. Run /conductor:implement to start.

---

User: /conductor:newTrack "User authentication with JWT"

Agent: I'll create a specification for this feature...
       [Asks clarifying questions]
       [Generates spec.md]
       Does this look correct?

User: Yes

Agent: ✅ Track 'auth_jwt_20260104' created.

---

User: /conductor:implement

Agent: Starting track: User authentication with JWT
       
       📋 Task: Create user model
       🔴 Writing tests...
       [Creates test_user_model.py]
       Running tests... ❌ 1 failed (expected)
       
       🟢 Implementing...
       [Creates user_model.py]
       Running tests... ✅ All passed
       
       📊 Coverage: 87%
       💾 Committed: feat(auth): Add user model [abc1234]
       
       ✅ Task complete
```

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Plan updates use: `conductor(plan): <description>`
Checkpoints use: `conductor(checkpoint): <description>`