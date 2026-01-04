# Maestro Conductor Skill

A Maestro skill that integrates Gemini CLI's **Conductor** extension methodology for Context-Driven Development.

## Overview

This skill enables Maestro to follow Conductor's structured development workflow:

- **Context-Driven Development**: Maintain project context (product, tech stack, guidelines) that drives all development decisions
- **Spec-First Planning**: Create specifications and plans before writing code
- **Track-Based Organization**: Organize work into "tracks" (features, bugs, chores)
- **TDD Workflow**: Follow Test-Driven Development with clear phases
- **Git-Aware Operations**: Track progress through commits and enable smart reverts

## Installation

Copy the skill files to your Maestro skills directory or reference them in your project.

## Commands

### `/conductor:setup`

Initialize the Conductor environment for a new or existing project.

**Creates:**
- `conductor/product.md` - Product definition and goals
- `conductor/product-guidelines.md` - Brand and communication guidelines
- `conductor/tech-stack.md` - Technology choices and rationale
- `conductor/workflow.md` - Development workflow configuration
- `conductor/code_styleguides/` - Language-specific style guides
- `conductor/tracks.md` - Track registry

### `/conductor:newTrack [description]`

Create a new track (feature, bug fix, or chore) with specification and plan.

**Creates:**
- `conductor/tracks/<track_id>/spec.md` - Detailed requirements
- `conductor/tracks/<track_id>/plan.md` - Phased task breakdown
- `conductor/tracks/<track_id>/metadata.json` - Track metadata

### `/conductor:implement [track_name]`

Execute the tasks in a track's plan following the configured workflow.

**Actions:**
- Selects next pending task
- Follows TDD workflow (Red → Green → Refactor)
- Updates plan status as tasks complete
- Creates git commits with detailed notes
- Triggers phase verification checkpoints

### `/conductor:status`

Display current project and track progress.

**Shows:**
- Overall project status
- Current phase and task
- Progress statistics
- Blockers and next actions

### `/conductor:revert`

Git-aware revert of tracks, phases, or tasks.

**Supports:**
- Interactive target selection
- Git history reconciliation
- Handles rewritten commits
- Plan synchronization after revert

## Project Structure

```
conductor/
├── product.md              # Product definition
├── product-guidelines.md   # Brand/communication guidelines
├── tech-stack.md          # Technology stack
├── workflow.md            # Development workflow
├── tracks.md              # Track registry
├── code_styleguides/      # Style guides by language
│   ├── python.md
│   ├── javascript.md
│   └── ...
├── tracks/                # Individual tracks
│   └── <track_id>/
│       ├── spec.md
│       ├── plan.md
│       └── metadata.json
└── archive/               # Completed/archived tracks
```

## Workflow Principles

1. **Plan is Source of Truth** - All work tracked in `plan.md`
2. **Deliberate Tech Stack** - Changes documented before implementation
3. **Test-Driven Development** - Write tests before code
4. **High Code Coverage** - Target >80% coverage
5. **User Experience First** - Every decision prioritizes UX

## Task Lifecycle

1. Select task from plan
2. Mark as in-progress `[~]`
3. Write failing tests (Red)
4. Implement to pass (Green)
5. Refactor (optional)
6. Verify coverage
7. Commit with git notes
8. Mark complete `[x]` with SHA
9. Phase checkpoints trigger verification

## Integration with Maestro

This skill provides Maestro with:

- **Structured context management** via conductor files
- **Iterative planning** with spec/plan generation
- **Progress tracking** through plan status markers
- **Quality gates** via TDD workflow
- **Audit trail** through git notes and checkpoints

## Credits

Based on [Gemini CLI Conductor](https://github.com/gemini-cli-extensions/conductor) extension.

## License

Apache License 2.0