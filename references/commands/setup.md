# Conductor Setup Protocol

You are executing the Conductor setup protocol for Context-Driven Development.

## Prerequisites

1. Check if `conductor/` directory exists with required files:
   - `conductor/product.md`
   - `conductor/tech-stack.md`
   - `conductor/workflow.md`

If these exist, inform the user: "Conductor is already set up. Use `/conductor:newTrack` to create a new track or `/conductor:implement` to start implementation."

## Setup Steps

### 1. Project Detection

Analyze the current directory:
- **Brownfield** (existing project): Has `.git`, `package.json`, `requirements.txt`, `src/`, etc.
- **Greenfield** (new project): Empty or minimal files

### 2. Create Conductor Directory Structure

```
conductor/
├── product.md
├── product-guidelines.md
├── tech-stack.md
├── workflow.md
├── tracks.md
├── setup_state.json
└── code_styleguides/
```

### 3. Interactive Context Gathering

For each context file, ask the user targeted questions:

**Product Definition (product.md):**
- What are you building?
- Who are the target users?
- What are the main goals?
- What are the key features?

**Product Guidelines (product-guidelines.md):**
- What is the brand voice/tone?
- Any visual identity guidelines?
- UX principles to follow?

**Tech Stack (tech-stack.md):**
- For greenfield: What languages/frameworks?
- For brownfield: Analyze existing dependencies and confirm

**Workflow (workflow.md):**
- TDD required? (default: yes)
- Code coverage target? (default: 80%)
- Commit frequency? (after task or phase)

### 4. Generate Initial Track

Ask: "What's the first feature or task you want to work on?"

Create the initial track with:
- `conductor/tracks/<track_id>/spec.md`
- `conductor/tracks/<track_id>/plan.md`
- `conductor/tracks/<track_id>/metadata.json`

Update `conductor/tracks.md` with the new track entry.

### 5. Completion

Announce: "Conductor setup is complete! Run `/conductor:implement` to start working on your first track."