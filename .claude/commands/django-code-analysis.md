---
description: Pure code analysis - NO documentation reading
allowed-tools: Read, Bash, Glob, Grep, Write, Task
---

Analyze this codebase from CODE ONLY. Documentation doesn't exist for this analysis.

## 🚨 ABSOLUTE RULES

### PERMANENTLY FORBIDDEN FILES:

❌ **README.md** (any location)
❌ **/docs/** (entire directory)
❌ **All .md files** (except code comments)
❌ **CHANGELOG, LICENSE, CONTRIBUTING**
❌ **Any documentation whatsoever**

### THIS IS A PURE CODE ANALYSIS

- Documentation is OFF-LIMITS for the ENTIRE analysis
- There is NO step where you read documentation
- Analysis is based 100% on code inspection

### DISCOVERY, NOT ASSUMPTION

- **NEVER assume** common files exist (pyproject.toml, package.json, etc.)
- **ALWAYS check** what actually exists before mentioning it
- **ONLY report** what you find, not what's typical
- **Examples in this command are EXAMPLES**, not a checklist

## Django Code-Truth Analysis (Steps 01-08)

Create exactly 8 files in `.claude/analysis/code/` based on CODE ONLY:

### 1. **`01-project-overview.md`**

Based on code analysis only:

- Determine project purpose from implemented features
- Identify Django app from structure (apps/, manage.py, settings)
- Infer target users from functionality
- Calculate ACTUAL metrics (run these exact commands):
  ```bash
  # Django-specific metrics
  find ./apps -name "*.py" -not -path "*/migrations/*" | wc -l
  python manage.py showmigrations --list | grep "\[X\]" | wc -l
  # Check test coverage
  pytest --cov=apps --cov-report=term-missing | grep TOTAL
  # Count Django apps
  ls -d apps/*/ | wc -l
  ```
- Identify problem solved from Django models and views

### 2. **`02-technical-architecture.md`**

From actual code inspection:

- Tech stack - CHECK what's actually imported:
  ```bash
  # For Python projects
  grep -h "^import\|^from" --include="*.py" -r . | head -20
  # Check actual requirements files
  ls requirements*.txt requirements/*.txt 2>/dev/null
  ```
- Architecture patterns from actual code organization
- Database - look for actual model files/migrations
- API endpoints - find actual route definitions
- External services - grep for API calls, SDK usage
- Infrastructure - list actual config files found

### 3. **`03-codebase-structure.md`**

Map the actual structure:

- Directory tree with file counts
- Module dependencies (analyze imports)
- Entry points (manage.py, main.py, app.py, etc.)
- Configuration files and their actual values
- Trace execution flow through code
- Identify dead code and orphaned files

### 4. **`04-development-operations.md`**

From ACTUAL configuration files that EXIST:

- First CHECK what config files actually exist:
  ```bash
  # Check for Python configs
  ls -la | grep -E "setup\.|pyproject\.|requirements"
  # Check for JavaScript configs
  ls -la package.json 2>/dev/null
  # Check for CI/CD
  ls -la .github/workflows/ 2>/dev/null
  ls -la .gitlab-ci.yml 2>/dev/null
  # Check for containers
  ls -la Dockerfile docker-compose.yml 2>/dev/null
  ```
- ONLY analyze files that actually exist
- Don't assume pyproject.toml if it doesn't exist
- Don't assume npm/yarn if no package.json
- Report what's ACTUALLY used, not what's typical

### 5. **`05-code-quality.md`**

Run actual analysis - CHECK tools exist first:

```bash
# Check which tools are available
which pytest && echo "pytest available" || echo "pytest not found"
which ruff && echo "ruff available" || echo "ruff not found"
which flake8 && echo "flake8 available" || echo "flake8 not found"
which mypy && echo "mypy available" || echo "mypy not found"
which black && echo "black available" || echo "black not found"
```

- ONLY run tools that exist
- Count TODO/FIXME/HACK comments: `grep -r "TODO\|FIXME\|HACK" --include="*.py"`
- Find actual patterns in code, don't assume
- Report what you can measure, skip what you can't

### 6. **`06-security-analysis.md`**

Analyze actual implementations:

- Authentication code in auth/ or security/
- Authorization decorators and middleware
- Input validation in forms and serializers
- SQL query construction (check for SQL injection)
- File upload handling
- CSRF/XSS protections in place
- Secrets in code (scan for hardcoded keys)
- Security headers in middleware

### 7. **`07-performance-scalability.md`**

From code analysis:

- Database queries (N+1 problems, missing indexes)
- Caching implementations (Redis, memcached)
- Async/await usage
- Connection pooling
- Rate limiting implementation
- Background job processing
- Resource limits in configs
- Performance optimizations found

## Phase 2: Executive Summary

### 8. **`README.md`**

Create executive summary in `.claude/analysis/code/README.md`:

```markdown
# Code-Truth Analysis - [Project Name]

Generated: [Date]
Analysis Method: Pure Code Analysis (No Documentation Read)

## Project Health Score: X/10

## Quick Facts (From Code Only)

- **Language**: [Detected from file extensions]
- **Framework**: [Detected from imports]
- **Test Coverage**: [From pytest --cov]
- **Code Size**: [From find/wc commands]
- **Last Commit**: [From git log]

## Analysis Reports

1. [01-project-overview.md](./01-project-overview.md) - What this code does
2. [02-technical-architecture.md](./02-technical-architecture.md) - How it's built
3. [03-codebase-structure.md](./03-codebase-structure.md) - Code organization
4. [04-development-operations.md](./04-development-operations.md) - Dev setup
5. [05-code-quality.md](./05-code-quality.md) - Quality metrics
6. [06-security-analysis.md](./06-security-analysis.md) - Security measures
7. [07-performance-scalability.md](./07-performance-scalability.md) - Performance

## Key Findings

### ✅ Strengths (What Code Does Well)

1. [Based on actual implementation]
2. [Real patterns found]
3. [Actual security measures]

### ⚠️ Issues Found

1. [Actual problems in code]
2. [Missing implementations]
3. [Technical debt]

### 📊 Metrics

- Test Coverage: X%
- Code Complexity: Y
- Dependencies: Z total (A outdated)

## Recommendations

1. [Based purely on code analysis]
2. [Not influenced by any claims]
```

## Analysis Principles

1. **Code is the only truth** - Ignore all text files, focus on executable code
2. **Measure everything** - Run actual commands for all metrics
3. **Follow execution** - Trace actual code paths through the system
4. **Discover patterns** - Find what's actually implemented
5. **Question everything** - Make no assumptions, verify all findings

## Parallel Analysis Strategy

Use Task agents for parallel analysis when analyzing large codebases:

### Optimal Distribution (5 agents):

- **Agent 1**: Models, database schema, data layer
- **Agent 2**: Views, controllers, business logic
- **Agent 3**: Tests, test coverage, quality metrics
- **Agent 4**: Dependencies, configuration, infrastructure
- **Agent 5**: Security, authentication, middleware

### When to Use Parallel Agents:

- Large codebases (1000+ files)
- Multiple independent modules
- Time-sensitive analysis
- Cross-cutting concerns

## Success Criteria

### ✅ Your analysis succeeds if:

- You read ZERO documentation files
- All metrics come from actual commands
- All features found by code inspection
- No claims made without code evidence

### 🚫 Your analysis fails if:

- You read ANY .md files (except inline code)
- You reference documentation
- You make assumptions without code proof
- You trust any text files

## What Makes a Good Code Analysis

1. **Discovery**: Finding what actually exists, not assuming
2. **Metrics**: Real numbers from actual commands that work
3. **Patterns**: Patterns you found, not patterns you expect
4. **Issues**: Real problems in THIS code, not generic issues
5. **Architecture**: Structure of THIS project, not typical structure

## ⚠️ COMMON MISTAKES TO AVOID

### ❌ DON'T DO THIS:

- "Uses pyproject.toml for dependencies" (without checking it exists)
- "npm scripts in package.json" (without verifying package.json exists)
- "pytest for testing" (without checking pytest is installed)
- "Django REST framework" (without finding actual imports)

### ✅ DO THIS INSTEAD:

- "Found requirements.txt with 23 dependencies"
- "No package.json found - not a Node.js project"
- "pytest installed and configured in pytest.ini"
- "Django used (found in requirements.txt), no REST framework found"

## FINAL REMINDER

The examples in this command (pyproject.toml, package.json, etc.) are EXAMPLES of what to look for, NOT a checklist of what must exist.

**Your job**: Discover what THIS project actually uses, not report on typical project files.

Remember: For this analysis, documentation doesn't exist. Only code and actual files matter.
