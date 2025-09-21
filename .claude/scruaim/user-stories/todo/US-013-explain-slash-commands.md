# User Story: Explain Slash Commands

**ID**: US-013
**Created**: 2025-09-20
**Status**: TODO
**Effort**: 1 hour
**Value**: High (Deep Analysis)
**Risk**: Low

## Story

**As a** developer maintaining this project
**I want** to understand the slash commands and their outputs
**So that** I can generate deep analysis when needed

## Background

This project includes two powerful slash commands that generate comprehensive analysis. These commands created the detailed analysis in `.claude/analysis/` folder, providing deep insights into the codebase without relying on potentially outdated documentation. This story will explain what they do, show their outputs, and demonstrate their value.

## Acceptance Criteria

- [ ] Developer understands what slash commands are
- [ ] Developer sees the actual analysis generated
- [ ] Developer knows when to use each command
- [ ] Developer understands "code is truth" principle
- [ ] Developer can run the commands themselves
- [ ] Document shows real outputs from this project

## Technical Design

### Output File: `docs/tools/slash-commands.md`

Create a practical guide showing:

```markdown
# Slash Commands: Deep Analysis Tools

## What Are Slash Commands?

Custom commands that generate comprehensive analysis

## The Two Commands

[Explain code vs docs analysis]

## What They Generated

[Show actual outputs from this project]

## When to Use Them

[Practical triggers and scenarios]

## How to Use Them

[Step-by-step execution guide]
```

## Implementation Notes

### 1. Discovery Process

Show HOW to find and understand the commands:

```markdown
## Discovering Slash Commands

### Step 1: Find the Commands
```bash
# Check what commands exist:
ls -la .claude/commands/
cat .claude/commands/*.md | head -50

# Count available commands:
ls .claude/commands/*.md | wc -l
```

### Step 2: Understand Their Purpose
```bash
# Read each command's description:
grep "description:" .claude/commands/*.md

# Check allowed tools:
grep "allowed-tools:" .claude/commands/*.md
```

### Step 3: Find Their Output
```bash
# See what they generated:
ls -la .claude/analysis/
ls -la .claude/analysis/code/
ls -la .claude/analysis/docs/

# Read the executive summary:
cat .claude/analysis/code/README.md
```

### What You'll Discover
- Commands generate comprehensive analysis
- One focuses on code truth
- One verifies documentation
- Output saved in .claude/analysis/
```

### 2. Analyze Generated Output

Guide exploration of results:

```markdown
## Exploring the Analysis Output

### Check What Was Generated
```bash
# List all analysis files:
find .claude/analysis -name "*.md" -type f

# Check file sizes (substance):
ls -lh .claude/analysis/code/*.md

# Sample the content:
head -20 .claude/analysis/code/01-project-overview.md
head -20 .claude/analysis/code/05-code-quality.md
```

### Extract Key Findings
```bash
# Find metrics:
grep -i "coverage\|lines\|files" .claude/analysis/code/*.md

# Find technology stack:
grep -i "django\|postgres\|htmx" .claude/analysis/code/*.md

# Find issues or recommendations:
grep -i "issue\|problem\|recommend" .claude/analysis/code/*.md
```

### What the Analysis Reveals
- Project metrics and health
- Technology choices made
- Architecture patterns used
- Quality measurements
```

### 3. Understanding the Philosophy

Discover the principle from the commands:

```markdown
## Understanding "Code is Truth"

### Read the Command Philosophy
```bash
# Look for the principle:
grep -A5 -B5 "truth\|documentation" .claude/commands/django-code-analysis.md

# Find forbidden items:
grep "FORBIDDEN\|NEVER\|avoid" .claude/commands/django-code-analysis.md
```

### Compare Analysis Types
```bash
# See the difference:
diff <(head -50 .claude/commands/django-code-analysis.md) \
     <(head -50 .claude/commands/django-docs-analysis.md)
```

### What This Reveals
- Code analysis ignores ALL documentation
- Metrics come from actual commands
- Documentation verification comes separately
- Truth derived from implementation only
```

### 4. When to Run Analysis

Practical triggers:

```markdown
## When to Generate Fresh Analysis

### Triggers for Code Analysis

Run when:
- Taking over a project
- After major refactoring
- Before architectural decisions
- Debugging mysterious issues
- Every 7-14 days minimum

### Triggers for Docs Verification

Run when:
- Documentation seems wrong
- Onboarding new developers
- Before releases
- After feature completion

### Real Scenario

This project ran analysis when:
1. Initial exploration (understand structure)
2. After AI integration (verify patterns)
3. Before open-sourcing (ensure accuracy)
````

### 5. Execution Guide

Step-by-step instructions:

```markdown
## How to Run Commands

### Running Code Analysis

1. **Trigger the command**:
```

Use: /code-analysis
Or manually: Follow django-code-analysis.md

```

2. **Wait for completion** (10-15 minutes)

3. **Review outputs** in `.claude/analysis/code/`

4. **Check README.md** for executive summary

### Running Docs Verification

1. **After code analysis complete**

2. **Trigger**: /docs-analysis

3. **Review** verification reports

4. **Update** outdated documentation

### Tips for Best Results

- Ensure clean git state
- Run tests first
- Have dependencies installed
- Close other heavy processes
```

### 6. Value Demonstration

Show the impact:

```markdown
## Value Delivered

### For This Project

#### Before Analysis

- Assumed Django REST framework used
- Thought Celery was required
- Unclear about test coverage

#### After Analysis

- Discovered HTMX-only approach
- Found synchronous processing
- Confirmed 86% coverage

### Time Saved

Manual analysis: 4-6 hours
Slash command: 15 minutes
Accuracy: 100% vs ~70%

### Decisions Enabled

Based on analysis:

- Kept HTMX (no React needed)
- Didn't add Celery (unnecessary)
- Focused on raising coverage
```

### 7. Template for Your Project

Provide reusable template:

````markdown
## Creating Your Own Commands

### Basic Template

```markdown
---
description: Analyze [project type]
allowed-tools: Read, Bash, Glob, Grep, Write
---

Analyze this codebase:

1. Discover structure
2. Verify claims
3. Measure metrics
4. Generate reports
```
````

### Customization Points

- Add language-specific checks
- Include framework detection
- Measure domain metrics
- Generate team-specific reports

```

## Testing Plan

Validate documentation by checking:
- Can developer understand the commands?
- Are outputs clearly explained?
- Is execution guide followable?
- Does value proposition resonate?

## Success Metrics

Documentation succeeds when:
- Reader understands command purpose
- Reader can execute commands
- Reader sees value in analysis
- Reader adopts "code is truth" mindset

## Out of Scope

- Scruaim framework (US-011)
- Handover process (US-012)
- Writing custom commands
- AI technical details

## Notes

Focus on showing actual outputs and discoveries from this project. Emphasize how the commands revealed truth that documentation missed. Make it practical, not theoretical.

---

*"Code is truth, documentation is hope"*
```
