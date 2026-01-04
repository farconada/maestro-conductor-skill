# Maestro Conductor Skill

A Maestro skill following the [Agent Skills specification](https://agentskills.io/specification) that integrates Gemini CLI's **Conductor** methodology for Context-Driven Development.

## Overview

This skill enables Maestro to follow Conductor's structured development workflow:

- **Context-Driven Development**: Maintain project context (product, tech stack, guidelines) that drives all development decisions
- **Spec-First Planning**: Create specifications and plans before writing code
- **Track-Based Organization**: Organize work into "tracks" (features, bugs, chores)
- **TDD Workflow**: Follow Test-Driven Development with clear phases
- **Git-Aware Operations**: Track progress through commits and enable smart reverts

## Installation

This skill follows the [Agent Skills specification](https://agentskills.io/specification). Copy the skill directory to your agent's skills location.

## Skill Structure

```
maestro-conductor-skill/
├── SKILL.md                    # Main skill file (required)
├── README.md                   # Documentation
├── LICENSE                     # Apache 2.0 license
├── scripts/                    # Executable code
│   └── conductor_skill.py      # Python utilities
├── references/                 # Additional documentation
│   ├── workflow.md             # Detailed workflow rules
│   └── commands/               # Command protocols
│       ├── setup.md
│       ├── new_track.md
│       ├── implement.md
│       ├── status.md
│       └── revert.md
└── assets/                     # Static resources
    └── templates/              # Project templates
        ├── product.md
        ├── product-guidelines.md
        └── tech-stack.md
```

## Commands

| Command | Description |
|---------|-------------|
| `/conductor:setup` | Initialize Conductor environment for a new or existing project |
| `/conductor:newTrack [description]` | Create a new track with specification and plan |
| `/conductor:implement [track_name]` | Execute tasks following TDD workflow |
| `/conductor:status` | Display current project and track progress |
| `/conductor:revert` | Git-aware revert of tracks, phases, or tasks |

## Conductor Project Structure

When you run `/conductor:setup`, it creates:

```
conductor/
├── product.md              # Product definition
├── product-guidelines.md   # Brand/communication guidelines
├── tech-stack.md          # Technology stack
├── workflow.md            # Development workflow
├── tracks.md              # Track registry
├── code_styleguides/      # Style guides by language
└── tracks/                # Individual tracks
    └── <track_id>/
        ├── spec.md
        ├── plan.md
        └── metadata.json
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

## Credits

Based on [Gemini CLI Conductor](https://github.com/gemini-cli-extensions/conductor) extension.

## License

Apache License 2.0