# AI Handover System - Django Excel AI Validator

## Purpose

This system preserves **institutional knowledge** across AI context resets and team transitions. When context windows fill or work pauses, handovers capture the reasoning and discoveries that would otherwise be lost.

## When to Create Handovers

### Create a handover when:
- **Context is scarce** (< 15% remaining) but work continues
- **Significant discoveries** were made that aren't obvious from code
- **Complex decisions** need reasoning preserved
- **Work will pause** and resume later
- **Dead ends explored** that shouldn't be repeated

### Skip handovers when:
- Work completed naturally
- Changes are straightforward
- No significant discoveries made

## Handover Template

Create handovers as: `YYYYMMDD-topic.md`

```markdown
# Handover: [Topic/Feature] - [Date]

## Context & Goals
- **What we were working on**: [Main objective]
- **Why this matters**: [Business/technical reason]
- **Key constraints**: [Limitations, requirements]
- **Success criteria**: [How we know it's done]

## Key Decisions Made
- **[Decision]**: [What was chosen] because [reasoning]. Rejected [alternative] due to [reason].
<!-- Add more decisions as needed -->

## Discoveries & Insights
- **Pattern found**: [What you discovered and why it matters]
- **Performance insight**: [Metric before] → [after] via [approach]
- **Gotcha encountered**: [Trap that wasn't obvious]
<!-- Capture non-obvious learnings -->

## Current State
- **Completed**:
  - [What's fully done]
- **In Progress**:
  - [Current work and its state]
- **Not Started**:
  - [Planned but not begun]

## Django-Specific Sections

### Database Schema Decisions
- **Model design choices**: [Why specific field types/relationships]
- **Migration strategy**: [How complex migrations are handled]
- **PostgreSQL features used**: [JSONField, ArrayField, etc.]

### Authentication & Security
- **Permission architecture**: [How authorization is structured]
- **Allauth customizations**: [Extensions to django-allauth]
- **Security middleware**: [Custom security implementations]
- **PII encryption approach**: [GDPR compliance strategy]

### API Design Patterns
- **View architecture**: [CBV vs FBV decisions]
- **Serialization approach**: [How data is formatted]
- **URL namespace strategy**: [How URLs are organized]

### Performance Optimizations
- **Query optimizations**: [select_related, prefetch_related patterns]
- **Caching strategy**: [What's cached and why]
- **Static file handling**: [Whitenoise, CDN decisions]

## Next Steps (Priority Order)
1. **Immediate**: [Most urgent/important]
2. **Next**: [Following priority]
3. **Future**: [Nice to have/consider later]

## What Files Don't Show
- **Why approaches were chosen**: [Reasoning not in code]
- **Business context**: [Stakeholder input, user feedback]
- **Failed attempts**: [What didn't work and why - saves time]

## For Next AI/Human
- **Start here**: [Specific file or entry point]
- **Key context**: [Essential knowledge for continuation]
- **Watch out for**: [Traps or gotchas to avoid]
```

## Django Project Specific Patterns

### Enterprise Architecture Decisions
- **No Django Admin in production**: Using custom backoffice views instead
- **Split settings**: base/dev/staging/prod configuration
- **App structure**: `apps/` for business logic, `libs/` for shared code
- **PRM compliance**: Code duplication extracted after 2+ uses

### Testing Strategy
- **pytest over Django TestCase**: More flexible fixtures, better markers
- **Enterprise folder structure**: Tests in `apps/*/tests/` folders
- **Factory pattern**: Using factory-boy for test data generation
- **Coverage target**: 70% minimum (currently achieving 87%)
- **Security tests mandatory**: Each view must test auth/permissions
- **Performance tests**: Database query counts tracked

### Tailwind CSS Integration
- **Utility-first**: Custom CSS only when necessary
- **Component patterns**: Reusable templates in `templates/components/`
- **Build process**: `python manage.py tailwind` commands

## Quality Guidelines

### Good Handovers Include:
- **Decision reasoning** - The why, not just what
- **Time-saving context** - Prevents re-discovery
- **Clear next steps** - Obvious continuation path
- **Discovered patterns** - Non-obvious insights
- **Django gotchas** - Framework-specific traps

### Good Handovers Exclude:
- **Code transcripts** - Code explains itself
- **Obvious information** - What's clear from files
- **Personal opinions** - Stick to facts and reasoning
- **Conversation logs** - Focus on knowledge

## Examples

### Django Migration Decision
```markdown
## Key Decisions Made
- **Custom User model from start**: Django strongly recommends this even if not immediately needed. Changing later requires complete database rebuild.
```

### Query Optimization Discovery
```markdown
## Discoveries & Insights
- **Dashboard queries N+1**: DashboardView loading user.profile.organization on each widget. Added select_related('profile__organization') - 15 queries → 3 queries.
```

### Security Pattern
```markdown
## What Files Don't Show
- **Avoided @login_required decorator**: Using LoginRequiredMixin consistently for CBVs provides better inheritance and testing patterns.
```

## Recovery Integration

When starting fresh with a handover:

1. **Read handover first** - Get context before diving into code
2. **Check "Current State"** - Understand what's done/pending
3. **Review "Next Steps"** - Clear priorities
4. **Note "What Files Don't Show"** - Avoid repeating failures
5. **Check .claude/scruaim/backlog/** - Current sprint priorities

## Privacy & Storage

Handovers should be:
- **Stored in**: `.claude/handovers/`
- **Gitignored**: Keep `*.md` files local, only track README
- **Honest**: Private storage enables frank documentation
- **Sanitized if shared**: Remove sensitive details before sharing

## Integration with .scruaim

- **User stories**: Reference `.claude/scruaim/user-stories/` for business context
- **Backlog**: Check `.claude/scruaim/backlog/in-progress.md` for WIP
- **Patterns**: Align with `.claude/scruaim/user-stories/INSTRUCTIONS.md`

## Maintenance

- **Archive old handovers** to `archive/` subfolder after 3+ months
- **Update this README** based on what patterns work for your team
- **Extract patterns** that appear in multiple handovers to INSTRUCTIONS.md

## Recent Handovers

### [20250920-documentation-cleanup.md](./20250920-documentation-cleanup.md)
**Date**: September 20, 2025
**Focus**: Documentation verification and open source preparation
**Key Achievement**: Transformed interview project into open-source ready application
**Highlights**:
- Verified 15+ documentation files (75% → 98% accuracy)
- Updated to Claude Sonnet 4 with real production metrics
- Created Rails-to-Django guide
- Removed all interview artifacts
- Fixed critical dev-start.sh bug

## Getting Started

1. **Create your first handover** when you hit a trigger
2. **Use Django sections** for framework-specific insights
3. **Reference .claude/scruaim** for business context
4. **Iterate based on value** - keep what helps, drop what doesn't

---

*The goal: Create institutional memory that makes future Django work faster and smarter.*