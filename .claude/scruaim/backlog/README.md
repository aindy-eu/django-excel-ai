# Backlog System - Django Excel AI Validator

> Track and prioritize work systematically

## Workflow

```
backlog.md → in-progress.md → completed.md
```

## Files

### backlog.md
- **Purpose**: Prioritized list of all pending user stories
- **Format**: Ordered by priority (highest first)
- **Update**: When new stories are added or priorities change

### in-progress.md
- **Purpose**: Track currently active work
- **WIP Limit**: Maximum 3 stories
- **Update**: When starting/pausing/completing work
- **Contains**: Story reference, start date, assigned to, blockers

### completed.md
- **Purpose**: Archive of completed stories with lessons learned
- **Update**: When stories are done
- **Contains**: Story reference, completion date, actual time, lessons

## How to Use

### 1. Starting Work
```bash
# Pick top item from backlog.md
# Move to in-progress.md
# Update status and start date
```

### 2. During Work
```bash
# Update blockers if any arise
# Add notes about challenges
# Track actual time spent
```

### 3. Completing Work
```bash
# Move story files to done/
# Update in-progress.md (remove item)
# Add to completed.md with lessons learned
# Pick next item from backlog.md
```

## WIP Limit Rules

**Maximum 3 stories in progress**

Why?
- Prevents context switching
- Ensures focus
- Identifies blockers quickly
- Improves completion rate

If at WIP limit:
1. Finish current work first
2. Or explicitly pause/blocked one
3. Document why if exceeding temporarily

## Priority Guidelines

### High Priority
- Blocking other work
- User-facing bugs
- Security issues
- Core functionality

### Medium Priority
- New features
- Performance improvements
- Developer experience
- Technical debt

### Low Priority
- Nice-to-have features
- Cosmetic changes
- Documentation
- Refactoring (non-critical)

## Status Indicators

Use these in in-progress.md:

- 🟢 **Active** - Currently working
- 🟡 **Paused** - Temporarily stopped
- 🔴 **Blocked** - Waiting on something
- 🔵 **Review** - Implementation complete, reviewing

## Time Tracking

Track both estimated and actual time:
```markdown
- Estimated: 4 hours
- Actual: 5.5 hours (database migration issues)
```

This helps improve future estimates.

## Lessons Learned Format

When completing stories, capture:

```markdown
### Story: [Story Name]
**What went well:**
- [Positive outcome]

**What was challenging:**
- [Difficulty encountered]

**What we learned:**
- [Key insight for future]

**Time difference:**
- Estimated: X hours
- Actual: Y hours
- Reason: [Why different]
```

## Backlog Grooming

Weekly/Sprint tasks:
1. Review priorities
2. Remove obsolete stories
3. Break down large stories
4. Update estimates based on learnings
5. Ensure top 5 are ready to work

## Metrics to Track

Over time, monitor:
- Average completion time vs estimates
- Common blockers
- Types of work that run over
- Velocity trends

## Integration with User Stories

- Reference story files: `user-stories/todo/001-feature.md`
- Keep story details in story files
- Backlog tracks status and metadata only
- Don't duplicate information

## Tips for Success

1. **Update daily** - Keep status current
2. **Be honest** - About blockers and challenges
3. **Learn from patterns** - Similar stories should improve
4. **Communicate blocks** - Don't stay stuck
5. **Celebrate completions** - Finished work = progress

## Anti-Patterns

❌ Starting new work when blocked (communicate instead)
❌ Not updating status (creates confusion)
❌ Exceeding WIP limit without reason
❌ Not capturing lessons learned
❌ Keeping zombies stories that won't be done

## Quick Commands

```bash
# See current work
cat .claude/scruaim/backlog/in-progress.md

# Check priorities
head -20 .claude/scruaim/backlog/backlog.md

# Review completed
tail -50 .claude/scruaim/backlog/completed.md
```